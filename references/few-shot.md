# Few-Shot Patterns

Use these examples as style anchors. Do not copy coordinates blindly; copy the construction strategy.

## 1. Triangle + Incenter + Incircle

Source pattern: `../tsqx/examples/figures/fig1.tsqx`

```tsqx
A = dir 110
B = dir 210
C = dir 330
I 45 = incenter A B C

A--B--C--cycle / 0.12 lightcyan / blue
incircle A B C / 0.15 lightgreen / darkgreen
A--I / red
B--I / red
C--I / red
```

Use this pattern when the statement centers on a standard triangle center and one canonical circle.

## 2. Orthocenter + Pedal Triangle

Source pattern: `../tsqx/examples/figures/fig2.tsqx`

```tsqx
A = dir 95
B = dir 215
C = dir 330
H = orthocenter A B C
D = foot H B C
E = foot H C A
F = foot H A B

A--B--C--cycle / 0.08 lightyellow / blue
D--E--F--cycle / 0.15 lightcyan / red
A--D / gray
B--E / gray
C--F / gray
```

Use this pattern when a point is defined first, then several feet are dropped to sides.

## 3. Circle Through Given Points With Line Intersections

Source pattern: `../tsqx/personal/week_02_20260313/blue-ch01-p3.tsqx`

```tsqx
C = dir 110
A = dir 200
B = dir 320
I N = incenter A B C
O 90 = circumcenter A I B
!path circleO = circumcircle(A, I, B);
P 180 = OP circleO (Line C A)
Q 0 = OP circleO (Line C B)
```

Use this pattern when a derived circle must meet known lines again.

## 4. Perpendicular Helper Line Via Raw Asymptote

Source pattern: `../tsqx/personal/handout/Mon_3/images/blue-ch01-p8.tsqx`

```tsqx
H 270 ;= orthocenter A B C
!pair pBH = H + rotate(90)*(B-H);
D 140 ;= extension A B H pBH
```

Use this when the statement says "through point X draw a line perpendicular to YZ" and plain TSQX syntax alone is awkward.

## 5. Tangent-Circle Or Mixed TSQX/Asymptote Figure

Source pattern: `../tsqx/personal/week_02_20260313/2025p1.tsqx`

Observed strategy:

- keep the main named construction in TSQX
- isolate hard geometry into small `!pair` or helper functions
- return to TSQX-style drawing commands for the main figure

Use this pattern for advanced olympiad-style diagrams where a pure TSQX encoding would become less readable than a hybrid approach.

## 6. Explicit Coordinates For Strict Constraint Satisfaction

Source pattern: `../tsqx/personal/week_02_20260313/2025gd.tsqx`

Observed strategy:

- choose coordinates directly when exact problem constraints matter more than synthetic elegance
- annotate why those coordinates were chosen
- derive the remaining points from the stated conditions

Use this when the figure must satisfy algebraic constraints exactly and a synthetic construction would be harder to control.
