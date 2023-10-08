import math
import time
import numpy as np
import controls as ctrl

# Constants
R = 0.026     # Wheel radius (m)
L = 0.151    # Wheelbase (m)

# Initial pose of the robot (x, y, theta)
x = 0.0
y = 0.0
theta = 0.0


def direct_kinematics(left_speed, right_speed):
    linear_speed = (R / 2) * (left_speed + right_speed)
    angular_speed = (R / L) * (right_speed - left_speed)

    return linear_speed, angular_speed

def odom(linear_speed, angular_speed, dt):
    delta_theta = angular_speed * dt
    dx = 0
    dy = 0
    if delta_theta != 0:
        center_rot_dist =  linear_speed * dt / delta_theta #cp
        dx = center_rot_dist * (1-np.cos(delta_theta))
        dy = center_rot_dist * np.sin(delta_theta)
    else:
       dy = linear_speed * dt     
    return dx, dy, delta_theta

def tick_odom(x_world, y_world, theta_world, linear_speed, angular_speed, dt):
    delta_x_robot, delta_y_robot, delta_theta = odom(linear_speed, angular_speed, dt)

    delta_x_world = delta_x_robot * math.cos(theta_world) - delta_y_robot * math.sin(theta_world)
    delta_y_world = delta_x_robot * math.sin(theta_world) + delta_y_robot * math.cos(theta_world)

    return x_world + delta_x_world, y_world + delta_y_world, theta_world + delta_theta


def inverse_kinematics(linear_speed, angular_speed):
    left_speed = (linear_speed - (L * angular_speed) / 2) / R
    right_speed = (linear_speed + (L * angular_speed) / 2) / R
    return left_speed, right_speed


def rotate_robot(robot, goal_angle, eps=0.01):
    global theta
    t0 = time.time()
    while np.abs(theta -goal_angle ) > eps:
        dir_angle = np.arctan2(np.sin(goal_angle-theta), np.cos(goal_angle-theta))
        ang_speed = np.sign(dir_angle)
        move_robot(robot, 0, ang_speed)
        t1 = time.time()
        dt = t1-t0
        t0 = t1
        theta += ang_speed * dt
    move_robot(robot,0,0)

def move_robot(robot, linear_speed, angular_speed):
    left_speed, right_speed = inverse_kinematics(linear_speed, angular_speed)
    left_speed = np.degrees(left_speed)
    right_speed = np.degrees(right_speed)

    robot.set_moving_speed({ctrl.LEFT:left_speed, ctrl.RIGHT:-right_speed})
    time.sleep(0.01)    

def go_to_xya_odom(robot, x_target, y_target, theta_target, xy_tolerance=0.01, theta_tolerance=0.001):
    global x, y, theta

    ## TESTER GET_DIRECTION_ANGLE
    dir_angle = ctrl.get_direction_angle(x, y, x_target, y_target)  # Calculate the initial angle to rotate to -> RADIANS
    
    # move(robot, linear = 0, angular = dir_angle )
    rotate_robot(robot,dir_angle)
    time.sleep(1)
    move_robot(robot,0.1,0)
    t0 = time.time()

    while True:
        t1 = time.time()
        dt = t1-t0
        t0 = t1
        # Calculate errors to target
        x_error = x_target - x
        y_error = y_target - y
        theta_error = theta_target - theta

        # Check if the robot reached the target pose within tolerances
        if abs(x_error) < xy_tolerance and abs(y_error) < xy_tolerance: # and abs(theta_error) < theta_tolerance:
            print("END !")
            break  # Robot reached the target pose

        # Recalculate the left and right speeds
        right_angular_speed, left_angular_speed = robot.get_present_speed([1,2])
 #       print(f"right motor : {right_angular_speed}  left_angular_speed : {left_angular_speed}")
        right_angular_speed *= -1

        left_speed = np.radians(left_angular_speed)
        right_speed = np.radians(right_angular_speed)

        # Recalculate the linear and angular speeds
        linear_speed, angular_speed = direct_kinematics(left_speed, right_speed)

        # Calculate the new position and orientation of the robot in the world frame
        new_x, new_y, new_theta = tick_odom(x, y, theta, linear_speed, angular_speed, dt)


        # # print("linear_speed =", linear_speed, " angular_speed =", angular_speed)
        # # print("new_x =", new_x, " new_y =", new_y, " new_theta =", new_theta)

        # # Update the global robot variables
        x = new_x
        y = new_y
        theta = new_theta

        left_to_travel = np.sqrt((x_target-x)**2 +(y_target-y)**2)

#        print(f"dif angle : {dir_angle- new_theta:.4f}")
        move_robot(robot, 0.2 * left_to_travel + 0.1, 1.2* (dir_angle- new_theta))


        # if (linear_speed > 80):
        #     print("STOP")
        #     ctrl.stop(robot) # Stop the robot
        #     break

    ctrl.stop(robot) # Stop the robot
    rotate_robot(robot, theta_target)
    return x, y, theta
