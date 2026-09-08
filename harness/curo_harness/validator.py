"""JSON Schema validation against repository-local Curo contracts."""

from __future__ import annotations

import datetime
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple, Union
from urllib.parse import unquote, urlparse

from .core import get_curo_root, safe_read_json, safe_write_json


def get_schema_path(schema_name: str) -> Path:
    """Resolve a canonical schema by short name or filename."""
    root = get_curo_root()
    requested = Path(schema_name).name
    names = [requested] if requested.endswith(".schema.json") else [f"{requested}.schema.json", requested]
    for directory in (root / "schemas", root / "observability"):
        for name in names:
            candidate = directory / name
            if candidate.is_file():
                return candidate.resolve()
    raise FileNotFoundError(f"Curo schema not found: {schema_name}")


def _json_type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    expected_type = {"string": str, "array": list, "object": dict}.get(expected)
    return True if expected_type is None else isinstance(value, expected_type)


def _resolve_ref(ref: str, schema_path: Path, document: Mapping[str, Any]) -> Tuple[Mapping[str, Any], Path, Mapping[str, Any]]:
    parsed = urlparse(ref)
    if parsed.scheme not in ("", "file"):
        raise ValueError(f"Unsupported non-local schema reference: {ref}")
    if parsed.scheme == "file":
        target_path = Path(unquote(parsed.path)).resolve()
    elif parsed.path:
        target_path = (schema_path.parent / unquote(parsed.path)).resolve()
    else:
        target_path = schema_path
    target_document = document if target_path == schema_path else safe_read_json(target_path)
    target: Any = target_document
    if parsed.fragment:
        if not parsed.fragment.startswith("/"):
            raise ValueError(f"Unsupported JSON pointer in $ref: {ref}")
        for part in parsed.fragment[1:].split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
    if not isinstance(target, Mapping):
        raise ValueError(f"Schema reference does not resolve to an object: {ref}")
    return target, target_path, target_document


def _fallback_validate(value: Any, schema: Mapping[str, Any], schema_path: Path,
                       document: Mapping[str, Any], instance_path: str = "$") -> List[str]:
    errors: List[str] = []
    if "$ref" in schema:
        try:
            target, target_path, target_document = _resolve_ref(str(schema["$ref"]), schema_path, document)
            return _fallback_validate(value, target, target_path, target_document, instance_path)
        except Exception as exc:
            return [f"{instance_path}: failed to resolve $ref '{schema['$ref']}': {exc}"]

    if "if" in schema:
        condition_errors = _fallback_validate(value, schema["if"], schema_path, document, instance_path)
        selected = schema.get("then") if not condition_errors else schema.get("else")
        if isinstance(selected, Mapping):
            errors.extend(_fallback_validate(value, selected, schema_path, document, instance_path))

    for keyword in ("allOf", "anyOf", "oneOf"):
        if keyword in schema:
            branch_errors = [
                _fallback_validate(value, branch, schema_path, document, instance_path)
                for branch in schema[keyword]
            ]
            valid_count = sum(not item for item in branch_errors)
            if keyword == "allOf":
                for item in branch_errors:
                    errors.extend(item)
            elif keyword == "anyOf" and valid_count == 0:
                errors.append(f"{instance_path}: value does not satisfy any allowed schema")
            elif keyword == "oneOf" and valid_count != 1:
                errors.append(f"{instance_path}: value must satisfy exactly one allowed schema")

    if "const" in schema and value != schema["const"]:
        errors.append(f"{instance_path}: value {value!r} does not equal required constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{instance_path}: value {value!r} is not in allowed enum {schema['enum']!r}")

    expected = schema.get("type")
    expected_types: Sequence[str] = [expected] if isinstance(expected, str) else (expected or [])
    if expected_types and not any(_json_type_matches(value, item) for item in expected_types):
        errors.append(f"{instance_path}: expected type {list(expected_types)!r}, got {type(value).__name__}")
        return errors

    if isinstance(value, str) and len(value) < int(schema.get("minLength", 0)):
        errors.append(f"{instance_path}: string is shorter than minLength {schema['minLength']}")
    if isinstance(value, str) and "pattern" in schema:
        try:
            if re.search(str(schema["pattern"]), value) is None:
                errors.append(f"{instance_path}: string does not match pattern {schema['pattern']!r}")
        except re.error as exc:
            errors.append(f"{instance_path}: invalid schema pattern {schema['pattern']!r}: {exc}")
    if isinstance(value, str) and schema.get("format") == "date-time":
        try:
            parsed = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed.tzinfo is None or parsed.utcoffset() is None:
                raise ValueError("timezone is required")
        except ValueError:
            errors.append(f"{instance_path}: value is not an ISO-8601 date-time with timezone")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{instance_path}: missing required property '{key}'")
        if len(value) < int(schema.get("minProperties", 0)):
            errors.append(f"{instance_path}: object has fewer than {schema['minProperties']} properties")
        properties = schema.get("properties", {})
        for key, item in value.items():
            if key in properties:
                errors.extend(_fallback_validate(item, properties[key], schema_path, document, f"{instance_path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{instance_path}: additional property '{key}' is not allowed")
            elif isinstance(schema.get("additionalProperties"), Mapping):
                errors.extend(_fallback_validate(item, schema["additionalProperties"], schema_path, document, f"{instance_path}.{key}"))
    if isinstance(value, list):
        if len(value) < int(schema.get("minItems", 0)):
            errors.append(f"{instance_path}: array has fewer than {schema['minItems']} items")
        if "maxItems" in schema and len(value) > int(schema["maxItems"]):
            errors.append(f"{instance_path}: array has more than {schema['maxItems']} items")
        if schema.get("uniqueItems") is True:
            canonical_items = [
                json.dumps(item, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
                for item in value
            ]
            if len(canonical_items) != len(set(canonical_items)):
                errors.append(f"{instance_path}: array items are not unique")
        if isinstance(schema.get("items"), Mapping):
            for index, item in enumerate(value):
                errors.extend(_fallback_validate(item, schema["items"], schema_path, document, f"{instance_path}[{index}]"))
    return errors


def validate_curo_payload(payload: Dict[str, Any], schema_name: str) -> Tuple[bool, List[str]]:
    """Validate without ambiguity: validation and resolver failures are explicit results."""
    try:
        schema_path = get_schema_path(schema_name)
        schema = safe_read_json(schema_path)
    except Exception as exc:
        return False, [f"Failed to load schema '{schema_name}': {exc}"]
    try:
        import jsonschema
        from referencing import Registry, Resource

        registry = Registry()
        for candidate in sorted(get_curo_root().glob("*/*.schema.json")):
            candidate_schema = safe_read_json(candidate)
            resource = Resource.from_contents(candidate_schema)
            registry = registry.with_resource(candidate.as_uri(), resource)
            if candidate_schema.get("$id"):
                registry = registry.with_resource(candidate_schema["$id"], resource)
        validator_class = jsonschema.validators.validator_for(schema)
        validator_class.check_schema(schema)
        validator = validator_class(schema, registry=registry)
        errors = [
            f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
            for error in sorted(validator.iter_errors(payload), key=lambda item: list(item.absolute_path))
        ]
        return not errors, errors
    except ImportError:
        pass
    except Exception as exc:
        return False, [f"JSON Schema validation failed explicitly: {exc}"]
    try:
        errors = _fallback_validate(payload, schema, schema_path, schema)
    except Exception as exc:
        return False, [f"Fallback schema validation failed explicitly: {exc}"]
    return not errors, errors


def validate_and_write_json(payload: Dict[str, Any], schema_name: str,
                            output_path: Union[str, Path]) -> Tuple[bool, List[str]]:
    """Persist an authoritative JSON artifact only after successful validation."""
    valid, errors = validate_curo_payload(payload, schema_name)
    if not valid:
        return False, errors
    try:
        safe_write_json(output_path, payload)
    except Exception as exc:
        return False, [f"Atomic persistence failed: {exc}"]
    return True, []
