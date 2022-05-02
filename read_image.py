import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import math

global mouseX, mouseY

global clicked_point
global zoom_factor, radius
tag_mode = False
draw_mode = False
drawing = False
radius = 50
global_origin = [-13.80, -13.80] # pegar esse valor global no arquivo
count_click = 0

colors = {'blue': (255, 0, 0), 'green': (0, 255, 0), 'red': (255, 0, 255), 'yellow': (0, 255, 255), 'magenta': (255, 0, 255), 'cyan': (255, 255, 0), 'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (125, 125, 125), 'rand': np.random.randint(0, high=256, size=(3,)).tolist(), 'dark_gray': (50, 50, 50), 'light_gray': (220, 220, 220)}


def zoom(img, zoom_factor):
    global_origin_zoom = np.dot(global_origin,zoom_factor)
    return cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor), global_origin_zoom

def trans_coord(point):
    x = global_origin[0] + (-1) * point[0]
    y = global_origin[1] + (-1) * point[1]   
    return x,y 

def draw_circle(event,x,y,flags,param):
    mouseX,mouseY = x,y
    max_y, max_x = np.shape(img)

    if draw_mode:

        global ix,iy,drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix,iy = x,y
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                if tag_mode == True:
                    cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
                else:
                    cv2.circle(img,(x,y),5,(0,0,255),-1)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            if tag_mode == True:
                cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
            else:
                cv2.circle(img,(x,y),5,(0,0,255),-1)
        
    elif tag_mode:
        # Clica, desenha um ponto
        # Obtém a coordenada
        # O segundo click desenha outro ponto
        # obtém a coordenada e calcula o atan2(), sendo a orientacao da tag. 
        # sai do tag mode.
        global angle_mode, p1, p2, seta_p1, seta_p2
        mouseX, mouseY = x,y
        if event == cv2.EVENT_LBUTTONDOWN:
            angle_mode = True
            mouseX, mouseY = x,y

            theta = np.pi
            point = np.transpose([mouseX, mouseY, 1])
            c, s = np.cos(float(theta)),np.sin(float(theta))
            HT = np.array([
            [c, 0, s], # Homogeneous Transformation Matrix
            [0, 1, 0],
            [-s, 0, c]])
            point2 = np.dot(HT, point)
            x,y = point2[0]/10, (point2[1]-max_y)/10
            p1 = trans_coord([x,y])
            seta_p1 = (mouseX, mouseY)
            print(f'posicao tag: {p1}')

   




        elif event == cv2.EVENT_MOUSEMOVE:
            pass
        elif event == cv2.EVENT_LBUTTONUP:
            angle_mode = False
            mouseX, mouseY = x,y

            theta = np.pi
            point = np.transpose([mouseX, mouseY, 1])
            c, s = np.cos(float(theta)),np.sin(float(theta))
            HT = np.array([
            [c, 0, s], # Homogeneous Transformation Matrix
            [0, 1, 0],
            [-s, 0, c]])
            point2 = np.dot(HT, point)
            x,y = point2[0]/10, (point2[1]-max_y)/10
            p2 = trans_coord([x,y])
            #math.atan2(y_max-y_min, x_max-x_min)
            theta = math.atan2(p2[1]-p1[1], p2[0]-p1[0])

            print(f'posicao tag: {p1[0], p1[1], np.rad2deg(theta)}')
            seta_p2 = (mouseX, mouseY)
            cv2.arrowedLine(img, (np.round(seta_p1[0]),np.round(seta_p1[1])), (np.round(seta_p2[0]),np.round(seta_p2[1])), (0,127,0), 2, cv2.LINE_AA, 0, 0.1)

            #cv2.arrowedLine(img, (np.round(p1[0]),np.round(p1[1])), (np.round(p2[0]),np.round(p2[1])), colors['blue'], 3, cv2.LINE_AA, 0, 0.3)

    else:
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(img,(x,y),radius,(0,0,0),1)
            
        elif  event == cv2.EVENT_LBUTTONUP:

            theta = np.pi
            point = np.transpose([mouseX, mouseY, 1])
            c, s = np.cos(float(theta)),np.sin(float(theta))
            HT = np.array([
            [c, 0, s], # Homogeneous Transformation Matrix
            [0, 1, 0],
            [-s, 0, c]])
            point2 = np.dot(HT, point)
            x,y = point2[0]/10, (point2[1]-max_y)/10

            point = trans_coord([x,y])
            print(np.divide(point, zoom_factor))
            clicked_point = point
            return clicked_point

            '''
            theta = np.pi/2
            c, s = np.cos(float(theta)),np.sin(float(theta))
            HT = np.array([
            [c, -s, 0], # Homogeneous Transformation Matrix
            [s, c, 0],
            [0, 0, 1]])
            point2 = np.dot(HT, point2)
            #print(max_x-point2[0], max_y-point2[1])
            print(point2[0],  point2[1])
            '''

sample_image = Image.open('map.png')
img = cv2.imread('map.png', cv2.IMREAD_UNCHANGED)

#img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
zoom_factor = 2
img, global_origin = zoom(img, zoom_factor)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('d'):
        print(f'desenhandooo')
        tag_mode = not tag_mode
    elif k == ord('t'):
        print('Adicionando tags')
        tag_mode = not tag_mode
