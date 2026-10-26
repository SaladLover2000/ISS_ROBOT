
"""RViz-only joint-position controller for the ISS gantry."""

import math

import rclpy
from sensor_msgs.msg import JointState

from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray


class ISSCoordinateController(Node):
    """Interpolate gantry joints for visualization in RViz."""

    JOINTS = (
        "Top_Slider",
        "Slider_2",
        "Slider_2_1",
        "Slider_3",
    )

    LIMITS = {
        "Top_Slider": (-0.630, 0.310),
        "Slider_2": (-0.630, 0.310),
        "Slider_2_1": (-0.650, 0.200),
        "Slider_3": (-0.057, 0.0025),
    }

    def __init__(self):
        super().__init__("iss_coordinate_controller")

        self.positions = {
            joint: 0.0 for joint in self.JOINTS
        }

        self.start_positions = self.positions.copy()
        self.target_positions = self.positions.copy()

        self.duration = 3.0
        self.elapsed = 0.0
        self.period = 0.05
        self.moving = False

        self.publisher = self.create_publisher(
            JointState,
            "/joint_states",
            10,
        )

        self.subscription = self.create_subscription(
            Float64MultiArray,
            "/iss_joint_targets",
            self.target_callback,
            10,
        )

        self.timer = self.create_timer(
            self.period,
            self.update_motion,
        )

        self.get_logger().info(
            "ISS RViz coordinate controller ready"
        )

    def target_callback(self, msg):
        """Receive a bounded joint-position target."""

        # Four values are accepted for compatibility with
        # the original command interface.
        #
        # Order:
        # [Top_Slider, Slider_2, Slider_2_1, Slider_3]
        #
        # The first value is not independently controlled.
        # Top_Slider follows Slider_2 via URDF mimic.

        if len(msg.data) != 4:
            self.get_logger().error(
                "Expected four joint values"
            )
            return

        if not all(math.isfinite(v) for v in msg.data):
            self.get_logger().error(
                "Non-finite joint target rejected"
            )
            return

        _, slider_2, slider_2_1, slider_3 = msg.data

        requested = {
            "Top_Slider": slider_2,
            "Slider_2": slider_2,
            "Slider_2_1": slider_2_1,
            "Slider_3": slider_3,
        }

        for joint, value in requested.items():
            lower, upper = self.LIMITS[joint]

            if not lower <= value <= upper:
                self.get_logger().error(
                    f"{joint} target outside URDF limits"
                )
                return

        self.start_positions = self.positions.copy()
        self.target_positions = requested

        self.elapsed = 0.0
        self.moving = True

        self.get_logger().info(
            f"Accepted target: {requested}"
        )

    def update_motion(self):
        """Publish the current interpolated joint positions."""

        if self.moving:
            self.elapsed += self.period

            t = min(self.elapsed / self.duration, 1.0)

            # Smoothstep interpolation:
            # zero slope at start and finish.
            blend = t * t * (3.0 - 2.0 * t)

            for joint in self.JOINTS:
                start = self.start_positions[joint]
                target = self.target_positions[joint]

                self.positions[joint] = (
                    start + blend * (target - start)
                )

            if t >= 1.0:
                self.moving = False
                self.get_logger().info(
                    "Joint target reached in RViz simulation"
                )

        message = JointState()
        message.header.stamp = self.get_clock().now().to_msg()
        message.name = list(self.JOINTS)
        message.position = [
            self.positions[joint] for joint in self.JOINTS
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
