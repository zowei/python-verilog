# -*- codeing = utf-8 -*-
import socket
import cv2
import numpy as np


# 调用摄像头获取视频数据
def get_cam():
    capture = cv2.VideoCapture(0)
    while True:
        # ret 为返回值 boolean 类型, frame为视频的每一帧
        ret, frames = capture.read()
        yield frames
        # 客户端调用显示视频, 显示当前视频画面
        cv2.imshow('the video in local', frames)
        c = cv2.waitKey(50)
        if c == 27:  # 按了esc候可以退出
            break
    return frames


# 通过客户端发送数据
class client:
    def __init__(self, frames, address):
        super().__init__()
        self.address = address
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # udp 客户端不需要 bind 服务器地址，直接获取 socket 发送
        # self.udp_socket.bind(address)
        self.frames = frames

    def post_cam(self, frame, addr):
        # 控制画面大小
        frame = cv2.resize(frame, (460, 360))
        img_encode = cv2.imencode('.jpg', frame)[1]
        # 转化为字节流
        data = np.array(img_encode).tobytes()
        # 发送数据
        self.udp_socket.sendto(data, addr)

    def run(self):
        print(f'{self.address}的线程成功启动！')
        for frame in self.frames:
            self.post_cam(frame, self.address)


if __name__ == "__main__":
    address = 'localhost', 20388
    # 调用本机的摄像机，获取视频数据
    frames = get_cam()
    # 发送数据
    client(frames, address).run()
