from pypot.dynamixel.io import DxlIO
from time import sleep
import controls as ctrl

# Paramètres de communication
port = '/dev/ttyACM0'  # Port série de votre moteur
print("debut")
with DxlIO(port) as dxl_io:
    dxl_io.set_wheel_mode([1])
    dxl_io.set_wheel_mode([2])
    ctrl.stop(dxl_io)
    print("fin")
