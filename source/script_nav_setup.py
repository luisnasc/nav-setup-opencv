#!/usr/bin/env python3

# from re import X
from errno import EUCLEAN
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math, json
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter
#from tkinter import *
import tkinter.simpledialog
from ScrollableImage import *

global mouseX, mouseY

global clicked_point
global zoom_factor, radius, map_file
zoom_factor=1
radius=10
global_origin=[]
map_file = '../map.png'
resolution = 1
tag_mode = False
draw_mode = False
drawing = False
graph_mode = False
distance_mode = False
distance2_mode = False
count_click = 0
angle_mode = False
dict_tags = {}
objects_to_delete = []
cont_tag = 0
flag_iniciou_tag = 0
botao_rotacionar = False
angulo_rotacionar = 0.0
rotacionar = False
click_p1 = 0
count_scale = 1
global_origin_last = []
dict_objects = {}

colors = {'blue': (255, 0, 0), 'green': (0, 255, 0), 'red': (255, 0, 255), 'yellow': (0, 255, 255), 'magenta': (255, 0, 255), 'cyan': (255, 255, 0), 'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (125, 125, 125), 'rand': np.random.randint(0, high=256, size=(3,)).tolist(), 'dark_gray': (50, 50, 50), 'light_gray': (220, 220, 220)}

def init_setup():
    global zoom_factor, radius, map_file, global_origin, resolution, botao_rotacionar
    f = open('../config_aeroporto_vix.json')
    data = json.load(f)
    map_file = '../'+data['map_file']
    resolution = data['resolution']
    global_origin = data['global_origin']
    zoom_factor = data['scale']

init_setup()



def zoom(img, zoom_factor, global_origin):
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


def transforma_ponto(mouseX, mouseY, zoom_factor, resolution, max_y):
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
    point = np.divide(point, zoom_factor)
    return point


def click_esq_event(event):
    shape = np.shape(img)
    max_y, max_x  = shape[0], shape[1]
    print(event.state)


    global seta_p1, angle_mode, tag_mode, point1, objects_to_delete, canvas, click_p1
    global click_p1_trans, contador_mouse_move, distance2_mode, distance_mode
    canvas = event.widget

    if event.state == 17:
        distance_mode = True
    elif event.state != 17 and button_dist.config('text')[-1] != 'Concluir':
        distance_mode = False
    
    mouseX, mouseY = 0,0
    try:
        mouseX = canvas.canvasx(event.x)
        mouseY = canvas.canvasy(event.y)
    except Exception as e:
        print(e)

    if (str(canvas) == '.!scrollableimage.!canvas') :

        if graph_mode: # draw circles
            point = transforma_ponto(mouseX, mouseY, zoom_factor, resolution, max_y)
            
            radius_graph = int(txt_raio.get("1.0","end-1c"))

            #print(point)
            c = create_circle(mouseX, mouseY, radius_graph, canvas)
            objects_to_delete.append(c)
        elif tag_mode:
            if not angle_mode:
                angle_mode = True
                contador_mouse_move = 0
                point1 = transforma_ponto(mouseX, mouseY, zoom_factor, resolution, max_y)

                seta_p1 = (mouseX, mouseY)
                #ponto
                obj = canvas.create_line(seta_p1[0], seta_p1[1], seta_p1[0], seta_p1[1], width=1, fill='blue')
                objects_to_delete.append(obj)
              
                #cruz
                obj = canvas.create_line(seta_p1[0]+30, seta_p1[1], seta_p1[0]-30, seta_p1[1], width=3, fill='green')
                objects_to_delete.append(obj)
                obj = canvas.create_line(seta_p1[0], seta_p1[1]+30, seta_p1[0], seta_p1[1]-30, width=3, fill='green')
                objects_to_delete.append(obj)  
        elif distance_mode:
            if not distance2_mode:
                distance2_mode = True
                point1 = transforma_ponto(mouseX, mouseY, zoom_factor, resolution, max_y)
                seta_p1 = (mouseX, mouseY)
                contador_mouse_move = 0                    
        else:
            point = transforma_ponto(mouseX, mouseY, zoom_factor, resolution, max_y)
            click_p1 = [mouseX, mouseY]
            click_p1_trans = point

            texto_pose = '{xx:.3f}, {yy:.3f}'
            #check_rot.config(text=texto_pose.format(angulo = np.rad2deg(theta)))

            if(rotacionar):
                ponto_rotacionado = rotate_position(point)
                txt_pose.delete("1.0", tkinter.END)
                txt_pose.insert('end', texto_pose.format(xx = ponto_rotacionado[0], yy = ponto_rotacionado[1]) )                
                #print(ponto_rotacionado)
            else:
                txt_pose.delete("1.0", tkinter.END)
                txt_pose.insert('end', texto_pose.format(xx = point[0], yy = point[1]) )


def create_seta(event):
    #mouseX,mouseY = event.x,event.y
    shape = np.shape(img)
    max_y, max_x  = shape[0], shape[1]
    # max_y, max_x = np.shape(img)
    global seta_p1, angle_mode, tag_mode, cont_tag, objects_to_delete, dict_objects, count_scale, distance_mode, distance2_mode
    
    try:
        canvas = event.widget
        mouseX = canvas.canvasx(event.x)
        mouseY = canvas.canvasy(event.y)
    except Exception as e:
        print(e)  

    if(botao_rotacionar):
        calcular_angulo_drop(event, click_p1, click_p1_trans, objects_to_delete)      

    if (angle_mode and str(canvas) == '.!scrollableimage.!canvas'): # Desenho seta orientação tag
        angle_mode = False
            
        point2 = transforma_ponto(mouseX, mouseY, zoom_factor, resolution, max_y)

        theta = math.atan2(point2[1]-point1[1], point2[0]-point1[0])
        seta_p2 = (mouseX, mouseY)
        
        #removendo a cruz
        ids = [objects_to_delete.pop(), objects_to_delete.pop(), objects_to_delete.pop()]
        
        image_window.reset_canvas(ids)
        txt_local = tkinter.simpledialog.askstring(title="Posicionando TAGs", prompt="Informe a descrição do local:")
        
        if txt_local != None:
            x_fim1 =  15*np.cos(-theta+np.pi)
            y_fim1 = 15*np.sin(-theta+np.pi)

            obj_seta = canvas.create_line(seta_p1[0]+x_fim1, seta_p1[1]+y_fim1, seta_p1[0], seta_p1[1], width=3+count_scale, fill='blue', arrow=tkinter.LAST)
            objects_to_delete.append(obj_seta)
            dict_objects[str(obj_seta)] = ['seta', seta_p1]
            # text=str(cont_tag).zfill(3)

            if -0.6 >= theta >=-2.5:
                x_fim = 25* np.cos(-theta+np.pi)
                y_fim = 25* np.sin(-theta+np.pi)  
                #print('aqui')              
            else:
                x_fim = 34* np.cos(-theta+np.pi)
                y_fim = 34* np.sin(-theta+np.pi)
            fonte = "Times "+str(10+count_scale)+" bold"
            obj_valor = canvas.create_text(seta_p1[0]+x_fim, seta_p1[1]+y_fim,fill="red",font=fonte, text=str(cont_tag).zfill(3)) 
            objects_to_delete.append(obj_valor)
            dict_objects[str(obj_valor)] = ['valor', [seta_p1[0]+x_fim, seta_p1[1]+y_fim]]
            dict_tags[str(cont_tag)] = [point1[0], point1[1], theta, txt_local]
            
            texto_pose = '{xx:.3f}, {yy:.3f}, {zz:.3f}'
            txt_pose.delete("1.0", tkinter.END)
            txt_pose.insert('end', texto_pose.format(xx = point1[0], yy = point1[1], zz = theta) )            
            print(f'Posição da {cont_tag}ª Tag: {point1[0]}, {point1[1]}, {theta}')
            cont_tag+=1



        else:
            #apagar o ponto
            image_window.reset_canvas([objects_to_delete.pop()])
        #txt_local.grab_release()

    elif (distance2_mode and str(canvas) == '.!scrollableimage.!canvas'):
        distance2_mode = False
            
        point2 = transforma_ponto(mouseX, mouseY, zoom_factor, resolution, max_y)

        theta = math.atan2(point2[1]-point1[1], point2[0]-point1[0])
        seta_p2 = (mouseX, mouseY)
        

        texto_pose = '{xx:.3f}'
        dist_final = eucl_dist(point2[0:2], point1[0:2])
        txt_dist.delete("1.0", tkinter.END)
        txt_dist.insert('end', texto_pose.format(xx = dist_final) )            
        print(f'Distancia: {dist_final}')
        #objects_to_delete.append(obj_seta)
        image_window.reset_canvas([objects_to_delete.pop()])




def mouse_move_seta(event):
    #mouseX,mouseY = event.x,event.y
    shape = np.shape(img)
    max_y, max_x  = shape[0], shape[1]
    # max_y, max_x = np.shape(img)
    global seta_p1, angle_mode, tag_mode, cont_tag, objects_to_delete, contador_mouse_move
    
    try:
        canvas = event.widget
        mouseX = canvas.canvasx(event.x)
        mouseY = canvas.canvasy(event.y)
    except Exception as e:
        pass
        #print(e)


    if angle_mode and str(canvas) == '.!scrollableimage.!canvas': # Desenho seta orientação tag
            
        point2 = transforma_ponto(mouseX, mouseY, zoom_factor, resolution, max_y)

        theta = math.atan2(point2[1]-point1[1], point2[0]-point1[0])
        seta_p2 = (mouseX, mouseY)
        #print(point1, theta)

        texto_pose = '{xx:.3f}, {yy:.3f}, {zz:.3f}'
        txt_pose.delete("1.0", tkinter.END)
        txt_pose.insert('end', texto_pose.format(xx = point1[0], yy = point1[1], zz = theta) )            

        #removendo a cruz
        if contador_mouse_move == 0:
            obj = canvas.create_line(seta_p1[0]+3, seta_p1[1], seta_p1[0]-3, seta_p1[1], width=5, fill='red')
            objects_to_delete.append(obj)      
        image_window.reset_canvas([objects_to_delete.pop()])
        obj = canvas.create_line(seta_p1[0], seta_p1[1], seta_p2[0], seta_p2[1], width=3, fill='blue', arrow=tkinter.LAST)
        objects_to_delete.append(obj)
        contador_mouse_move +=1
    elif distance2_mode and str(canvas) == '.!scrollableimage.!canvas': # Desenho seta orientação 
        point2 = transforma_ponto(mouseX, mouseY, zoom_factor, resolution, max_y)

        theta = math.atan2(point2[1]-point1[1], point2[0]-point1[0])
        seta_p2 = (mouseX, mouseY)
        #print(point1, theta)
        dist_final = eucl_dist(point2[0:2], point1[0:2])
        texto_pose = '{xx:.3f}'
        txt_dist.delete("1.0", tkinter.END)
        txt_dist.insert('end', texto_pose.format(xx = dist_final) )            

        #removendo a cruz
        if contador_mouse_move == 0:
            obj = canvas.create_line(seta_p1[0], seta_p1[1], seta_p1[0], seta_p1[1], width=1, fill='red')
            objects_to_delete.append(obj)      
        image_window.reset_canvas([objects_to_delete.pop()])
        obj = canvas.create_line(seta_p1[0], seta_p1[1], seta_p2[0], seta_p2[1], width=3, fill='green', arrow=tkinter.BOTH)
        objects_to_delete.append(obj)
        contador_mouse_move +=1        


def save_as_png(canvas,fileName):
    # save postscipt image 
    x = canvas.canvasx(40)
    y = canvas.canvasy(0)
    canvas.postscript(file = fileName + '.eps', height = altura, width=largura, x=x, y=y) 
    # use PIL to convert to PNG 
    img = Image.open(fileName + '.eps') 
    img.save(fileName + '.png', 'png') 


def draw_point(initial_point, canvas):
    python_green = "#476042"
    x1, y1 = (initial_point[0] - 3), (initial_point[1] - 3)
    x2, y2 = (initial_point[0] + 3), (initial_point[1] + 3)
    canvas.create_oval(x1, y1, x2, y2, fill=python_green)

init_setup()



def close_win():
    if tkinter.messagebox.askyesno("Confirmação", "Gostaria realmente de sair?"):
        root.destroy()
    else:
        pass

def ligar_tags():
    global tag_mode, txt_num_tag, cont_tag, flag_iniciou_tag


    if(not flag_iniciou_tag):
        cont_tag = int(txt_num_tag.get("1.0","end-1c"))

    flag_iniciou_tag = 1

    if button_tag.config('text')[-1] == 'Concluir \nTAGs':
        txt_num_tag.config(state="normal")
        txt_num_tag.delete("1.0", tkinter.END)
        txt_num_tag.insert('end', str(cont_tag))
        txt_num_tag.config(state="disabled")
        button_tag.config(text='Posicionar TAGs', background=defaultbg)
        tag_mode = False
        #txt_num_tag.config(state="normal")
        button_tag_salvar.config(state="normal")
        button_reset.config(state="normal")
        #cont_tag = int(txt_num_tag.get("1.0","end-1c"))
    else:
        button_tag.config(text='Concluir \nTAGs', background='blue')
        tag_mode = True
        button_graph.config(state="disabled")
        button_tag_salvar.config(state="disabled")
        #cont_tag = int(txt_num_tag.get("1.0","end-1c"))
        txt_num_tag.config(state="disabled")
        button_reset.config(state="disabled")


def ligar_grafos():
    global graph_mode, cont_tag

    if button_graph.config('text')[-1] == 'Concluir \nGrafo':
        button_graph.config(text='Criar Grafo', background=defaultbg)
        graph_mode = False
    else:
        button_graph.config(text='Concluir \nGrafo', background='blue')
        graph_mode = True

def calc_distance_btn():
    global distance_mode
    if button_dist.config('text')[-1] == 'Concluir':
        button_dist.config(text='Calcular distância', background=defaultbg)
        distance_mode = False
    else:
        button_dist.config(text='Concluir', background='blue')
        distance_mode = True


def reset_win(event=None):
    global image_window, im, imgtk, root, cont_tag, flag_iniciou_tag, dict_tags, dict_objects
    image_window.reset_canvas(objects_to_delete)
    flag_iniciou_tag=0
    dict_tags = {}
    dict_objects = {}
    cont_tag = int(txt_num_tag.get("1.0","end-1c"))
    txt_num_tag.config(state="normal")
    button_graph.config(state="normal")


def salvar_tags():
    global cont_tag, image_window, flag_iniciou_tag, txt_num_tag
    if tkinter.messagebox.askyesno("Confirmação", "TAGs posicionadas corretamente? Scroll retornado para a posição inicial? "):
        flag_iniciou_tag = 0
        canvas_ref = image_window.cnvs

        json_object = json.dumps(dict_tags, indent = 4)
        with open("tags.json", "w") as outfile:
            outfile.write(json_object)

        save_as_png(canvas_ref,'tags_posicionadas')
        button_graph.config(state="normal")
        txt_num_tag.config(state="normal")
        button_tag_salvar.config(state="disabled")
        tkinter.messagebox.showinfo("Confirmação", "Tags posicionadas com sucesso!")
        
    else :
        pass


def calcular_angulo_drop(event, p1, p1_trans, objects_to_delete):
    global botao_rotacionar, angulo_rotacionar
    try:
        canvas = event.widget
        mouseX = canvas.canvasx(event.x)
        mouseY = canvas.canvasy(event.y)
        shape = np.shape(img)
        max_y, max_x  = shape[0], shape[1]
        p2 = [mouseX, mouseY]

        point2 = transforma_ponto(mouseX, mouseY, zoom_factor, resolution, max_y)


        obj = canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=2, fill='red')
        objects_to_delete.append(obj)    

        obj = canvas.create_line(p1[0], p1[1], p2[0], p1[1], width=2, fill='green')
        objects_to_delete.append(obj)

        #calcular angulo
        theta = math.atan2(point2[1]-p1_trans[1], point2[0]-p1_trans[0])
        angulo_rotacionar = theta

        #Após calcular a rotação reseta o click
        botao_rotacionar = False
        texto_check = 'Rotacionar {angulo:.3f} °'
        check_rot.config(text=texto_check.format(angulo = np.rad2deg(theta)))

    except Exception as e:
        print(e)


def rotate_position(point):
        theta = -angulo_rotacionar
        c, s = np.cos(float(theta)),np.sin(float(theta))
        point = np.transpose([point[0], point[1], 1])
        HT = np.array([
        [c, -s, s], # Homogeneous Transformation Matrix
        [s, c, 0],
        [0, 0, 1]])

        ponto =  np.dot(HT, point)
        return ponto[0], ponto[1]



def get_position_botao_dir(event): #
    shape = np.shape(img)
    max_y, max_x  = shape[0], shape[1]

    canvas = event.widget
    try:
        mouseX = canvas.canvasx(event.x)
        mouseY = canvas.canvasy(event.y)
    except Exception as e:
        print(e)
    point1 = transforma_ponto(mouseX, mouseY, zoom_factor, resolution, max_y)
    texto_pose = '{xx:.3f}, {yy:.3f}'
    txt_pose.delete("1.0", tkinter.END)
    txt_pose.insert('end', texto_pose.format(xx = point1[0], yy = point1[1]) )      


def calc_rotacao():
    global botao_rotacionar
    botao_rotacionar = True


def check_angulo_marcado():
    global rotacionar
    if (flag_rot.get() == 1):
        print('Rotacionar')
        #rotacionar todo click
        rotacionar = True
    else:
        print('Nao Rotacionar')
        rotacionar = False


##
##  ::: PRINCIPAL ::: 
##

img = cv2.imread(map_file, cv2.IMREAD_UNCHANGED)
original_img = img
#cv2.namedWindow('image')
#cv2.setMouseCallback('image',draw_circle)
global_origin_default = global_origin
global_origin_last = global_origin
img, global_origin = zoom(img, zoom_factor, global_origin_default)
shape = np.shape(img)
altura, largura  = shape[0], shape[1]



root = tkinter.Tk()
root.title("Vixsystem - Setup Navegação")
root.attributes('-zoomed', True)
defaultbg = root.cget('bg')

im = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=im)

image_window = ScrollableImage(root, image=imgtk, scrollbarwidth=6, width=1600, height=1200)
image_window.pack(side="right")

#draw_point(global_origin, image_window.cnvs)

labelframe = tkinter.LabelFrame(root, text="Posicionamento das TAGs", width=200, height=200, labelanchor="n")
labelframe.pack( anchor="nw", padx=20,  pady=10 )
 

lbl_num_tag = tkinter.Label(labelframe, text="Nº Tag Inicial")
lbl_num_tag.place(x=10, y=10)

txt_num_tag = tkinter.Text(labelframe, height = 1, width = 5, end="0")
txt_num_tag.place(x=120, y=10)
txt_num_tag.insert('end', '0')

button_tag = tkinter.Button(labelframe, text="Posicionar TAGs", width=10, height=2, command=ligar_tags, wraplength=90)
button_tag.place(x=40, y=50)

button_tag_salvar = tkinter.Button(labelframe, text="Salvar TAGs", width=10, height=2, background='lightgreen', command=salvar_tags, state="disabled", wraplength=90)
button_tag_salvar.place(x=40, y=110)

###### Pose robo

labelframe_pose = tkinter.LabelFrame(root, text="Pose do robô", labelanchor="n", width=200, height=85)
labelframe_pose.pack( anchor="w", padx=20 )


txt_pose = tkinter.Text(labelframe_pose, height = 2, width = 20, end="0", font="Times 14 bold")
txt_pose.place(x=5, y=10)
txt_pose.insert('end', '0.000, 0.000, 0.000')


###### Calcular Distância

labelframe_dist = tkinter.LabelFrame(root, text="Cálculo de distância", labelanchor="n", width=200, height=90)
labelframe_dist.pack( anchor="w", padx=20, pady=10 )

button_dist = tkinter.Button(labelframe_dist, text="Calcular Distância", width=8, height=2, wraplength=90, command=calc_distance_btn)
button_dist.place(x=8, y=10)

txt_dist = tkinter.Text(labelframe_dist, height = 1, width = 7, end="0", font="Times 13 bold")
txt_dist.place(x=105, y=20)
txt_dist.insert('end', '0.000')


lbl_dist = tkinter.Label(labelframe_dist, text="m")
lbl_dist.place(x=175, y=20)


#####   Grafo

labelframe_grafo = tkinter.LabelFrame(root, text="Configurar Grafo", width=200, height=200, labelanchor="n")
labelframe_grafo.pack( anchor="w", padx=20 )


lbl_raio = tkinter.Label(labelframe_grafo, text="Radio do círculo")
lbl_raio.place(x=10, y=10)

txt_raio = tkinter.Text(labelframe_grafo, height = 1, width = 5, end="0")
txt_raio.place(x=120, y=10)
txt_raio.insert('end', '5')


button_graph = tkinter.Button(labelframe_grafo, text="Configurar \nGrafo", width=10, height=3, command=ligar_grafos,  wraplength=90)
button_graph.place(x=40, y=50)


##### Rotacionar
labelframe_rotacionar = tkinter.LabelFrame(root, text="Rotacionar Mapa", width=200, height=150, labelanchor="n")
labelframe_rotacionar.pack( anchor="w", padx=20 )

button_rotacao = tkinter.Button(labelframe_rotacionar, text="Calcular Rotação", width=10, height=3, wraplength=90, command=calc_rotacao)
button_rotacao.place(x=40, y=15)

flag_rot = tkinter.IntVar()
check_rot = tkinter.Checkbutton(labelframe_rotacionar, text='Rotacionar',variable=flag_rot, onvalue=1, offvalue=0, command=check_angulo_marcado)
check_rot.place(x=10, y=90)

labelframe_geral = tkinter.LabelFrame(root, text="Geral", width=200, height=200, labelanchor="n")
labelframe_geral.pack( anchor="w", padx=20 )

button_reset = tkinter.Button(labelframe_geral, text="Resetar", width=10, height=3, command=reset_win)
button_reset.place(x=10, y=20)

button_close = tkinter.Button(labelframe_geral, text="Sair", width=10, height=3, command=close_win)
button_close.place(x=10, y=100)

def eucl_dist(point1, point2):
    sum_sq = np.sum(np.square(np.array(point1) - np.array(point2)))
    return np.sqrt(sum_sq)

def resize_canvas_obj(event, c, obj_id, dict_obj, val_zoom):
    #c = canvas
    

    if dict_obj.get( str(obj_id) )[0] == 'seta':
        # print('aumentando seta')
        width = 3+val_zoom
        x0 = c.bbox(obj_id)[0] # x-coordinate of the left side of the text
        c.itemconfigure(obj_id, width=width)
        # shrink to fit
        height = c.winfo_height() # canvas height
        y1 = c.bbox(obj_id)[3] # y-coordinate of the bottom of the text
        while y1 > height:# and fontsize > 1:
            #fontsize -= 1
            c.itemconfigure(obj_id, width=width)
            y1 = c.bbox(obj_id)[3]
    elif dict_obj.get( str(obj_id) )[0] == 'valor':
        # print('aumentando valor')
        fontsize = 10+val_zoom
        font = "Times " + str(fontsize) + " bold"
        x0 = c.bbox(obj_id)[0] # x-coordinate of the left side of the text
        c.itemconfigure(obj_id, width=c.winfo_width() - x0, font=font)
        # shrink to fit
        height = c.winfo_height() # canvas height
        y1 = c.bbox(obj_id)[3] # y-coordinate of the bottom of the text
        while y1 > height and fontsize > 1:
            fontsize -= 1
            c.itemconfigure(obj_id, font=font)
            y1 = c.bbox(obj_id)[3]

def mouse_scroll(event):
    global root, img, count_scale, altura, largura, global_origin, imgtk, zoom_factor, global_origin_last
    
    if flag_iniciou_tag == 1:
        print('Finalizar esse processo')

    canvas = event.widget
    if event.num == 4 and event.state == 20:
        count_scale+=1
        zoom_factor = count_scale
        global_origin_last = global_origin
        img, global_origin = zoom(original_img, count_scale, global_origin_default)


        shape = np.shape(img)
        altura, largura  = shape[0], shape[1]

        shape_old = np.shape(original_img)
        altura_old, largura_old  = shape_old[0], shape_old[1]

        distancia = eucl_dist(shape, shape_old)

        for obj_id in objects_to_delete:
            if str(obj_id) in list(dict_objects.keys()) and canvas.type(obj_id) in ['line', 'text']:

                #print(obj_id)
                #print(dict_objects.get(str(obj_id)))
                position = dict_objects.get(str(obj_id))[1]
                print('Escala', count_scale)
                print('posicao', position)
                position_final = np.dot(position, count_scale)
                # distancia = eucl_dist(position, position_final)
                dif_x, dif_y = (position_final[0]-position[0]), (position_final[1]-position[1])

                resize_canvas_obj(event, canvas, obj_id, dict_objects, count_scale)


                #image_window.reset_canvas([objects_to_delete.pop()])
                #obj = canvas.create_line(seta_p1[0], seta_p1[1], seta_p2[0], seta_p2[1], width=3, fill='blue', arrow=tkinter.LAST)
                #objects_to_delete.append(obj)


                canvas.move(obj_id, dif_x, dif_y)
                #canvas.itemconfigure(obj_id, width=width)


        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)
        #print('foi aqui')

        image_window.redraw_canvas(1, imgtk)
        #canvas.create_image(0, 0, anchor='nw', image=imgtk)


    if event.num == 5 and event.state == 20:
        print('zoom out')
        #canvas.delete("all")
        count_scale-=1
        zoom_factor = count_scale
        if(count_scale < 1):
            count_scale = 1
        else:
            global_origin_last = global_origin
            img, global_origin = zoom(original_img, count_scale, global_origin_default)
            shape = np.shape(img)
            altura, largura  = shape[0], shape[1]

            shape_old = np.shape(original_img)
            

            for obj_id in objects_to_delete:
                if str(obj_id) in list(dict_objects.keys()):
                    print('foi')
                    resize_canvas_obj(event, canvas, obj_id, dict_objects, count_scale)

            im = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=im)

            image_window.redraw_canvas(1, imgtk)
            


#<Double-Button-1
root.bind("<Button 1>",click_esq_event)

root.bind("<Button 3>",get_position_botao_dir)
root.bind("<ButtonRelease-1>",create_seta)
root.bind("<B1-Motion>",mouse_move_seta)
root.bind_all("<Button-4>", mouse_scroll)
root.bind_all("<Button-5>", mouse_scroll)

root.mainloop()