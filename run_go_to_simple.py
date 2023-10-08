from pypot.dynamixel.io import DxlIO
import sys
import controls as ctrl

# Paramètres de communication
port = '/dev/ttyACM0'  # Port série de votre moteur
print("debut")

if len(sys.argv) < 7:
    print("Missing argument")
    exit
with DxlIO(port) as dxl_io:
    print("Debut du demarrage du go to\n")
    dxl_io.set_wheel_mode([1])
    dxl_io.set_wheel_mode([2])
    ctrl.go_to(dxl_io, int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),20)
    print("Fin")
