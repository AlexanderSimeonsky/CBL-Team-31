# **Technical reflection**

### Bidirectional Communication
Bidirectional Communication was achived only in the virtual environment for communcation between the system and virtual robot.
The robot provides the system with information such as its current position and speed which the system uses to estimate arrival time.
The system provides the robot with movement goals which it uses to navigate. We were not able to introduce bidirectional communication
between the physical and virtual robots. We encountered many problems with Unity and Docker which lead to us switching to Gazebo and VM. 
This had a massive impact on the project as when were did make the change we were able to make progress much faster. Other issues we 
encountered were with learning ROS2 and Python in a short period of time. We believe that given an additional 5-8 weeks we can fully satisfy
this characteristic of DTAS by having the physical robot send environmental data like new obstacles to simulate road closure to the DT
which will update its own environment so next time it generates a route it will take into account these new changes and avoid those obstacles
if necessary.

### State Synchronization
State Synchronization was achieved only in the virtual environment as the virtual robot follows the commands of the system. Again the progress for this
was impacted heavily by the same problems discussed in the previous section. If given additional time we believe we can meet this characteristic of DTAS,
but only after esablishing Bidirectional Communication. When that is established we will create scripts that synchronize the movement of both robots so 
that when one detects a new obstacle not present in the other's environment both robots will move to avoid it in the same way. 

### Environmental and Object Interaction
Environmental and Object Interaction was achieved in both environments, but without the robots' states being synchronized. Currently both robots will evade
obstacles when given movement goals and will navigate to their destination without issues, but they will avoid these obstacles in different ways due to us
not implenting state synchronization between both robots. We weren't able to record the physical robot performing that as we ran out of time in the last lab 
session. If given additional time we will be able to implement state synchronization and we will just need to do a final test to verify that no new issues 
have arisen with navigation.

#### **Lab Laptop Credentials**
**Username:** <br>
team31 <br>
**Password:** <br>
sieteamigos <br>
