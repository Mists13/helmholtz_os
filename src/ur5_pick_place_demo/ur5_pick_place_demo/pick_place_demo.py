#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time
import os

class PickPlaceDemo(Node):
    def __init__(self):
        super().__init__('pick_place_demo')
        self.get_logger().info('ur5_pick_place_demo started ✅')
        
        # Create publisher for joint commands
        self.joint_pub = self.create_publisher(
            Float64MultiArray,
            '/forward_position_controller/commands',
            10
        )
        
        # Control loop frequency (Hz)
        self.loop_frequency = 45
        self.timer = self.create_timer(
            1.0 / self.loop_frequency,
            self.control_loop
        )
        
        # Demo state
        self.step = 0
        self.max_steps = 480
        self.get_logger().info('Control loop initialized')
    
    def control_loop(self):
        """Main control loop for robot arm"""
        self.step += 1
        
        # Example: Move joints in a changing pattern
        joint_positions = self.get_target_positions()
        
        msg = Float64MultiArray()
        msg.data = joint_positions
        self.joint_pub.publish(msg)
        
        self.get_logger().debug(f'Step {self.step}: Positions = {joint_positions}')
        
        # Stop after max steps
        if self.step >= self.max_steps:
            self.get_logger().info('Demo completed!')
            # Write completion marker file
            with open('/tmp/pick_place_demo_complete.txt', 'w') as f:
                f.write(f'Completed at step {self.step}\n')
            self.timer.cancel()
    

    def get_target_positions(self):

        poses = [
            [0.0, -1.3, 1.6, -1.9, -1.57, 0.0],
            [0.0, -1.1, 1.9, -2.3, -1.57, 0.0],
            [0.0, -1.3, 1.6, -1.9, -1.57, 0.0],
            [1.2, -1.3, 1.6, -1.9, -1.57, 0.0],
            [1.2, -1.1, 1.9, -2.3, -1.57, 0.0],
            [1.2, -1.3, 1.6, -1.9, -1.57, 0.0],
        ]

        steps_per_motion = 80

        segment = self.step // steps_per_motion
        i0 = segment % len(poses)
        i1 = (i0 + 1) % len(poses)

        alpha = (self.step % steps_per_motion) / steps_per_motion

        p0 = poses[i0]
        p1 = poses[i1]

        target = [
            (1.0 - alpha) * a + alpha * b
            for a, b in zip(p0, p1)
        ]

        return target


def main():
    rclpy.init()
    node = PickPlaceDemo()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
