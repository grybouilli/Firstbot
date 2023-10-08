from pypot.dynamixel.io import DxlIO
import time
import controls as ctrl
import numpy as np
import odom
import sys
# Paramètres de communication
port = '/dev/ttyACM0'  # Port série de votre moteur
print("debut")
with DxlIO(port) as dxl_io:
    dxl_io.set_wheel_mode([1,2])
    dxl_io.enable_torque([1,2])
    # odom.rotate_robot(dxl_io, np.pi/2)
    odom.go_to_xya_odom(dxl_io, int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
