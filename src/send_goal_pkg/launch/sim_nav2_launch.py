from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    SetEnvironmentVariable,
    IncludeLaunchDescription,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Declare launch arguments
    turtlebot3_model_arg = DeclareLaunchArgument(
        'turtlebot3_model',
        default_value='burger',
        description='TurtleBot3 model type (burger, waffle, waffle_pi)'
    )
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    # Launch configuration substitutions
    turtlebot3_model = LaunchConfiguration('turtlebot3_model')
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Set the TURTLEBOT3_MODEL environment variable
    set_env_var = SetEnvironmentVariable('TURTLEBOT3_MODEL', turtlebot3_model)

    # Launch Gazebo simulation
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_gazebo'),
                'launch',
                'turtlebot3_world.launch.py'
            ])
        ])
    )

    # Launch Nav2 stack
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_navigation2'),
                'launch',
                'navigation2.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time
        }.items()
    )

    # Launch custom goal sender
    send_goal_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('send_goal_pkg'),
                'launch',
                'send_goal_launch.py'
            ])
        ])
    )

    return LaunchDescription([
        turtlebot3_model_arg,
        use_sim_time_arg,
        set_env_var,
        gazebo_launch,
        nav2_launch,
        send_goal_launch,
    ])

