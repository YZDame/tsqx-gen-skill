# TSQX Idioms

Use this file to stay close to the style and capability boundaries seen in `../tsqx/examples` and real local usage under `../tsqx/personal`.

## Construction Priorities

Prefer these layers in order:

1. Free anchor points with explicit coordinates or `dir`
2. Standard derived points using TSQX built-ins
3. Intersections and extensions
4. Circles and highlighted paths
5. Raw Asymptote injected with `!` only when TSQX syntax is not enough

## Common Built-ins Seen In Practice

- `midpoint A--B`
- `foot P A B`
- `incenter A B C`
- `orthocenter A B C`
- `circumcenter A B C`
- `extension A B C D`
- `IP (Line A B) (Line C D)`
- `OP path (Line A B)`
- `incircle A B C`
- `circumcircle A B C`

These are the first options to try before injecting raw Asymptote.

## Label And Dot Conventions

Observed patterns:

- `A = dir 110`
- `I 45 = incenter A B C`
- `H NW = orthocenter A B C`
- `D 220 ;= midpoint B--C`

Guidance:

- Keep the original point names from the problem if possible.
- Add direction hints when labels are likely to overlap.
- Use `:=` or `;=` only when that improves label or dot behavior and the example pattern clearly matches.

## Drawing Conventions

Common patterns from local examples:

```tsqx
A--B--C--cycle / 0.08 lightyellow / grey
D--E--F--cycle / 0.15 lightcyan / red
A--D / gray
circleO / gray
N--P--M / red dashed
```

Guidance:

- Draw the main polygon first.
- Then draw auxiliary lines.
- Then draw circles or highlighted relations.
- Use color sparingly to indicate logical role, not decoration.

## When To Use Raw Asymptote

Use `!` blocks when you need:

- helper functions
- explicit `path` or `pair` objects
- tangent constructions not expressible cleanly in TSQX alone
- vector arithmetic such as `rotate(90) * (B-A)`

Examples from real usage:

```tsqx
!path w = circumcircle(A, B, C);
!pair pBH = H + rotate(90)*(B-H);
!pair O1 = solveCenterThroughTwoPtsTangentLine(B, P, A, C, true);
```

Do not jump to raw Asymptote too early. First ask whether a built-in TSQX construction already exists.

## Faithfulness Rules

- Preserve incidence before exact metric appearance.
- Prefer a simple valid model over a visually perfect but overconstrained one.
- If the diagram is only suggestive, avoid hard-coding guessed equalities or perpendicularities.
- When a problem uses a line extension, represent the extension explicitly instead of faking the point with arbitrary coordinates.

## Typical Pattern Families

### Triangle Center Figures

Use free points for `A B C`, then derive `I`, `H`, `G`, or `O`.

### Foot And Altitude Figures

Use `foot` first. If the statement gives a perpendicular line through a derived point, use a helper `!pair` with `rotate(90)`.

### Circle-Line Intersection Figures

Represent the circle as `!path` and use `IP` or `OP` against `Line`.

### Handout-Style Composite Figures

Keep the construction readable. It is acceptable to mix TSQX with small injected Asymptote helpers when the geometry is genuinely more complex.
