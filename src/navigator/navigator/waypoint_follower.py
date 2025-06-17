import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path, Odometry
from std_msgs.msg import String
from math import sqrt


class Nav2WaypointFollower(Node):
    def __init__(self):
        super().__init__('nav2_waypoint_follower')

        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        self.path_sub = self.create_subscription(Path, '/digital_twin_path', self.path_callback, 10)
        self.pose_sub = self.create_subscription(PoseStamped, '/single_goal_pose', self.pose_callback, 10)
        self.next_goal_sub = self.create_subscription(PoseStamped, '/next_goal_point', self.waypoint_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        self.goal_done_pub = self.create_publisher(String, '/goal_status', 10)

        self.waypoints = []
        self.current_goal_idx = 0
        self.goal_active = False
        self.can_send_next_goal = True   # <-- New flag to control sending
        self.current_pose = None
        self.current_speed = 0.0
        self.eta_timer = self.create_timer(1.0, self.periodic_eta_log)

    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose
        linear = msg.twist.twist.linear
        self.current_speed = sqrt(linear.x ** 2 + linear.y ** 2 + linear.z ** 2)

    def path_callback(self, msg):
        self.get_logger().info(f"Received path with {len(msg.poses)} waypoints")
        self.waypoints = msg.poses
        self.current_goal_idx = 0
        if self.can_send_next_goal and not self.goal_active:
            self.send_next_goal()
        self.calculate_and_log_eta()

    def pose_callback(self, msg):
        self.get_logger().info("Received single pose goal")
        self.waypoints = [msg]
        self.current_goal_idx = 0
        if self.can_send_next_goal and not self.goal_active:
            self.send_next_goal()
        self.calculate_and_log_eta()

    def waypoint_callback(self, msg: PoseStamped):
        self.get_logger().info(f"Received next goal point: ({msg.pose.position.x}, {msg.pose.position.y})")
        self.waypoints.append(msg)
        self.calculate_and_log_eta()
        if self.can_send_next_goal and not self.goal_active:
            self.send_next_goal()

    def calculate_eta(self):
        if not self.current_pose or not self.waypoints:
            return None

        min_dist = float('inf')
        closest_idx = 0
        robot_x = self.current_pose.position.x
        robot_y = self.current_pose.position.y

        for i, pose_stamped in enumerate(self.waypoints):
            wp = pose_stamped.pose.position
            dist = sqrt((wp.x - robot_x) ** 2 + (wp.y - robot_y) ** 2)
            if dist < min_dist:
                min_dist = dist
                closest_idx = i

        distance_remaining = 0.0
        for i in range(closest_idx, len(self.waypoints) - 1):
            p1 = self.waypoints[i].pose.position
            p2 = self.waypoints[i + 1].pose.position
            distance_remaining += sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

        distance_remaining += min_dist
        min_speed = 0.05
        speed = self.current_speed if self.current_speed > min_speed else 0.2
        return distance_remaining / speed

    def calculate_and_log_eta(self):
        eta = self.calculate_eta()
        if eta is not None:
            self.get_logger().info(f"Estimated time to final goal: {eta:.1f} seconds")

    def periodic_eta_log(self):
        if self.goal_active:
            eta = self.calculate_eta()
            if eta is not None:
                self.get_logger().info(f"[Periodic ETA] Estimated time to final goal: {eta:.1f} seconds")

    def send_next_goal(self):
        if not self.can_send_next_goal:
            self.get_logger().info("Waiting to send next goal, send blocked")
            return

        if not self.waypoints:
            self.get_logger().info("No waypoints available yet, waiting...")
            self.goal_active = False
            return

        if self.current_goal_idx >= len(self.waypoints):
            self.get_logger().info("All waypoints reached")
            done_msg = String()
            done_msg.data = "All waypoints reached"
            self.goal_done_pub.publish(done_msg)
            self.goal_active = False
            return

        goal_pose = self.waypoints[self.current_goal_idx]
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = goal_pose

        self.get_logger().info(
            f"Sending goal {self.current_goal_idx + 1}/{len(self.waypoints)}: "
            f"({goal_pose.pose.position.x:.2f}, {goal_pose.pose.position.y:.2f})"
        )

        self.action_client.wait_for_server()
        self.goal_active = True
        self.can_send_next_goal = False  # Block sending next goal until current finishes
        self._send_goal_future = self.action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn("Goal rejected!")
            self.goal_active = False
            self.can_send_next_goal = True
            return

        self.get_logger().info("Goal accepted.")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == 3 or status == 5:  # SUCCEEDED or ABORTED
            if status == 3:
                self.get_logger().info(f"Goal {self.current_goal_idx + 1} reached!")
            else:
                self.get_logger().warn(f"Goal {self.current_goal_idx + 1} aborted, moving to next goal")

            done_msg = String()
            done_msg.data = f"Goal {self.current_goal_idx + 1} {'reached' if status == 3 else 'aborted'}"
            self.goal_done_pub.publish(done_msg)

            self.current_goal_idx += 1
            self.goal_active = False
            self.can_send_next_goal = True  # Allow sending next goal now
            self.send_next_goal()

        elif status == 6:  # REJECTED
            self.get_logger().warn("Goal was rejected")
            self.goal_active = False
            self.can_send_next_goal = True

        else:
            self.get_logger().warn(f"Goal ended with unexpected status: {status}")
            self.goal_active = False
            self.can_send_next_goal = True


def main(args=None):
    rclpy.init(args=args)
    node = Nav2WaypointFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

