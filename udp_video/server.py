# -*- codeing = utf-8 -*-
import binascii
import queue
import socket
import struct
import random
import threading
import cv2
import numpy as np
import crcmod
from udp_video.util import GetHostIP

# 定义消息队列, 用于存储生产者发送的数据和消费者接收的数据
msg_queue = queue.Queue()


class server(threading.Thread):
    def __init__(self, name, address):
        # 调用父类的初始化方法
        super().__init__()
        self.address = address
        self.name = name
        print(f"{self.name} 线程启动")

    def receive_save(self):
        # 建立 udp 连接
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 提升系统缓冲区容量 --- win 默认为 8192字节即8k
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 64 * 1024)
        s.bind(self.address)
        try:
            while True:
                data, addr = s.recvfrom(64 * 1024)
                # 存放数据到消息队列
                msg_queue.put((data, addr))
        except socket.error as e:
            print("socket 异常", e)
            exit(1)
        finally:
            s.close()

    def run(self):
        self.receive_save()


# 定义消费者类，继承自 threading.Thread
class consumer(threading.Thread):
    def __init__(self, name):
        # 调用父类的初始化方法
        super().__init__()
        # 设置线程名字
        self.name = name
        print(f"{self.name} 线程启动")

    def run(self):
        # 定义视频保存地址和个数
        avi_path = "../video/cam-" + str(random.randint(0, 10000)) + ".avi"
        v = cv2.VideoWriter(avi_path, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480), True)

        # 线程运行的方法, 循环从消息队列中取出数据并处理
        while msg_queue.not_empty:
            # 从消息队列中消费数据, 返回一个元组(data, addr)
            data, addr = msg_queue.get()
            # print(type(data))  # -bytes
            # print("data = ", bin(int.from_bytes(data, byteorder=sys.byteorder)))

            # -----------------加密模块---------------------------#
            # 加密后的数据---0b100110000010001110110110111

            # after_crc_32 = binascii.crc32(data) & 0xffffffff
            # print("after crc-32 = ", hex(after_crc_32))

            # crcmod- 自定义crc算法
            # crc-32 --- X32+X26+X23+X22+X16+X12+X11+X10+X8+X7+X5+X4+X2+X+1 --- 0x104C11DB7
            # 处理数据
            frame = np.frombuffer(data, dtype=np.uint8)
            # 提取校验值
            crc32_recv = struct.unpack('<I', frame[-4:])[0]
            # 重新计算校验值
            crcmod_crc32 = crcmod.mkCrcFun(0x104C11DB7, initCrc=0, xorOut=0xffffffff)
            crc32_calc = crcmod_crc32(frame[:-4])
            if crc32_recv == crc32_calc:
                print("校验通过")
            else:
                print("校验失败")

            img_decode = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            # 一帧一帧保存图片成视频
            v.write(cv2.resize(img_decode, (640, 480)))
            try:
                # 视频展示
                cv2.startWindowThread()
                cv2.imshow('img_receive', img_decode)
                # 50ms 一张图片, 0.05s 一张图片; 5s一百张图片; 1s20张图; fps=20
                # 计算fps：fps = 1000 / x
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
            except Exception as e:
                v.release()
                cv2.destroyAllWindows()
                print("中断异常", e)


if __name__ == '__main__':
    address = GetHostIP(), 20388

    # 开启 server 监听并接收数据线程
    server("sever", address).start()
    # 消费数据
    consumer("consumer").start()
