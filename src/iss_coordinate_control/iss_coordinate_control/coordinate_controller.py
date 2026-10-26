
"""Sequential RViz-only motion controller for the ISS gantry."""

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray


class ISSCoordinateController(Node):
    """Move the three independent gantry joints sequentially."""

    JOINTS = (
        "Top_Slider",
        "Slider_2",
        "Slider_2_1",
        "Slider_3",
    )

    # Ordered motion stages: first, second, third actuator.
    # Cartesian XYZ mapping has not yet been calibrated.
    MOTION_JOINTS = (
        "Slider_2",
        "Slider_2_1",
        "Slider_3",
    )

    # Actual limits from the existing URDF, in meters.
    LIMITS = {
        "Top_Slider": (-0.630, 0.310),
        "Slider_2": (-0.630, 0.310),
        "Slider_2_1": (-0.650, 0.200),
        "Slider_3": (-0.057, 0.0025),
    }

    def __init__(self):
        super().__init__("iss_coordinate_controller")

        # RViz-only simulated joint positions.
        self.positions = {
            joint: 0.0 for joint in self.JOINTS
        }

        self.target_positions = self.positions.copy()

        # Sequential movement settings.
        self.axis_index = 0
        self.axis_start = 0.0
        self.elapsed = 0.0

        self.period = 0.05
        self.axis_duration = 2.0
        self.tolerance = 0.0001
        self.moving = False

        # Publish joint states for robot_state_publisher and RViz.
        self.publisher = self.create_publisher(
            JointState,
            "/joint_states",
            10,
        )

        # Receive joint position commands.
        self.subscription = self.create_subscription(
            Float64MultiArray,
            "/iss_joint_targets",
            self.target_callback,
            10,
        )

        # Update movement 20 times per second.
        self.timer = self.create_timer(
            self.period,
            self.update_motion,
        )

        self.get_logger().info(
            "ISS sequential joint controller ready"
        )

    def target_callback(self, msg):
        """Validate and accept a new joint target."""

        if self.moving:
            self.get_logger().warning(
                "Controller busy: finish current goal first"
            )
            return

        # Command format:
        # [Top_Slider, Slider_2, Slider_2_1, Slider_3]
        #
        # Top_Slider is a mimic of Slider_2.
        # Its supplied command value is ignored.

        if len(msg.data) != 4:
            self.get_logger().error(
                "Expected four joint values: "
                "[Top_Slider, Slider_2, Slider_2_1, Slider_3]"
            )
            return

        if not all(math.isfinite(v) for v in msg.data):
            self.get_logger().error(
                "Rejected non-finite joint target"
            )
            return

        _, slider_2, slider_2_1, slider_3 = msg.data

        requested = {
            "Top_Slider": slider_2,
            "Slider_2": slider_2,
            "Slider_2_1": slider_2_1,
            "Slider_3": slider_3,
        }

        # Enforce the real URDF travel limits.
        for joint, value in requested.items():
            lower, upper = self.LIMITS[joint]

            if not lower <= value <= upper:
                self.get_logger().error(
                    f"{joint}: target {value:.4f} m "
                    f"outside limits [{lower}, {upper}]"
                )
                return

        self.target_positions = requested

        # Start with the first independent joint.
        self.axis_index = 0
        self.elapsed = 0.0
        self.moving = True

        first_joint = self.MOTION_JOINTS[0]
        self.axis_start = self.positions[first_joint]

        self.get_logger().info(
            f"Accepted target: {requested}"
        )

        self.get_logger().info(
            f"Starting axis 1/3: {first_joint}"
        )

    def update_motion(self):
        """Move one joint at a time and publish joint states."""

        if self.moving:
            joint = self.MOTION_JOINTS[self.axis_index]

            self.elapsed += self.period

            # Normalize time from 0.0 to 1.0.
            t = min(
                self.elapsed / self.axis_duration,
                1.0,
            )

            # Smoothstep interpolation:
            # movement starts and stops smoothly.
            blend = t * t * (3.0 - 2.0 * t)

            start = self.axis_start
            target = self.target_positions[joint]

            self.positions[joint] = (
                start + blend * (target - start)
            )

            # Top_Slider must follow Slider_2.
            self.positions["Top_Slider"] = (
                self.positions["Slider_2"]
            )

            # Compare simulated position with target.
            error = abs(self.positions[joint] - target)

            if t >= 1.0:
                if error <= self.tolerance:
                    self.get_logger().info(
                        f"{joint} reached target: "
                        f"{self.positions[joint]:.4f} m"
                    )

                    # Advance to the next joint.
                    self.axis_index += 1

                    if self.axis_index >= len(
                        self.MOTION_JOINTS
                    ):
                        self.moving = False

                        self.get_logger().info(
                            "All three simulated axes completed"
                        )

                    else:
                        next_joint = self.MOTION_JOINTS[
                            self.axis_index
                        ]

                        self.axis_start = self.positions[
                            next_joint
                        ]

                        self.elapsed = 0.0

                        self.get_logger().info(
                            f"Starting axis "
                            f"{self.axis_index + 1}/3: "
                            f"{next_joint}"
                        )

                else:
                    self.moving = False

                    self.get_logger().error(
                        f"{joint} failed simulated "
                        f"position verification"
                    )

        # Publish all joint positions every timer cycle.
        message = JointState()

        message.header.stamp = (
            self.get_clock().now().to_msg()
        )

        message.name = list(self.JOINTS)

        message.position = [
            self.positions[joint]
            for joint in self.JOINTS
        ]

        self.publisher.publish(message)


def main(args=None):
    rclpy.init(args=args)

    node = ISSCoordinateController()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
