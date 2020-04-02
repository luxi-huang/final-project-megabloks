# ME 495: Embedded Systems (Fall 2019)
# Final Project - MEGA BLOKS
## Group Members:
- Allie Pinosky
- Luxi Huang
- Marcel Bonnici
- Senthil Palanisamy

### Click to Watch on YouTube
[![The Baxter Builder](https://i.ytimg.com/vi/mz1FwBR94og/maxresdefault.jpg)](https://youtu.be/mz1FwBR94og "Baxter")

## 1. Project Overview:
For this project, Baxter assembles a MEGA BLOKS pyramid from the blocks provided by the user. The flow is:

1. Human places blocks on the plate.
2. Blocks tare detected on Baxter's camera image using OpenCV.
3. Among all detected blocks, a block is chosen at random and locate its 3D position.
4. Goal block is displayed to users on the screen.
5. Baxter picked the blocks up and places it in the drop location using position control in Moveit.
6. As a double check, the gripper hand is pushed against the block to ensure that the block is pushed in, which is applied by Force control in MoveIt.
6. Baxter repeats steps 3 and 6 until the pyramid is complete.

### My contribution:
- Designed Baxter robot Path-planing trajectory by applying Moveit and inverse kinematics modified joint velocity limits and scaling to meet desired performance.
- Programmed Baxter grippers to close and open to grab the Lego pyramid.
- Using force control in Moveit to force on Baxter grippers.

### ROS Packages and Libraries:
- Computer Vision:
	- AR Tags
	- OpenCV
	- OpenCV_bridge
- Trajectory Planning:
	- MoveIt
	- Joint Trajectory Action Server

## 2. Guide:
### A. Dont forget to source:
`source setup/baxter.bash`
- you can check the connection with `ping 10.42.0.2`
### B. Either run the launch file or steps 1-3:
`roslaunch blocks setup_blocks.launch`

1. `rosrun blocks setup_blocks_hw`
	- Enables the robot
	- Moves the arms above the table (`safe_arms` position)
	- Then it moves to the start position
	- Also sets up cameras
2. `roslaunch blocks load_tower.launch`
	- Loads the block locations into the rosparam list
3. `roslaunch blocks ar_track_baxter_cam.launch`
	- Loads the computer vision node and supporting nodes
### C. Manually enable joint action trajectory server
`rosrun baxter_interface joint_trajectory_action_server.py`
### D. Run:
1. `roslaunch baxter_moveit_config baxter_grippers.launch`
	- Starts moveit
2. `rosrun blocks test_find_block`
	- Moves the robot from detected block locations to hard-coded place positions

(Eventually, will be able to run `roslaunch blocks run_blocks.launch`, but not until we get rid of 'inputs' where you press enter in `test_find_block` debugging)
### E. When you're done, here are the functions to shut down safely:
1. Shut down all nodes, then run:
2. `rosrun blocks safe_arms`
	- Run this when you're done :)
3. `rosrun baxter_tools enable_robot.py -d`
	- Disable the robot

## 3. List of all nodes and launchfiles and what they do
### Nodes
- `computer_vision.py`
	- visualizes the Plate Space and find the ball & hole
- `move_arm_manual`
	- Moves gripper to random manually input positions for testing
- `new_find_block`
	- Determines and executes arm paths for assembling a 3 block pyramid
- `safe_arms`
	- Moves the arms to a hard-coded position away from the build space
- `setup_blocks_hw`
	- Set up configuration for hardware testing and moves arm to 'start' position
- `setup_blocks_world`
	- Spawns dummy configuration for testing and moves arm to 'start' position
- `test_find_block`
	- Robot use pick and place position to assemble the pyramid

### Launchfiles
- `ar_track_baxter_cam.launch`
	- Uses robot with alvar tags, letting it determine the baseplate's location relative to the tag
- `baxter_gazebo_test.launch`
	 - Launches a simulated worled with a building space and Baxter robot
- `run_blocks.launch`
	- Essentially runs the `test_find_block` node.
- `setup_blocks.launch`
	- Uses hard-coded place positions, moves arm to 'start' position, and include the `ar_track_baxter_cam.launch` file
## 4. System Architecture
1. Setup Baxter
	- Enable the robot
	- Move to start position
	- Enable camera
	- Enable computer_vision service
	- Load tower 'place' positions
2. Setup MoveIt (done separately from #1 because MoveIt configuration prevents moving to specific joint angles using the limb_interface. also, these steps must be run sequentially)
	1. Run Joint Trajectory Action Server
	2. Enable Baxter grippers configuration
3. Run core `find_blocks` function
	- This function can be run many times without running steps 1 and 2
	- It calls the AR service, to them them know when to find the block. This controls the flow of the program

## 5. Lessons Learned
The ultimate lesson with "The Baxter Builder" is how ambitious locking toy blocks is for a robot. While more time coding and perfecting the physical building space could improve Baxter's performance, his place position sometimes fluctuated by an entire row of studs/circles with the baseplate static between test runs. To make the program absolutely flawless, both software and hardware modifications would be needed.
