import numpy as np
import time
import matplotlib.pyplot as plt

from pypot.dynamixel.io import DxlIO
import odom

port = '/dev/ttyACM0'  # Port série de votre moteur
print("debut")
with DxlIO(port) as dxl_io:
    dxl_io.disable_torque([1,2])
    t0 = time.time()
    x = 0
    y = 0
    theta = 0

    xs = [x]
    ys = [y]
    plt.ion()

    figure, ax = plt.subplots(figsize=(8,6))
    line1, = ax.plot(xs, ys)
    plt.title("Dynamic Plot of sinx",fontsize=25)

    plt.xlabel("X",fontsize=18)
    plt.ylabel("sinX",fontsize=18)
    while True:
        s1, s2 = dxl_io.get_present_speed([1,2])
        linear, angular = odom.direct_kinematics(np.pi * s2/180, np.pi * (-s1) /180)
        t1 = time.time()
        dt = t1-t0
        t0 = t1

        x, y, theta = odom.tick_odom(x,y,theta,linear, angular,dt)
        print(f"{x} {y}")
        xs.append(x)
        ys.append(y)
        line1.set_xdata(xs)
        line1.set_ydata(ys)
        
        figure.canvas.draw()
        
        figure.canvas.flush_events()

    ##############
