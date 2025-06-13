import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient


class GoalReceiverNode(Node):
    def __init__(self):
        super().__init__('goal_receiver_node')
        self.subscriber = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.goal_callback,
            10
        )
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.get_logger().info('GoalReceiverNode is ready and listening to /goal_pose')

    def goal_callback(self, msg: PoseStamped):
        self.get_logger().info(f"Received goal: x={msg.pose.position.x}, y={msg.pose.position.y}")
        self.send_goal(msg)

    def send_goal(self, pose: PoseStamped):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose

        self._action_client.wait_for_server()
        send_goal_future = self._action_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn('Goal was rejected by the action server.')
            return

        self.get_logger().info('Goal accepted. Waiting for result...')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f"Goal result received. Result code: {result}")
        # Optional: Add logic based on result.status if needed


def main(args=None):
    rclpy.init(args=args)
    node = GoalReceiverNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

