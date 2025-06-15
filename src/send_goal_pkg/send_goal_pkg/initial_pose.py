import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped

class InitialPosePublisher(Node):
    def __init__(self):
        super().__init__('initial_pose_publisher')
        self.publisher = self.create_publisher(PoseWithCovarianceStamped, 'initialpose', 10)
        # Publish once after a short delay (e.g., 1 second)
        self.timer = self.create_timer(1.0, self.publish_initial_pose)
        self.published = False

    def publish_initial_pose(self):
        if not self.published:
            msg = PoseWithCovarianceStamped()
            msg.header.frame_id = 'map'
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.pose.pose.position.x = -2.0
            msg.pose.pose.position.y = -0.5
            msg.pose.pose.position.z = 0.1
            msg.pose.pose.orientation.x = 0.0
            msg.pose.pose.orientation.y = 0.0
            msg.pose.pose.orientation.z = 0.0
            msg.pose.pose.orientation.w = 1.0
            msg.pose.covariance = [0.0]*36
            self.publisher.publish(msg)
            self.get_logger().info('Published initial pose: x=-2.0, y=-0.5, z=0.1')
            self.published = True
            self.timer.cancel()  # stop the timer after publishing once


def main(args=None):
    rclpy.init(args=args)
    node = InitialPosePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

