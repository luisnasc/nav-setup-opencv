import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import math, json
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter
#from tkinter import *
from ScrollableImage import *

global mouseX, mouseY

global clicked_point
global zoom_factor, radius, map_file
zoom_factor=1
radius=10
global_origin=[]
map_file = 'map.png'
resolution = 1
tag_mode = False
draw_mode = False
drawing = False
graph_mode = False
count_click = 0
angle_mode = False

colors = {'blue': (255, 0, 0), 'green': (0, 255, 0), 'red': (255, 0, 255), 'yellow': (0, 255, 255), 'magenta': (255, 0, 255), 'cyan': (255, 255, 0), 'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (125, 125, 125), 'rand': np.random.randint(0, high=256, size=(3,)).tolist(), 'dark_gray': (50, 50, 50), 'light_gray': (220, 220, 220)}

def init_setup():
    global zoom_factor, radius, map_file, global_origin, resolution
    f = open('config.json')
    data = json.load(f)
    map_file = data['map_file']
    resolution = data['resolution']
    radius = data['radius']
    global_origin = data['global_origin']
    zoom_factor = data['scale']

init_setup()




def zoom(img, zoom_factor):
    global_origin_zoom = np.dot(global_origin,zoom_factor)
    return cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor), global_origin_zoom

def trans_coord(point):
    x = global_origin[0] + (-1) * point[0]
    y = global_origin[1] + (-1) * point[1]   
    return x,y 


def create_circle(x, y, r, canvasName): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1)

def draw_circle2(event):
    mouseX,mouseY = event.x,event.y
    max_y, max_x = np.shape(img)
    global root, image_window, seta_p1, angle_mode, tag_mode
    
    #myCanvas = tkinter.Canvas(root)
    #myCanvas.pack()
    if graph_mode:
        try:
            canvas = event.widget
            mouseX = canvas.canvasx(event.x)
            mouseY = canvas.canvasy(event.y)

            theta = np.pi
            point = np.transpose([mouseX, mouseY, 1])
            c, s = np.cos(float(theta)),np.sin(float(theta))
            HT = np.array([
            [c, 0, s], # Homogeneous Transformation Matrix
            [0, 1, 0],
            [-s, 0, c]])
            point2 = np.dot(HT, point)

            x,y = point2[0]*resolution, (point2[1]-max_y)*resolution

            point = trans_coord([x,y])
            x,y = point[0], point[1]
            print(np.divide(point, zoom_factor))
            create_circle(mouseX, mouseY, radius*zoom_factor, canvas)
        except:
            pass
    elif tag_mode:

        try:
            canvas = event.widget
            mouseX = canvas.canvasx(event.x)
            mouseY = canvas.canvasy(event.y)

            theta = np.pi
            point = np.transpose([mouseX, mouseY, 1])
            c, s = np.cos(float(theta)),np.sin(float(theta))
            HT = np.array([
            [c, 0, s], # Homogeneous Transformation Matrix
            [0, 1, 0],
            [-s, 0, c]])
            point2 = np.dot(HT, point)

            x,y = point2[0]*resolution, (point2[1]-max_y)*resolution

            point = trans_coord([x,y])
            x,y = point[0], point[1]
            print(np.divide(point, zoom_factor))
        except:
            pass



        if angle_mode=='False':
            angle_mode = True
            try:
                print('primeiro ponto')
                canvas = event.widget
                mouseX = canvas.canvasx(event.x)
                mouseY = canvas.canvasy(event.y)

                theta = np.pi
                point = np.transpose([mouseX, mouseY, 1])
                c, s = np.cos(float(theta)),np.sin(float(theta))
                HT = np.array([
                [c, 0, s], # Homogeneous Transformation Matrix
                [0, 1, 0],
                [-s, 0, c]])
                point2 = np.dot(HT, point)

                x,y = point2[0]*resolution, (point2[1]-max_y)*resolution

                point = trans_coord([x,y])
                seta_p1 = (mouseX, mouseY)
                x,y = point[0], point[1]
            except:
                pass

        elif angle_mode:
            angle_mode = False
            print('segundo ponto')
            try:
                canvas = event.widget
                mouseX = canvas.canvasx(event.x)
                mouseY = canvas.canvasy(event.y)

                theta = np.pi
                point = np.transpose([mouseX, mouseY, 1])
                c, s = np.cos(float(theta)),np.sin(float(theta))
                HT = np.array([
                [c, 0, s], # Homogeneous Transformation Matrix
                [0, 1, 0],
                [-s, 0, c]])
                point2 = np.dot(HT, point)

                x,y = point2[0]*resolution, (point2[1]-max_y)*resolution

                point = trans_coord([x,y])
                theta = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
                print(f'Posição da Tag: {theta}')
                seta_p2 = (mouseX, mouseY)
                print(np.divide(point, zoom_factor))

                canvas.create_line(seta_p1[0], seta_p1[1], seta_p2[0], seta_p2[1], arrow=tkinter.LAST) 
            except:
                pass



init_setup()


img = cv2.imread(map_file, cv2.IMREAD_UNCHANGED)

cv2.namedWindow('image')
#cv2.setMouseCallback('image',draw_circle)
img, global_origin = zoom(img, zoom_factor)
altura, largura = np.shape(img)

def close_win():
   root.destroy()

def ligar_tags():
    global tag_mode
    if button_tag.config('text')[-1] == 'Concluir Posicionamento':
        button_tag.config(text='Posicionar TAGS')
        print('habilitado')
        tag_mode = False
    else:
        button_tag.config(text='Concluir Posicionamento')
        tag_mode = True

def ligar_grafos():
    global graph_mode
    if button_graph.config('text')[-1] == 'Concluir Grafo':
        button_graph.config(text='Criar Grafo')
        graph_mode = False
    else:
        button_graph.config(text='Concluir Grafo')
        graph_mode = True

root = tkinter.Tk()
root.title("Vixsystem - Setup Navegação")
root.attributes('-zoomed', True)
button_tag = tkinter.Button(root, text="Posicionar TAGS", width=20, height=5, command=ligar_tags)
button_tag.place(x=230, y=20)

button_graph = tkinter.Button(root, text="Configurar Grafo", width=20, height=5, command=ligar_grafos)
button_graph.place(x=230, y=130)

button_close = tkinter.Button(root, text="Sair da Aplicação", width=20, height=5, command=close_win)
button_close.place(x=230, y=250)


root.bind("<Button 1>",draw_circle2)
#root.bind("<ButtonRelease-1>",create_seta)
im = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=im)
image_window = ScrollableImage(root, image=imgtk, scrollbarwidth=6, width=largura, height=altura)


#while(1):
    #cv2.imshow('image',img)
    #tkinter.Label(root, image=imgtk).pack() 
image_window.pack()
root.mainloop()
# k = cv2.waitKey(20) & 0xFF
# if k == 27:
#     break
# elif k == ord('d'):
#     print(f'desenhandooo')
#     tag_mode = not tag_mode
# elif k == ord('t'):
#     print('Adicionando tags')
#     tag_mode = not tag_mode
