import numpy as np
import cv2 as cv2
import time
from pypot.dynamixel.io import DxlIO
import controls as ctrl
import math
from math_utils import get_direction_angle
LEFT = 2
RIGHT= 1
RADIUS = 2.6 #cm
ANGLE_ROBOT=0

LEFT = 2
RIGHT= 1


port = '/dev/ttyACM0'  # Port série de votre moteur
vitesse = 20
borne_erreur = 50
rot_erreur=3
cpt_tour=0

def get_rot_speed(speed):
    global RADIUS
    return 180 * speed / (RADIUS * np.pi)
DEGREE_TIME_RELATION=0.75/90 #trouvé à la main 
COEFF_ERR = 90/320
def go_side_forward(robot, current_speed,bonus_speed):
    # if bonus_speed != 0:
    #     current_speed=current_speed*1/(abs(bonus_speed)*2)
    bonus_speed=bonus_speed*2
    malus_speed=bonus_speed/1.5
    
    if bonus_speed>0:  
        
        bonus_speed+=1
        malus_speed=1-malus_speed
        rot_speed = get_rot_speed(current_speed*malus_speed)
        rot_speed_sup=get_rot_speed(current_speed*bonus_speed)
        robot.set_moving_speed({RIGHT:-rot_speed})
        robot.set_moving_speed({LEFT:rot_speed_sup})
    if bonus_speed<0:  
        
        bonus_speed=1+abs(bonus_speed)
        malus_speed=1-abs(malus_speed)
        rot_speed = get_rot_speed(current_speed*malus_speed)
        rot_speed_sup=get_rot_speed(current_speed*bonus_speed)
        robot.set_moving_speed({RIGHT:-rot_speed_sup})
        robot.set_moving_speed({LEFT:rot_speed})


# def go_side_forward(robot, current_speed,bonus_speed):
#     # if bonus_speed != 0:
#     #     current_speed=current_speed*1/(abs(bonus_speed)*2)
#     if(abs(bonus_speed)>0.5):
#         bonus_speed=bonus_speed*0.9
#         malus_speed=bonus_speed*0.4
#     else:
#          bonus_speed=bonus_speed*0.5
#          malus_speed=bonus_speed*0.5
    
#     if bonus_speed<0:  
        
#         bonus_speed+=1
#         malus_speed=1-malus_speed
#         rot_speed = get_rot_speed(current_speed*malus_speed)
#         rot_speed_sup=get_rot_speed(current_speed*bonus_speed)
#         robot.set_moving_speed({RIGHT:-rot_speed})
#         robot.set_moving_speed({LEFT:rot_speed_sup})
#     if bonus_speed>0:  
        
#         bonus_speed=1+abs(bonus_speed)
#         malus_speed=1-abs(malus_speed)
#         rot_speed = get_rot_speed(current_speed*malus_speed)
#         rot_speed_sup=get_rot_speed(current_speed*bonus_speed)
#         robot.set_moving_speed({RIGHT:-rot_speed_sup})
#         robot.set_moving_speed({LEFT:rot_speed})
#     # else:
    #     rot_speed = get_rot_speed(current_speed)
    #     robot.set_moving_speed({RIGHT:-rot_speed})
    #     robot.set_moving_speed({LEFT:rot_speed})



def transfo(image,target_color):
    tresh=100
    color=["noir","orange","vert"]
    mask = np.zeros_like(image[:, :, 0])
    x=-1
    y=-1
    if target_color==color[0]:

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Seuil pour détecter le noir
        _, thresholded = cv2.threshold(gray, tresh, 255, cv2.THRESH_BINARY)
        # Trouver les contours dans l'image seuillée
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Dessiner les contours sur le masque
        cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED) 
        mask = cv2.bitwise_not(mask)

    if target_color==color[1]:
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_red = np.array([10, 100, 100])  # Limite inférieure du rouge dans l'espace HSV
        upper_red = np.array([20, 230, 230])  # Limite supérieure du rouge dans l'espace HSV

        # Créer un masque en utilisant les seuils de teinte pour détecter le rouge
        red_mask = cv2.inRange(hsv_image, lower_red, upper_red)
        # Trouver les contours des objets rouges dans l'image
        x= cv2.countNonZero(red_mask)
        return mask,x,y
    if target_color==color[2]:
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_red = np.array([23, 100, 100])  # Limite inférieure du rouge dans l'espace HSV
        upper_red = np.array([120, 240, 240])  # Limite supérieure du rouge dans l'espace HSV

        # Créer un masque en utilisant les seuils de teinte pour détecter le rouge
        red_mask = cv2.inRange(hsv_image, lower_red, upper_red)
        # Trouver les contours des objets rouges dans l'image
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Dessiner les contours sur le masque
        cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)     

    
    non_zero_points = cv2.findNonZero(mask)
    if non_zero_points is not None:
        if non_zero_points.size!=0 :
            centre = np.mean(non_zero_points, axis=0).astype(int)
 
            y=centre[0][1]
            x=centre[0][0]
            mask[y][x]=0
            return mask,x,y
    
    return mask, x,y
def deplacementV1(robot,x,frame):
    erreur = x - frame.shape[1]/2
    if x ==-1:
        ctrl.stop(robot)
    if erreur < -borne_erreur:
#        print("erreur < -40")
        ctrl.rotation(robot, -rot_erreur)
    elif erreur > borne_erreur:
 #       print("erreur 40")
        ctrl.rotation(robot, rot_erreur)
    else :
        print("forward")
        ctrl.go_forward(robot,.85*vitesse)    
        time.sleep(.75)    

def deplacementV2(robot,x,frame):
    erreur=x-frame.shape[1]/2
    bonus = (erreur/(frame.shape[0]/2))#renvoie entre 1 et -1
    if x ==-1:
        ctrl.stop(robot)
    else:
        print("bonus :",bonus)
        go_side_forward(robot,.70*vitesse,bonus)
        

def mainV2 ():
    global cpt_tour
    cap = cv2.VideoCapture(-1)
    cap.set(3,320)
    cap.set(4,240)
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    memorange=False
    while True:
        with DxlIO(port) as dxl_io:
            print("cpt tour = ", cpt_tour)
            #dxl_io.scan()
            dxl_io.set_wheel_mode([2])
            dxl_io.set_wheel_mode([2])
            # Capture frame-by-frame
            ret, frame = cap.read()
        
            hauteur, largeur, canaux = frame.shape

            debut_x = 0 # 25% de la largeur à partir de la gauche
            fin_x =3*largeur  //4 # 75% de la largeur à partir de la gauche#############c mon haut
            debut_y = hauteur // 8  # 25% de la hauteur à partir du haut
            fin_y = 3 * hauteur // 2   # 75% de la hauteur à partir du haut

            frame= frame[debut_y:fin_y, debut_x:fin_x]
            
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            # Our operations on the frame come herez
            gray ,x,y= transfo(frame,"orange")#cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            
            if cv2.waitKey(1) == ord('q'):
                break
            if x <= 20:
                print("no orange\n")
                memorange=False
            elif memorange!=True: 
                memorange=True
                cpt_tour+=1
            if cpt_tour == 1 :
                gray ,x,y= transfo(frame,"noir")#cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                deplacementV2(dxl_io,y,frame)

            if cpt_tour == 2 : 
                gray ,x,y= transfo(frame,"vert")#cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                deplacementV2(dxl_io,y,frame)

            if cpt_tour == 3:
                ctrl.stop(dxl_io)
                print("Fin du circuit\n")
                break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


mainV2()
