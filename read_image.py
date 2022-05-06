from re import X
import numpy as np
import cv2, json
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
dict_tags = {}
objects_to_delete = []
cont_tag = 0
flag_iniciou_tag = 0
botao_rotacionar = False
angulo_rotacionar = 0.0
rotacionar = False

colors = {'blue': (255, 0, 0), 'green': (0, 255, 0), 'red': (255, 0, 255), 'yellow': (0, 255, 255), 'magenta': (255, 0, 255), 'cyan': (255, 255, 0), 'white': (255, 255, 255), 'black': (0, 0, 0), 'gray': (125, 125, 125), 'rand': np.random.randint(0, high=256, size=(3,)).tolist(), 'dark_gray': (50, 50, 50), 'light_gray': (220, 220, 220)}

def init_setup():
    global zoom_factor, radius, map_file, global_origin, resolution, botao_rotacionar
    f = open('config_pacheco.json')
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
    shape = np.shape(img)
    max_y, max_x  = shape[0], shape[1]


    #max_y, max_x = np.shape(img)
    global root, image_window, seta_p1, angle_mode, tag_mode, point1, objects_to_delete, canvas, click_p1, click_p1_trans

    
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
            c = create_circle(mouseX, mouseY, radius*zoom_factor, canvas)
            objects_to_delete.append(c)
        except Exception as e:
            print(e)
    elif tag_mode:
        if not angle_mode:
            angle_mode = True
            try:
                # print('primeiro ponto')
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

                point1 = trans_coord([x,y])
                point1 = np.divide(point1, zoom_factor)
                seta_p1 = (mouseX, mouseY)
                obj = canvas.create_line(seta_p1[0]+30, seta_p1[1], seta_p1[0]-30, seta_p1[1], width=3, fill='green')
                objects_to_delete.append(obj)
                obj = canvas.create_line(seta_p1[0], seta_p1[1]+30, seta_p1[0], seta_p1[1]-30, width=3, fill='green')
                objects_to_delete.append(obj)                
                obj = canvas.create_line(seta_p1[0]+2, seta_p1[1], seta_p1[0]-2, seta_p1[1], width=3, fill='red')
                objects_to_delete.append(obj)
                x,y = point1[0], point1[1]
            except Exception as e:
                print(e)
    else:
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
            point = np.divide(trans_coord([x,y]) , zoom_factor)

            #print(np.divide(point, zoom_factor))
            click_p1 = [mouseX, mouseY]
            click_p1_trans = point
            if(rotacionar):
                ponto_rotacionado = rotate_position(point)
                print(ponto_rotacionado)
        except Exception as e:
            print(e)


def create_seta(event):
    mouseX,mouseY = event.x,event.y
    shape = np.shape(img)
    max_y, max_x  = shape[0], shape[1]
    # max_y, max_x = np.shape(img)
    global root, image_window, seta_p1, angle_mode, tag_mode, cont_tag, objects_to_delete
    
    if(botao_rotacionar):
        calcular_angulo_drop(event, click_p1, click_p1_trans, objects_to_delete)      



    if angle_mode:
        angle_mode = False
        # print('segundo ponto')
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

            point2 = trans_coord([x,y])
            point2 = np.divide(point2, zoom_factor)
            theta = math.atan2(point2[1]-point1[1], point2[0]-point1[0])
            seta_p2 = (mouseX, mouseY)
            #theta = math.atan2(seta_p1[1]-seta_p2[1], seta_p1[0]-seta_p2[0])
            
            #print(np.divide(point, zoom_factor))
            print(f'Posição da {cont_tag}ª Tag: {point1[0]}, {point1[1]}, {theta}')


            dict_tags[str(cont_tag)] = [point1[0], point1[1], theta]

            obj = canvas.create_line(seta_p1[0], seta_p1[1], seta_p2[0], seta_p2[1], width=3, fill='blue', arrow=tkinter.LAST)
            objects_to_delete.append(obj)
            obj = canvas.create_text(seta_p1[0], seta_p1[1],fill="red",font="Times 20 bold", text=str(cont_tag).zfill(4)) 
            objects_to_delete.append(obj)
            cont_tag+=1
            #
        except Exception as e:
            print(e)




def save_as_png(canvas,fileName):
    # save postscipt image 
    x = canvas.canvasx(40)
    y = canvas.canvasy(0)
    canvas.postscript(file = fileName + '.eps', height = altura, width=largura, x=x, y=y) 
    # use PIL to convert to PNG 
    img = Image.open(fileName + '.eps') 
    img.save(fileName + '.png', 'png') 

init_setup()


img = cv2.imread(map_file, cv2.IMREAD_UNCHANGED)

cv2.namedWindow('image')
#cv2.setMouseCallback('image',draw_circle)
img, global_origin = zoom(img, zoom_factor)
shape = np.shape(img)
altura, largura  = shape[0], shape[1]
# altura, largura = np.shape(img)

def close_win():
   root.destroy()

def ligar_tags():
    global tag_mode, txt_num_tag, cont_tag, flag_iniciou_tag

    if(not flag_iniciou_tag):
        cont_tag = int(txt_num_tag.get("1.0","end-1c"))

    flag_iniciou_tag = 1

    if button_tag.config('text')[-1] == 'Concluir \nTAGs':
        button_tag.config(text='Posicionar TAGs', background=defaultbg)
        tag_mode = False
        #txt_num_tag.config(state="normal")
        button_tag_salvar.config(state="normal")
        button_reset.config(state="normal")
       
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

def reset_win(event=None):
    global image_window, im, imgtk, root, cont_tag, flag_iniciou_tag, dict_tags
    image_window.reset_canvas(objects_to_delete)
    flag_iniciou_tag=0
    dict_tags = {}
    cont_tag = int(txt_num_tag.get("1.0","end-1c"))
    txt_num_tag.config(state="normal")
    button_graph.config(state="normal")
    #for i in objects_to_delete:
    #    canvas.delete(i-1)
    #    print(i)
    print('FOIII!! Limpando a tela...')

def salvar_tags():
    global cont_tag, image_window, flag_iniciou_tag
    flag_iniciou_tag = 0
    cont_tag = int(txt_num_tag.get("1.0","end-1c"))
    canvas_ref = image_window.cnvs

    json_object = json.dumps(dict_tags, indent = 4)
    with open("tags.json", "w") as outfile:
        outfile.write(json_object)

    save_as_png(canvas_ref,'tags_posicionadas')
    button_graph.config(state="normal")
    txt_num_tag.config(state="normal")
    button_tag_salvar.config(state="disabled")
    tkinter.messagebox.showinfo("Confirmação", "Tags posicionadas com sucesso!")


def calcular_angulo_drop(event, p1, p1_trans, objects_to_delete):
    global botao_rotacionar, angulo_rotacionar
    try:
        canvas = event.widget
        mouseX = canvas.canvasx(event.x)
        mouseY = canvas.canvasy(event.y)
        shape = np.shape(img)
        max_y, max_x  = shape[0], shape[1]
        p2 = [mouseX, mouseY]

        theta = np.pi
        point = np.transpose([mouseX, mouseY, 1])
        c, s = np.cos(float(theta)),np.sin(float(theta))
        HT = np.array([
        [c, 0, s], # Homogeneous Transformation Matrix
        [0, 1, 0],
        [-s, 0, c]])
        point2 = np.dot(HT, point)

        x,y = point2[0]*resolution, (point2[1]-max_y)*resolution

        point2 = trans_coord([x,y])
        point2 = np.divide(point2, zoom_factor)  




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

        print(theta)
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
        print(point)

        ponto =  np.dot(HT, point)
        return ponto[0], ponto[1]





def get_position(event): #double click
    pass

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

root = tkinter.Tk()
root.title("Vixsystem - Setup Navegação")
root.attributes('-zoomed', True)
defaultbg = root.cget('bg')

im = Image.fromarray(img)
imgtk = ImageTk.PhotoImage(image=im)
image_window = ScrollableImage(root, image=imgtk, scrollbarwidth=6, width=largura, height=altura)
image_window.pack(side="right")

labelframe = tkinter.LabelFrame(root, text="Configurar Posicionamento das Tags", width=270, height=200)
labelframe.pack( anchor="nw" )
 


button_tag = tkinter.Button(labelframe, text="Posicionar TAGs", width=10, height=3, command=ligar_tags, wraplength=90)
button_tag.place(x=20, y=20)

button_tag_salvar = tkinter.Button(labelframe, text="Salvar TAGs", width=10, height=3, background='lightgreen', command=salvar_tags, state="disabled", wraplength=90)
button_tag_salvar.place(x=140, y=20)

lbl_num_tag = tkinter.Label(labelframe, text="Nº Tag Inicial")
lbl_num_tag.place(x=20, y=100)

txt_num_tag = tkinter.Text(labelframe, height = 1, width = 5, end="0")
txt_num_tag.place(x=140, y=100)
txt_num_tag.insert('end', '0')
#left.pack()


button_graph = tkinter.Button(root, text="Configurar \nGrafo", width=10, height=3, command=ligar_grafos,  wraplength=90)
button_graph.place(x=20, y=210)

button_reset = tkinter.Button(root, text="Resetar", width=10, height=3, command=reset_win)
button_reset.place(x=20, y=280)

button_close = tkinter.Button(root, text="Sair", width=10, height=3, command=close_win)
button_close.place(x=20, y=360)

button_close = tkinter.Button(root, text="Calcular Rotação", width=10, height=3, wraplength=90, command=calc_rotacao)
button_close.place(x=20, y=460)

flag_rot = tkinter.IntVar()
check_rot = tkinter.Checkbutton(root, text='Rotacionar      ',variable=flag_rot, onvalue=1, offvalue=0, command=check_angulo_marcado)
check_rot.pack()

root.bind("<Button 1>",draw_circle2)
root.bind("<Button 3>",get_position)
root.bind("<ButtonRelease-1>",create_seta)

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
