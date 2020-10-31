# SUGAR2: Simulation with Unity and Gazebo for Augmented Reality and Robots

SUGAR2 is a novel hybrid simulation platform that for the first time supports the simultaneous simulation of human-multi-robot behaviors and their AR-based interactions.

The figures shows the Gazebo environment with the workbench (left), and the three Turtlebot2 robots waiting outside the room (right).

![Image of Gazebo Environment](https://github.com/kchanda2/SUGAR2/blob/master/images/three_robots_table_chair.png)          ![Image of Gazebo Three Robots](https://github.com/kchanda2/SUGAR2/blob/master/images/three_robots_zoomed_center.png)

The figures shows the Unity environment with the workbench, the virtual human and the virtual AR device (left), and, the three robots waiting outside in Unity (right).

![Image of Virtual Human](https://github.com/kchanda2/SUGAR2/blob/master/images/three_robots_table_chair_unity_resized.png)           ![Image of Unity Three Robots](https://github.com/kchanda2/SUGAR2/blob/master/images/three_robots_zoomed_center_unity.png)

The figures shows the third person view of the virtual human holding tablet (left), and the first person view of the virtual human looking at the virtual AR interface (right).

![Image of Unity 3POV](https://github.com/kchanda2/SUGAR2/blob/master/images/human_tablet_resized.png)            ![Image of Zoomed Tablet](https://github.com/kchanda2/SUGAR2/blob/master/images/zoomed_human_tablet.png)


# Instructions to run the Unity simulation environment:
The virtual human and the AR device are simulated in [Unity](https://unity.com/). The simulated environment uses ```Unity 2019.3.0a2```, so to avoid dependency related errors, please install the same version of Unity.
To import the package to Unity, create a new project, and import the project folder.

# Deploying code to an AR device (Android):
Ensure that you install ```Android build support``` including ```Android SDK & NDK Tools, and OpenJDK``` by going to Installs in Unity Hub.
Once the packages are installed, you can connect an Android device in debugging mode. In the build settings, select Android as the platform and click Apply.
Then, Build and run to deploy the visualizations to an AR device.

# Instructions to run the Gazebo simulation environment:
The Gazebo environment simulates the multi-robot behaviors. The simualation environment of Gazebo can be found under Gazebo folder.
The instructions assume that [ROS](https://www.ros.org/) and [Gazebo](http://gazebosim.org/tutorials?tut=ros_overview) are already installed. We use ROS Kinectic in our simulations. To communicate with Unity, we need to install [ROS#](https://github.com/siemens/ros-sharp). Also, ROS# needs rosbridge_suite to intiate TCP/IP connections with Unity.

Once ROS and Gazebo are installed, create a workspace and add the Gazebo folder to it and recompile the workspace.
Then in a terminal, run the following command:
```
roslaunch asp_navigation simulation.launch
```
The above command will start the Gazebo simulation in the environment show above with three turtlebots and also run RViz that shows the map already generated using SLAM.
Then run the following command in a terminal to start rosbridge.
```
roslaunch file_server publish_description_turtlebot2.launch
```
The codebase can be deployed to a real robot by running the following command:
```
roslaunch asp_navigation bot_bringup.launch
```
