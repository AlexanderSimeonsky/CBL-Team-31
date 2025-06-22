```bash
# commands to run current implementation  

# launch file to do steps 1-3 simultaniously (might cause issue for some reason)
source install/setup.bash  
ros2 launch send_goal_pkg full_sim_nav2_launch.py

# 1
source install/setup.bash  
export TURTLEBOT3_MODEL=burger  
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py  

# 2 on new terminal window  
source install/setup.bash  
export TURTLEBOT3_MODEL=burger  
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True  

# 3 on new terminal window  
source install/setup.bash  
export TURTLEBOT3_MODEL=burger  
ros2 launch send_goal_pkg send_goal_launch.py

# 4 on new terminal window 
source install/setup.bash  
export TURTLEBOT3_MODEL=burger
ros2 run navigator waypoint_follower

# 5 on new terminal window 
source install/setup.bash  
export TURTLEBOT3_MODEL=burger
ros2 run send_goal_pkg publish_goal
