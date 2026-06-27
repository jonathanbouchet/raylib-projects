## Motivation
This project compares Axis-Aligned Bounding Boxes (AABB), Oriented Bounding Boxes (OBB) methods for 2D collisions

- `pyray` is using AABB in its `pr.check_collisions_rects` and is not suited for rotated rectangles.
- got an OBB working but also found a py package doing the exact same thing: [polygoncollision](https://github.com/vertmit/PolygonCollision)
- the OBB method is using the Separating Axis Theorem  (SAT): The Separating Axis Theorem is a technique for solving convex polygon collision problems.  The Theorem postulates if a line can be drawn between two convex (and not concave) polygons the Polyhedra are not colliding.

Some related docs:
- https://code.tutsplus.com/collision-detection-using-the-separating-axis-theorem--gamedev-169t
- https://programmerart.weebly.com/separating-axis-theorem.html
- https://dev.to/pratyush_mohanty_6b8f2749/the-math-behind-bounding-box-collision-detection-aabb-vs-obbseparate-axis-theorem-1gdn