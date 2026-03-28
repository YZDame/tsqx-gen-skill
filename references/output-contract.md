# Output Contract

Use this default response shape unless the user asks for a different format.

## Assumptions

Short bullet list. Include only nontrivial inferences, such as:

- whether a point is assumed to lie on a segment extension
- whether a quadrilateral is treated as cyclic
- whether a visual midpoint or perpendicular mark is trusted

## Geometry Parse

Short factual summary of the construction:

- base objects
- derived objects
- target emphasis for drawing

This is not a proof. It is a construction summary.

## TSQX

Return one fenced block:

```tsqx
...
```

Prefer a single self-contained snippet.

## Checks

State one of:

- `Not compiled in this turn.`
- `Compiled successfully via tsqx -> asy.`
- `Compilation failed:` followed by one short reason.

Also mention whether the code preserves:

- incidence
- order / relative placement
- special constraints from the statement

## Open Questions

Only include when ambiguity remains. Keep it short and concrete.
