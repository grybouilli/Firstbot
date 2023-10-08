from pypot.dynamixel.io import DxlIO
import time
import controls as ctrl
import numpy as np
import odom
import matplotlib.pyplot as plt
import cv2 as cv


pos_array1 = []
file = open("positions.txt", "w+")


# Paramètres de communication
def compute_positions(pos_array):
  port = '/dev/ttyACM0'  # Port série de votre moteur
#  print("debut")
  with DxlIO(port) as dxl_io:
    print("Debut du mapping\n")
    print("Ctrl+C pour arrêter l'enregistrement de la séquence")
    dxl_io.set_wheel_mode([1])
    dxl_io.set_wheel_mode([2])

    ctrl.stop(dxl_io)
    print("debut de la sequence de test du go to")
    v=200
    # dxl_io.set_moving_speed({1:-v})
    # dxl_io.set_moving_speed({2:v})
    dxl_io.disable_torque([1,2])
    dt = 200

    t0 = time.time()
    x = 0
    y = 0
    theta = 0
    while True:
        s1, s2 = dxl_io.get_present_speed([1,2])
        linear, angular = odom.direct_kinematics(np.pi * s2/180, np.pi * (-s1) /180)
        t1 = time.time()
        dt = t1-t0
        t0 = t1

        x, y, theta = odom.tick_odom(x,y,theta,linear, angular,dt)
        pos_array.append((x,y))
        write_pos_into_file(x, y)

        #print(f"x = {x} y = {y} theta = {theta}")
        ##condition d'arret???

    return pos_array


def write_pos_into_file(pos_x, pos_y):
  content = str(pos_x) + ',' + str(pos_y) + '\n'
  file.write(content)


  ####
compute_positions(pos_array1)
write_array_into_file(pos_array1)
