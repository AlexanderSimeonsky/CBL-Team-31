import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose

class TurtlebotPoseListener(Node):
    def __init__(self):
        super().__init__('turtlebot_pose_listener')
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',  # or '/amcl_pose' if using localization
            self.odom_callback,
            10
        )
        self.subscription  # prevent unused variable warning

    def odom_callback(self, msg: Odometry):
        pose = msg.pose.pose
        position = pose.position
        orientation = pose.orientation
        self.get_logger().info(
            f"Position: x={position.x:.2f}, y={position.y:.2f}, z={position.z:.2f} | "
            f"Orientation: x={orientation.x:.2f}, y={orientation.y:.2f}, "
            f"z={orientation.z:.2f}, w={orientation.w:.2f}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = TurtlebotPoseListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

