# **Technical reflection**

### Bidirectional Communication
We only managed to achieve bidirectional communication between the system and the virtual simulation of the robot. The robot provides the system with information such as its current position and speed (odometry) which the system uses to estimate the arrival time.The system provides the robot with movement goals which it uses to navigate. 

We encountered many problems with Unity and Docker, like the Unity URDF and the different documentation used in Docker (Humble) compared to the one emphasized by the course (Foxy), which led us to switching to Gazebo and VM. This had a massive impact on the project as when we did make the change we were able to make progress much faster. Other issues we encountered were learning the ROS2 libraries and how to use them in Python/Unity in a short period of time. Because the course emphasized more on both the documentation and final presentation in the first 5-6 weeks  if we had some extra time we believe we could fully satisfy this characteristic of DTAS by having the physical robot send environmental data like new obstacles to simulate road closure to the DT which will update its own environment so next time it generates a route it will take into account these new changes and avoid those obstacles if necessary.


### State Synchronization
State Synchronization was achieved only in the virtual environment as the virtual robot follows the commands of the system. If given additional time in the labsessions we believe we could have met this characteristic of DTAS, but only after establishing Bidirectional Communication. After that was established we would have created scripts that synchronize the movement of both robots so that when one detects a new obstacle not present in the other's environment both robots will move to avoid it in the same way.

### Environmental and Object Interaction
Environmental and Object Interaction was achieved in both environments, but without the robots' states being synchronized. Currently both robots will evade obstacles when given movement goals and will navigate to their destination without issues, but they will avoid these obstacles in different ways due to us not implementing state synchronization between both robots. We weren't able to record the physical robot performing that, because we ran out of time in the last lab session. If given additional time we will be able to implement state synchronization and we will just need to do a final test to verify that no new issues have arisen with navigation.

#### **Lab Laptop Credentials**
**Username:** <br>
team31 <br>
**Password:** <br>
sieteamigos <br>
