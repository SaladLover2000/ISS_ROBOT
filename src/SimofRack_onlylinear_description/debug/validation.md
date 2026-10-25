# Validation Report: SimofRack_onlylinear

## Status: PASS (with warnings)

## Summary

| Metric | Value |
|--------|-------|
| Links | 8 |
| Joints | 7 |
| Assemblies | 6 |
| Root | `base_link` |
| Errors | 0 |
| Warnings | 2 |

## Warnings

- Multi-parent link detected (child=Top_support:1): keeping 'Top_Slider' as the URDF tree parent; routing ['Ybar_topslider'] to ``closing_joints`` (sidecar) — closed kinematic loop.  Tag the loop-closing joint(s) with prefix ``!closing_*`` in Fusion to make the choice explicit and avoid this warning.
- Root link renamed: 'Whole_Rack_Gemo' → 'base_link' (REP 120 convention). Consider renaming the component to 'base_link' in Fusion.

## Kinematic Tree

```
base_link [BAKE] [primitive]
  └─ Top_Slider [prismatic]
    Top_support [primitive]
  └─ Xslider18_Raack [fixed]
    Linear_Actuator_X_edited_Component18 [primitive]
      └─ Slider_2 [prismatic]
        Linear_Actuator_X_edited_Component1 [BAKE] [primitive]
          └─ Xplate_Ymotor [fixed]
            Linear_Actuator_Y_Component18 [primitive]
      └─ Slider_2_1 [prismatic]
        Linear_Actuator_Y_Component1 [BAKE] [primitive]
          └─ Rigid_52 [fixed]
            Component6 [primitive]
              └─ Slider_3 [prismatic]
                Component7 [BAKE] [primitive]
```

## Collision Geometry

| Link | Source | Shape/File |
|------|--------|------------|
| `Component6` | primitive STL | box |
| `Component7` | primitive STL | box |
| `Linear_Actuator_X_edited_Component1` | primitive STL | cylinder |
| `Linear_Actuator_X_edited_Component18` | primitive STL | box |
| `Linear_Actuator_Y_Component1` | primitive STL | cylinder |
| `Linear_Actuator_Y_Component18` | primitive STL | box |
| `Top_support` | primitive STL | box |
| `base_link` | primitive STL | box |

## Mesh Bake Offsets

Links where joint frame ≠ component origin. Visual/inertial/collision origins shifted.

| Link | Offset (mm) |
|------|-------------|
| `base_link` | (0.0, 0.0, 0.0) |
| `Linear_Actuator_X_edited_Component1` | (-26.4, -301.6, -50.7) |
| `Component7` | (0.0, -7.0, -181.9) |
| `Linear_Actuator_Y_Component1` | (-26.4, -301.6, -56.7) |
