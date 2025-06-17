import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from tf_transformations import quaternion_from_euler
import time

class GoalPublisher(Node):
    def __init__(self):
        super().__init__('goal_publisher')
        self.publisher = self.create_publisher(PoseStamped, '/single_goal_pose', 10)
        self.timer = self.create_timer(2.0, self.publish_goal_once)
        self.sent = False

    def publish_goal_once(self):
        if self.sent:
            return

        goal = PoseStamped()
        goal.header.frame_id = "map"
        goal.header.stamp = self.get_clock().now().to_msg()

        
        goal.pose.position.x = 1.5
        goal.pose.position.y = -0.5
        goal.pose.position.z = 0.0

        
        q = quaternion_from_euler(0, 0, 0)
        goal.pose.orientation.x = q[0]
        goal.pose.orientation.y = q[1]
        goal.pose.orientation.z = q[2]
        goal.pose.orientation.w = q[3]

        self.publisher.publish(goal)
        self.get_logger().info('Published goal to /goal_pose')
        self.sent = True

def main(args=None):
    rclpy.init(args=args)
    node = GoalPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
