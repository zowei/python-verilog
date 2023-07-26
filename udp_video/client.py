# -*- codeing = utf-8 -*-
import socket
import struct
import crcmod
import cv2
import numpy as np
from udp_video.util import GetHostIP


# 调用摄像头获取视频数据
def get_cam():
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        # ret 为返回值 boolean 类型, frame为视频的每一帧
        ret, frames = capture.read()
        yield frames
        # 客户端调用显示视频, 显示当前视频画面
        cv2.imshow('the video in local', frames)
        # 按了esc候可以退出
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    return frames


# 通过客户端发送数据
class client:
    def __init__(self, frames, address):
        super().__init__()
        self.address = address
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 提升系统缓冲区容量 --- win 默认为 8192字节即8k
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64 * 1024)
        # udp 客户端不需要 bind 服务器地址，直接获取 socket 发送
        # self.udp_socket.bind(address)
        self.frames = frames

    def post_cam(self, frame, addr):
        # 控制画面大小
        frame = cv2.resize(frame, (480, 320))
        img_encode = cv2.imencode('.jpg', frame)[1]
        # 转化为字节流
        data = np.array(img_encode).tobytes()

        # crc-32 加密
        crcmod_crc32 = crcmod.mkCrcFun(0x104C11DB7, initCrc=0, xorOut=0xffffffff)
        # 返回的是一个 32 位二进制的校验码
        crc32_value = crcmod_crc32(data)
        # 把32位校验码转化为4个字节二进制, 放到原始数据之后
        payload = data + struct.pack('<I', crc32_value)
        print("数据长度", len(payload) / 8, "B")
        # 发送数据
        self.udp_socket.sendto(payload, addr)

    def run(self):
        print(f'{self.address}的线程成功启动！')
        for frame in self.frames:
            self.post_cam(frame, self.address)


if __name__ == "__main__":
    address = GetHostIP(), 20388

    # 调用本机的摄像机，获取视频数据
    frames = get_cam()
    # 发送数据
    client(frames, address).run()
