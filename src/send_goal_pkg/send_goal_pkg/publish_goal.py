import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String


class GoalPublisher(Node):
    def __init__(self):
        super().__init__('goal_publisher')

        self.publisher = self.create_publisher(PoseStamped, '/next_goal_point', 10)
        self.status_sub = self.create_subscription(String, '/goal_status', self.status_callback, 10)

        self.goals = []
        self.current_goal_idx = 0
        self._populate_goals()

        self.publish_next_goal()

        self.timer = None

    def _populate_goals(self):
        goals_data = [
            (0.81, -0.57, 0.0),
            (0.66, 2.0, 0.0),
            (-0.6, 0.5, 0.0),  
        ]
        for x, y, z in goals_data:
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.position.z = z
            pose.pose.orientation.x = 0.0
            pose.pose.orientation.y = 0.0
            pose.pose.orientation.z = 0.0
            pose.pose.orientation.w = 1.0
            self.goals.append(pose)

    def publish_next_goal(self):
        if self.current_goal_idx >= len(self.goals):
            self.get_logger().info("All goals sent and confirmed.")
            return

        goal = self.goals[self.current_goal_idx]
        goal.header.stamp = self.get_clock().now().to_msg()
        self.publisher.publish(goal)
        self.get_logger().info(
            f"Published goal {self.current_goal_idx + 1}/{len(self.goals)} "
            f"to /next_goal_point: ({goal.pose.position.x}, {goal.pose.position.y})"
        )

    def status_callback(self, msg: String):
        self.get_logger().info(f"Received status: {msg.data}")

        # Only proceed if previous goal was reached successfully
        if "reached" in msg.data.lower():
            self.current_goal_idx += 1
            if self.timer is None:
                self.timer = self.create_timer(0.2, self.publish_next_goal_once)

    def publish_next_goal_once(self):
        self.publish_next_goal()
        if self.timer:
            self.timer.cancel()
            self.timer = None


def main(args=None):
    rclpy.init(args=args)
    node = GoalPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

