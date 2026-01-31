import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker


class SceneObjectPublisher(Node):

    def __init__(self):
        super().__init__("scene_object_publisher")

        self.pub = self.create_publisher(Marker, "/scene_object", 1)

        self.timer = self.create_timer(0.05, self.publish_object)

        self.start_time = self.get_clock().now()
        self.attached = False

        self.ee_frame = "link6"

    def publish_object(self):

        now = self.get_clock().now()

        # Attach after 4 seconds (fake "pick")
        if (now - self.start_time).nanoseconds * 1e-9 > 4.0:
            self.attached = True

        marker = Marker()

        marker.header.stamp = now.to_msg()

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

        if not self.attached:
            # ---- cube on the table (world / base frame)
            marker.header.frame_id = "base_link"

            marker.pose.position.x = 0.45
            marker.pose.position.y = 0.0
            marker.pose.position.z = 0.05

            marker.pose.orientation.w = 1.0

        else:
            # ---- cube follows the gripper
            marker.header.frame_id = self.ee_frame

            # small offset in the gripper frame
            marker.pose.position.x = 0.0
            marker.pose.position.y = 0.0
            marker.pose.position.z = 0.05

            marker.pose.orientation.w = 1.0

        self.pub.publish(marker)


def main():
    rclpy.init()
    node = SceneObjectPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
