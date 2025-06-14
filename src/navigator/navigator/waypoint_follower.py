import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from math import sqrt

class Nav2WaypointFollower(Node):
    def __init__(self):
        super().__init__('nav2_waypoint_follower')

        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.path_sub = self.create_subscription(Path, '/digital_twin_path', self.path_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        self.waypoints = []
        self.current_goal_idx = 0
        self.goal_active = False
        self.current_pose = None
        self.current_speed = 0.0  # robot linear speed (m/s)
        self.eta_timer = self.create_timer(1.0, self.periodic_eta_log)  # 1 Hz periodic ETA log

    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose
        # Calculate linear speed magnitude from odom twist
        linear = msg.twist.twist.linear
        self.current_speed = sqrt(linear.x**2 + linear.y**2 + linear.z**2)

    def path_callback(self, msg):
        self.get_logger().info(f"Received path with {len(msg.poses)} waypoints")
        self.waypoints = msg.poses
        self.current_goal_idx = 0
        if not self.goal_active:
            self.send_next_goal()
        self.calculate_and_log_eta()

    def calculate_eta(self):
        if not self.current_pose or not self.waypoints:
            return None

        # Find closest waypoint index from current robot position
        min_dist = float('inf')
        closest_idx = 0
        robot_x = self.current_pose.position.x
        robot_y = self.current_pose.position.y

        for i, pose_stamped in enumerate(self.waypoints):
            wp = pose_stamped.pose.position
            dist = sqrt((wp.x - robot_x)**2 + (wp.y - robot_y)**2)
            if dist < min_dist:
                min_dist = dist
                closest_idx = i

        # Sum distances along remaining path to final waypoint
        distance_remaining = 0.0
        for i in range(closest_idx, len(self.waypoints)-1):
            p1 = self.waypoints[i].pose.position
            p2 = self.waypoints[i+1].pose.position
            distance_remaining += sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

        # Add distance from robot to closest waypoint
        distance_remaining += min_dist

        # Use current speed if > threshold, else fallback to default average speed
        min_speed = 0.05  # 5 cm/s minimum speed to avoid division by zero
        speed = self.current_speed if self.current_speed > min_speed else 0.2

        eta_sec = distance_remaining / speed

        return eta_sec

    def calculate_and_log_eta(self):
        eta = self.calculate_eta()
        if eta is not None:
            self.get_logger().info(f"Estimated time to final goal: {eta:.1f} seconds")

    def periodic_eta_log(self):
        # Called by timer at 1 Hz to log ETA while goal active
        if self.goal_active:
            eta = self.calculate_eta()
            if eta is not None:
                self.get_logger().info(f"[Periodic ETA] Estimated time to final goal: {eta:.1f} seconds")

    def send_next_goal(self):
        if self.current_goal_idx >= len(self.waypoints):
            self.get_logger().info("All waypoints reached")
            self.goal_active = False
            return

        goal_pose = self.waypoints[self.current_goal_idx]

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = goal_pose

        self.get_logger().info(f"Sending goal {self.current_goal_idx + 1}/{len(self.waypoints)}: ({goal_pose.pose.position.x:.2f}, {goal_pose.pose.position.y:.2f})")

        self.action_client.wait_for_server()

        self.goal_active = True
        self._send_goal_future = self.action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn("Goal rejected!")
            self.goal_active = False
            return

        self.get_logger().info("Goal accepted.")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == 4:  # ABORTED
            self.get_logger().warn("Goal was aborted")
            self.goal_active = False
            return

        if status == 5:  # REJECTED
            self.get_logger().warn("Goal was rejected")
            self.goal_active = False
            return

        self.get_logger().info(f"Goal {self.current_goal_idx + 1} reached!")

        self.current_goal_idx += 1
        self.goal_active = False

        # Send the next goal after the current is reached
        self.send_next_goal()

def main(args=None):
    rclpy.init(args=args)
    node = Nav2WaypointFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

