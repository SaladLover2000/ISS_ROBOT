# ROS export repair — 2026-10-25

This is a **post-export kinematic workaround**. No Fusion 360 files or meshes were changed.

## Change

`Slider_2_1` has been reparented from `Linear_Actuator_X_edited_Component18` to `Linear_Actuator_Y_Component18`. Its joint origin was transformed into the new parent's frame, preserving the original child pose at the reference joint position and the joint-axis orientation in the reference world frame. The new X-motion dependency now propagates through the Y actuator housing to the Y carriage.

Updated files: `urdf/SimofRack_onlylinear.urdf`, `urdf/SimofRack_onlylinear.urdf.xacro`, `robot_data.yaml`. Other joints, limits, meshes, and controllers were not edited.

## Checks performed

- XML parsed successfully.
- Exactly 8 links and 7 joints; all links reachable from `base_link` and every nonroot link has exactly one parent.
- 4x4 transform composition confirms that the Y carriage's pose relative to the original X housing is preserved at q=0 (before and after reparenting).
- Joint-axis orientation preserved at reference pose.

## Not yet tested

ROS/RViz and simulation have **not** been run here. Compare zero positions and slider motion in RViz. Note that the original exported limits for `Slider_2_1` are [-0.85, -0.01] m, so 0 is outside those limits; these were preserved unchanged. The separate `Top_Slider` fallback-frame warning and closing-joint sidecar are unchanged.

This edit may be overwritten if you rerun Fusion2URDF; apply to new exports only after re-verifying their joint trees.
