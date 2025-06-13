import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, NavigationResult

class GoalReceiverNode(Node):
    def __init__(self):
        super().__init__('goal_receiver_node')

        # Start Nav2 interface
        self.navigator = BasicNavigator()

        # Subscribe to the Unity goal topic
        self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.goal_callback,
            10
        )

        self.get_logger().info("GoalReceiverNode is ready and listening to /goal_pose")

    def goal_callback(self, msg: PoseStamped):
        self.get_logger().info(f"Received goal at ({msg.pose.position.x:.2f}, {msg.pose.position.y:.2f})")

        # Send goal to Nav2
        self.navigator.goToPose(msg)

        # Wait for result (optional)
        result = self.navigator.getResult()
        if result == NavigationResult.SUCCEEDED:
            self.get_logger().info("Goal reached successfully.")
        elif result == NavigationResult.CANCELED:
            self.get_logger().warn("Goal was canceled.")
        else:
            self.get_logger().error("Goal failed!")

def main(args=None):
    rclpy.init(args=args)
    node = GoalReceiverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

