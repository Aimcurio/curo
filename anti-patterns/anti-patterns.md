# Anti-Patterns

## 1. Self-reported validation

Do not let the model claim a validation check it did not actually run.

## 2. Invented provenance

Unknown provenance must remain unknown until the harness establishes it.

## 3. Model-first recovery

Do not jump straight to changing the model when a harness, context, loop, or prompt issue is the real cause.

## 4. Unowned records

If no component owns a record, the record is not authoritative.

## 5. Hidden authority

Any check, gate, or write path that cannot be inspected should be treated as a risk until proven otherwise.

## 6. Host-tethered document utilities

Do not assume external system binaries (e.g., Poppler's pdftoppm, Ghostscript, ImageMagick) exist in execution environments without providing a self-contained, reproducible portable fallback (e.g., pymupdf via uv run).

## 7. Destructive spatial heuristics & hardcoded parameters

Do not apply fixed coordinate-based margin zeroing, hardcoded morphological kernel sizes (e.g., 5x5), or absolute pixel intensity thresholds to documents. Document resolutions and exposures vary. Blind zeroing silently clips corner pagination (Page X of Y) and routing barcodes. Hardcoded kernels fail catastrophically across different DPIs. Always compute component bounds, preserve isolated machine-readable markers, and use dynamically calculated or percentile-based computer vision parameters.

## 8. Process success presented as validation success

Do not map exit code zero directly to provenance or validation `PASS`. A process result is only one input to evidence-backed validation.

## 9. Persist first, validate later

Do not write an authoritative artifact and validate it afterward. Identify its canonical schema, validate the complete payload, and only then perform the atomic write.

## 10. Shell strings as replay authority

Do not persist arbitrary shell syntax as a replay contract. Use a structured executable and ordered argument array, or a non-executing artifact verification manifest.

## 11. Prefix-based path containment

Do not authorize a path by string prefix. Resolve both the boundary and candidate and use path-aware containment so traversal, sibling-prefix, and drive-boundary escapes fail.

