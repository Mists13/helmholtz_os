#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState


class JointRepublisher(Node):
    def __init__(self):
        super().__init__('joint_republisher')
        self.get_logger().info('joint_republisher started')

        # Publisher for JointState messages used by RViz / robot_state_publisher
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)

        # Subscribe to the controller command topic used by the demo
        self.sub = self.create_subscription(
            Float64MultiArray,
            '/forward_position_controller/commands',
            self.command_cb,
            10,
        )

        # Standard UR5 joint names
        self.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint',
        ]

    def command_cb(self, msg: Float64MultiArray):
        positions = list(msg.data)
        # Ensure length 6
        if len(positions) < 6:
            positions = positions + [0.0] * (6 - len(positions))
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = self.joint_names
        js.position = positions[:6]
        self.joint_pub.publish(js)


def main():
    rclpy.init()
    node = JointRepublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
