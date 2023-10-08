import time
import numpy as np
import math
from math_utils import get_direction_angle
RADIUS = 2.6 #cm
ANGLE_ROBOT=0

LEFT = 2
RIGHT= 1

DEGREE_TIME_RELATION=0.75/90 #trouvé à la main 

def rotate_wheel(robot, rot_speed, side):
    if side == RIGHT:
        rotate_right_wheel(robot,rot_speed)
    else:
        rotate_left_wheel(robot,rot_speed)

def rotate_left_wheel(robot, rot_speed):
    robot.set_moving_speed({LEFT:rot_speed})

def rotate_right_wheel(robot, rot_speed):
    robot.set_moving_speed({RIGHT:-rot_speed})

def get_rot_speed(speed):
    global RADIUS
    return 180 * speed / (RADIUS * np.pi)

def get_speed_from_rod(rod_speed):
    global RADIUS
    return rod_speed * RADIUS * np.pi / 180

def go_forward(robot, speed):
    rot_speed = get_rot_speed(speed)
    robot.set_moving_speed({1:-rot_speed})
    robot.set_moving_speed({2:rot_speed})
def stop(robot):
    go_forward(robot,0)

def go_side(robot, current_speed,side, other_side):
    if current_speed < 0.01:
        rotate_wheel(robot, -360, side)
        rotate_wheel(robot, 360, other_side)
        return
    rot_speed= get_rot_speed(current_speed)
    rotate_wheel(robot, 2 * rot_speed, other_side)
    rotate_wheel(robot, rot_speed, side)

def go_right(robot, current_speed):
    go_side(robot,current_speed,1,2)

def go_left(robot, current_speed):
    go_side(robot,current_speed,2,1)

def rotation(robot,teta):
    global ANGLE_ROBOT
    ANGLE_ROBOT+=teta
    if teta < 0:
        go_right(robot,0)
    if teta > 0:
        go_left(robot,0)
    time.sleep(np.absolute(teta)*DEGREE_TIME_RELATION)

    stop(robot)

#suppose que le graphe x,y x positif est vers la droite et y positif vers le haut
def go_to(robot,cx,cy, current_theta, x,y,target_theta, current_speed):
    global ANGLE_ROBOT
    ANGLE_ROBOT=current_theta
    dir_angle = get_direction_angle(cx, cy, x, y)
    print("angle is ", dir_angle)
    rotation(robot, np.degrees(dir_angle))
    travel_time = np.sqrt(x**2+y**2) / current_speed

    print("time is ", time)
    go_forward(robot,current_speed)
    time.sleep(travel_time)
    stop(robot)

    print(f"target_theta {target_theta}")
    print(f"ANGLE_ROBOT {ANGLE_ROBOT}")
    final_theta=target_theta-ANGLE_ROBOT
    print(f"final_theta = {final_theta}")
    rotation(robot,final_theta)
    stop(robot)
