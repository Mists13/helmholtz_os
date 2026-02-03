import rclpy
from rclpy.node import Node

from visualization_msgs.msg import Marker
from std_msgs.msg import Bool

import tf2_ros
import math


class SceneObjectPublisher(Node):

    def __init__(self):
        super().__init__("scene_object_publisher")

        self.pub = self.create_publisher(Marker, "/scene_object", 1)

        self.sub = self.create_subscription(
            Bool,
            "/grasped",
            self.grasp_cb,
            10
        )

        self.timer = self.create_timer(0.05, self.publish_object)

        self.want_attach = False
        self.attached = False

        self.ee_frame = "link6"
        self.base_frame = "base_link"

        # cube initial position in base frame
        self.obj_x = 0.45
        self.obj_y = 0.0
        self.obj_z = 0.05
        self.step_counter = 0

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.attach_distance = 0.06  # meters

    def grasp_cb(self, msg):
        self.want_attach = msg.data

    def publish_object(self):
        self.step_counter += 1

        marker = Marker()
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "pick_object"
        marker.id = 0
        marker.type = Marker.CUBE
        marker.action = Marker.ADD

        marker.scale.x = 0.05
        marker.scale.y = 0.05
        marker.scale.z = 0.05

        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        # -----------------------------
        # decide if we attach
        # -----------------------------
        if self.want_attach and not self.attached:

            try:
                t = self.tf_buffer.lookup_transform(
                    self.base_frame,
                    self.ee_frame,
                    rclpy.time.Time()
                )

                dx = t.transform.translation.x - self.obj_x
                dy = t.transform.translation.y - self.obj_y
                dz = t.transform.translation.z - self.obj_z

                dist = math.sqrt(dx*dx + dy*dy + dz*dz)

                if self.step_counter % 20 == 0:
                    print(f"DEBUG: Distance to object: {dist}, want_attach: {self.want_attach}")

                if dist < self.attach_distance:
                    self.attached = True

            except Exception:
                pass

        # -----------------------------
        # publish cube
        # -----------------------------
        if not self.attached:

            marker.header.frame_id = self.base_frame

            marker.pose.position.x = self.obj_x
            marker.pose.position.y = self.obj_y
            marker.pose.position.z = self.obj_z
            marker.pose.orientation.w = 1.0

        else:
            print("Object attached to end-effector")
            marker.header.frame_id = self.ee_frame

            marker.pose.position.x = 0.0
            marker.pose.position.y = 0.0
            marker.pose.position.z = 0.08
            marker.pose.orientation.w = 1.0

        self.pub.publish(marker)


def main():
    rclpy.init()
    node = SceneObjectPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
