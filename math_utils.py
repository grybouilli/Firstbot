import numpy as np

def get_direction_angle(x, y, x_target, y_target):
    delta_x = x_target - x
    delta_y = y_target - y

    # Calculate the angle (rad) between the positive x-axis and the line to the target point
    angle_to_target = np.arctan2(delta_y, delta_x) - np.pi / 2

    return np.arctan2(np.sin(angle_to_target), np.cos(angle_to_target))
