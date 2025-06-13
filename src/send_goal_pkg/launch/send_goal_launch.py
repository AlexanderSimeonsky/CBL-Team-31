from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='send_goal_pkg',
            executable='initial_pose',
            name='initial_pose_publisher',
            output='screen'
        ),
        Node(
            package='send_goal_pkg',
            executable='send_goal',
            name='send_goal_node',
            output='screen'
        )
    ])
