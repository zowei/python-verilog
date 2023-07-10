import struct
import zlib
import binascii

# 定义一个256个元素的全0数组
custom_crc32_table = [0 for x in range(0, 256)]

# 定义一个256个元素的全0数组
reversal_crc32_table = [0 for x in range(0, 256)]


# 一个8位数据加到16位累加器中去，只有累加器的高8位或低8位与数据相作用，
# 其结果仅有256种可能的组合值。
def generate_crc32_table():
    for i in range(256):
        c = i << 24
        for j in range(8):
            if c & 0x80000000:
                c = (c << 1) ^ 0x04C11DB7
            else:
                c = c << 1
        custom_crc32_table[i] = c & 0xffffffff


def get_crc32_val(bytes_arr):
    length = len(bytes_arr)
    # print(f"data length {length}")
    if bytes_arr is not None:
        crc = 0xffffffff
        for i in range(0, length):
            crc = (crc << 8) ^ custom_crc32_table[(getReverse(bytes_arr[i], 8) ^ (crc >> 24)) & 0xff]
    else:
        crc = 0xffffffff

    # - 返回计算的CRC值
    crc = getReverse(crc ^ 0xffffffff, 32)
    return crc


# 反转
def getReverse(temp_data, byte_length):
    reverseData = 0
    for i in range(0, byte_length):
        reverseData += ((temp_data >> i) & 1) << (byte_length - 1 - i)
    return reverseData


def reversal_init_crc32_table():
    for i in range(256):
        c = i
        for j in range(8):
            if c & 0x00000001:
                c = (c >> 1) ^ 0xEDB88320
            else:
                c = c >> 1

        reversal_crc32_table[i] = c & 0xffffffff


def reversal_getCrc32(bytes_arr):
    length = len(bytes_arr)
    if bytes_arr is not None:
        crc = 0xffffffff
        for i in range(0, length):
            crc = (crc >> 8) ^ reversal_crc32_table[(bytes_arr[i] ^ crc) & 0xff]
    else:
        crc = 0xffffffff
    crc = crc ^ 0xffffffff
    return crc


if __name__ == '__main__':
    s = struct.pack('>i', 400)
    # print(s.)
    print('当前CRC输入初始值: ', (s, type(s)))
    test = binascii.crc32(s) & 0xffffffff
    print('算出来的CRC值: ', '0x' + "{:0>8s}".format(str('%x' % test)))
    test = zlib.crc32(s) & 0xffffffff
    print('算出来的CRC值: ', '0x' + "{:0>8s}".format(str('%x' % test)))

    buf_s = [0x00, 0x00, 0x01, 0x90]

    generate_crc32_table()
    crc_stm = get_crc32_val(bytearray(buf_s)) & 0xffffffff
    print('算出来的CRC值:', '0x' + "{:0>8s}".format(str('%x' % crc_stm)))

    reversal_init_crc32_table()
    crc_stm = reversal_getCrc32(bytearray(buf_s)) & 0xffffffff
    print('反转算出来的CRC值:', '0x' + "{:0>8s}".format(str('%x' % crc_stm)))

    # 当前CRC输入初始值： (b'\x00\x00\x01\x90', <class 'bytes'>)
    # 算出来的CRC值: 0xc8507d19
    # 算出来的CRC值: 0xc8507d19
    # 算出来的CRC值: 0xc8507d19
    # 反转算出来的CRC值: 0xc8507d19

