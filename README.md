# Online Path Planning ROS Package
(Collaborators: Tanakrit Lertcompeesin and Samantha Caballero)

## Running the Simulation

To run the simulation using the provided commands, follow these steps:

1. Launch the Gazebo and turtlebot:
   ```bash
   roslaunch turtlebot_online_path_planning gazebo.launch
   ```
    This command will start the Gazebo simulation with the Turtlebot model.



2. In seperated window, run turtlebot_online_path_planning_node:
   ```bash
   rosrun turtlebot_online_path_planning turtlebot_online_path_planning_node.py
   ```
    This command will execute the node responsible for the online path planning process.

3. On RVIZ -> click on 2D Nav Goal. 
This will call the topic: move_base_simple/goal
It will send a goal to the navigation by setting a desired pose for the robot to achieve. 


## Overview

This ROS package implements an online path planning algorithm for robotic navigation. It comprises three main modules: `StateValidityChecker`, `Planner`, and `Controller`. These modules are utilized by the `turtlebot_online_path_planning_node.py` script to generate a sequence of online path planning actions. Additionally, this script manages the connection between the Turtlebot in the Gazebo simulation environment via ROS.

To simplified the sequences, the online path planning process can be depicted as a state machine with the following states:

1. **IDLE State:** The robot waits in the IDLE state until it receives a goal.
2. **Planning State:** Upon receiving a goal, the robot transitions to the Planning state, where the Planner module calculates a path to the goal.
3. **Move to Goal State:** Once a valid path is computed, the robot transitions to the Move to Goal state. Here, the Controller module determines the velocity commands required for the robot to follow the planned path and publishes them to the `/cmd_vel` topic. As the map progress by updating through the new gridmap from `OctoMapServer` node, the validity of the current path is continuously checked by utilizing `check_path()`. If the path becomes invalid due to changes in the environment, the robot returns to the Planning state to recalculate the path.
5. **Recovery State:** If the robot becomes stuck due to obstacles, it enters the Recovery state before planning a new path. The robot ensures its current position's validity by utilizing the `is_valid()` function from the StateValidityChecker module. The recovery action persists until the robot is no longer stuck.

The algorithm flow and the connection to other ROS nodes are illustrated in the figure below.

  ![Online Path Planning Overview](imgs/HOP_lab1_overview.jpg)


## Publishers

1. **Command Velocity (`/cmd_vel`):** Sends velocity commands for robot movement. 

2. **Path Visualization (`/turtlebot_online_path_planning/path_marker`):** Visualizes planned paths in RViz.

3. **Waypoints Visualization (`/turtlebot_online_path_planning/waypoints_marker`):** Visualizes waypoints in RViz.

## Subscribers

1. **Grid Map (`/projected_map`):** Receives grid map data from Octomap Server. 

2. **Odometry (`/odom`):** Subscribes to odometry data for path planning. 

3. **Goal (`/move_base_simple/goal`):** Subscribes to move goals for path planning.




## Modifications 
### Path Planning with RRT Algorithm

In the planning module, we've implemented the Rapidly-exploring Random Tree (RRT) algorithm. While the core principles of RRT are followed, we've made modifications in how we verify the validity of the tree's segments.

Previously, we access the configuration space directly. Now, we've integrated the StateValidityChecker module, specifically utilizing its `check_path()` function for validation.

Moreover, to adapt to various scenarios, several parameters are adjustable:

- **`max_time`:** Maximum execution time before returning a failure.
- **`delta_q`:** Maximum distance between nodes.
- **`p_goal`:** Probability of selecting a goal point.
- **`dominion`:** Position limit of the node; nodes cannot be generated outside this boundary.


### Recovery Behavior
For the recovery behavior, it executes before planning if the current pose is not valid, indicating that the robot is too close to an obstacle and unable to plan a path effectively.
![Recovery Behavior](imgs/recovery.gif)
The implemented behavior is straightforward: assuming that the robot will collide with the obstacle if it faces it directly, the recovery behavior consists of moving the robot backward at a constant velocity until the current pose is valid again. This ensures that the robot retreats from the obstacle and able to plan the path.
  
### Path Visualization
Previously, the path visualization was published only once upon finishing computation, which was insufficient to represent the current path adequately. Therefore, it has been modified to be published every 2 seconds.

![Path and Waypoint Visualization](imgs/wp_path.png)

Additionally, waypoint visualization has been added to provide a better representation of the current operation. Waypoints are represented by sphere markers. The figure  illustrates the visualization in Rviz.


 
## Potential Issues
### Robot Collides With Obstacles
In this package, the primary focus is not on obstacle avoidance or local planning. The controller implemented here is designed to follow waypoints rather than the actual path. So, there is a risk that the robot may collide with obstacles while navigating.

In the event of a collision, the robot may not immediately detect it, potentially leading to navigation errors. To address this issue, we have implemented a solution where the current pose of the robot is integrated into the current path for validity checking. If the current path is found to be invalid, indicating a potential collision, the robot enters a recovering state. After this state, the robot will be able to replan the path to avoid obstacles and resumes navigation.

![Non-optimized path](imgs/wall_loop.gif)

It's important to note that while this solution improves collision detection and recovery, it may not be effective if the robot becomes trapped in an obstacle while facing outward or sideways. In such cases, the robot may continuously move backward, leading to being stuck in a loop.

### Non-Optimized Path

The utilization of the RRT algorithm in this package can result in non-optimized paths due to its inherent randomness and lack of focus on finding the most efficient path. As a consequence, there is a potential for the robot to plan a detour path, leading to slower navigation.

To mitigate this issue, it's essential to tune the parameters of the RRT algorithm and provide it with the appropriate domain knowledge. By adjusting these parameters and providing constraints specific to the environment, the RRT algorithm can be guided to generate more optimized paths.
![Non-optimized path](imgs/lab1_detour_path.png)

The figure illustrates this problem, showcasing an example of a non-optimized path generated by the RRT algorithm.

### Error in controller loop 
An issue arises from the concurrent execution of the controller loop and the path checking process, both of which utilize the self.path variable. This concurrency may lead to coding errors, as there is a possibility that `self.path` could be set to empty during the execution of the control loop. 

## Demo Video 
[![Online Path Planning ROS - HOP](https://markdown-videos-api.jorgenkh.no/url?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DgHljYtFDeWU)](https://www.youtube.com/watch?v=gHljYtFDeWU)