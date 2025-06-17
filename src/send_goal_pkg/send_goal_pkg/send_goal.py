import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient


class DynamicGoalNav(Node):
    def __init__(self):
        super().__init__('dynamic_goal_nav')
        self.subscription = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.goal_callback,
            10
        )
        self.nav_action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.get_logger().info('Node ready, waiting for goals on /goal_pose...')

    def goal_callback(self, msg: PoseStamped):
        self.get_logger().info(f"Received goal: x={msg.pose.position.x}, y={msg.pose.position.y}")
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = msg

        
        self.nav_action_client.wait_for_server()
        self.send_goal(goal_msg)

    def send_goal(self, goal_msg):
        self.get_logger().info('Sending goal to NavigateToPose action server...')
        send_goal_future = self.nav_action_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn('Goal rejected by server.')
            return

        self.get_logger().info('Goal accepted. Waiting for result...')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Navigation result: {result}')


def main(args=None):
    rclpy.init(args=args)
    node = DynamicGoalNav()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

