import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

class DigitalTwinNode(Node):
    def __init__(self):
        super().__init__('digital_twin_node')
        self.publisher = self.create_publisher(Path, '/digital_twin_path', 10)
        self.last_path = None
        self.timer = self.create_timer(5.0, self.publish_path)

    def publish_path(self):
        points = [
            #(0.0, 0.0),
            (1.0, -0.5),
            (-1.0, -0.5),
            #(3.0, 1.5),
            #(4.0, 2.0),
        ]

        if self.last_path == points:
            return  

        path = Path()
        path.header.frame_id = "map"
        path.header.stamp = self.get_clock().now().to_msg()

        for x, y in points:
            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.header.stamp = self.get_clock().now().to_msg()
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.orientation.w = 1.0
            path.poses.append(pose)

        self.publisher.publish(path)
        self.get_logger().info(f"Published path with {len(points)} waypoints")
        self.last_path = points
def main(args=None):
    rclpy.init(args=args)
    node = DigitalTwinNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
