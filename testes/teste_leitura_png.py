import numpy as np
import cv2, json
f = open('config.json')
data = json.load(f)
map_file = data['map_file']
img = cv2.imread(map_file, cv2.IMREAD_UNCHANGED)

cv2.namedWindow('image')
shape = np.shape(img)
altura, largura = shape[0], shape[1]

