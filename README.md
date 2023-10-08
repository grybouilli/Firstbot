# Context

## Why

For my semester 9 of CS studies, I chose a major in Robotics. During the first week of this major are put in a team of six and asked to program a robot that can follow lines on the floor. They also have to do some odometry on the said robot.

## How

The following list of equipments are given to us:
* 2 servo motors MX-12W
* Fixation brackets for MX-12W
* LiPo3S battery with tension surveillance buzzer
* USB2AX UART 
* Logitech C270

The robot hunt model is left for us to create using onshape.
# Documentation

## Go to

### Simple go to

To run a simple "go to" (without odometry):
```bash
python run_go_to_simple <origin_x> <origin_y> <origin_theta> <target_x> <target_y> <target_theta>
```

### Odometric go to

To run a simple "go to" (without odometry):
```bash
python run_go_to_odom <target_x> <target_y> <target_theta>
```

## Mapping 
### Drag and map
To have a mapping of the robot's path after dragging it on the floor:
```bash
python mapping_data.py
^C
python mapping.py
```
### Follow and map

To make the robot follow a **black** line and get a map of the path: 
```
python run_line_following_map.py
```

## Follow line

There are two methods to follow a line (black line with an orange tape on start):

```
python run_line_following.py
python run_line_followingmini.py
```