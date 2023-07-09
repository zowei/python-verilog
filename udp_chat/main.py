import socket
# -*- coding: utf-8 -*-
import numpy as np
from urllib import request
import cv2

url = 'https://www.baidu.com/img/superlogo_c4d7df0a003d3db9b65e9ef0fe6da1ec.png?where=super'
resp = request.urlopen(url)
print(resp.type)

image = np.asarray(bytearray(resp.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)

cv2.imshow('url_image_show', image)

if cv2.waitKey(10000) & 0xFF == ord('q'):
    cv2.destroyAllWindows()


host = socket.gethostname()  # 本地计算机名
ip = socket.gethostbyname(host)  # 获取本地IP
