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
        self.loop_frequency = 10
        self.timer = self.create_timer(
            1.0 / self.loop_frequency,
            self.control_loop
        )
        
        # Demo state
        self.step = 0
        self.max_steps = 50
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
        """Generate target joint positions for UR5 (6 joints)"""
        # Sinusoidal motion for smooth changes
        amplitude = 0.5
        progress = self.step / self.max_steps
        
        # Simple sinusoidal pattern for each joint
        positions = [
            amplitude * __import__('math').sin(progress * 4 * 3.14159),  # Joint 1
            amplitude * __import__('math').cos(progress * 4 * 3.14159),  # Joint 2
            amplitude * __import__('math').sin(progress * 2 * 3.14159),  # Joint 3
            amplitude * __import__('math').cos(progress * 3 * 3.14159),  # Joint 4
            amplitude * __import__('math').sin(progress * 5 * 3.14159),  # Joint 5
            amplitude * __import__('math').cos(progress * 2 * 3.14159),  # Joint 6
        ]
        
        return positions

def main():
    rclpy.init()
    node = PickPlaceDemo()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
