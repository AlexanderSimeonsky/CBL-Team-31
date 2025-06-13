commands to run current implementation

source install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

#on new terminal window
source install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True

#on new terminal window
source install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch send_goal_pkg send_goal_launch.py

#on new terminal window
source install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 run send_goal_pkg publish_goal
