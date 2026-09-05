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

