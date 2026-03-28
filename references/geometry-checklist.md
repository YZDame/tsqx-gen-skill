# Geometry Checklist

Before writing TSQX, extract the following if present:

- named points
- free points versus constructed points
- collinear relations
- parallel or perpendicular relations
- equal lengths or equal angles
- circles, tangency, and cyclic relations
- intersections
- midpoints, feet, centroids, circumcenters, incenters, orthocenters
- extension points on rays or lines
- shaded or highlighted regions
- labels that must remain visible

Then decide:

1. Which objects are primitive?
2. Which objects should be derived from primitives?
3. Which relations are exact versus merely visual?
4. What is the simplest coordinate or constructive model that preserves the exact relations?

Common failure modes:

- encoding a diagram guess as a hard constraint
- using coordinates that accidentally break symmetry or incidence
- omitting helper objects needed for the final visual
- reproducing a proof idea instead of the actual figure
- overcomplicating coordinates when a simpler construction would be clearer
