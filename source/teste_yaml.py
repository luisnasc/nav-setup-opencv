#!/usr/bin/env python3
import yaml

def init_setup():
    global zoom_factor, radius, map_file, global_origin, resolution, botao_rotacionar
    f = open('../config_escritorio.yaml')
    data = yaml.load(f, Loader=yaml.FullLoader)

    map_file = '../'+data['image']
    resolution = data['resolution']
    global_origin = data['origin']
    zoom_factor = 1

init_setup()


print(map_file)
print(resolution)
print(global_origin)