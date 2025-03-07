import serial
import time
# import tkinter as tk

class testPotCirc_oscillation():
    def __init__(self,SERIAL_PORT = 'COM4',BAUD_RATE = 38400,TIMEOUT = 1,SERIAL_VAR = {"DATA_BITS":8,"STOP_BITS":2,"PARITY":serial.PARITY_NONE}):

        # 串口设置
        DATA_BITS = SERIAL_VAR["DATA_BITS"]       # 数据位，常见的有 7 或 8
        STOP_BITS = SERIAL_VAR["STOP_BITS"]       # 停止位，常见的有 1、1.5 或 2
        PARITY = SERIAL_VAR["PARITY"]  # 校验位，常见的有 NONE、EVEN、ODD 等
        
        # 打开串口
        self.ser = serial.Serial(
            SERIAL_PORT,
            BAUD_RATE,
            timeout=TIMEOUT,
            bytesize=DATA_BITS,
            stopbits=STOP_BITS,
            parity=PARITY
        )
        
        if self.ser.isOpen():
            print(f"串口 {SERIAL_PORT} 打开成功，波特率：{BAUD_RATE}，数据位：{DATA_BITS}，停止位：{STOP_BITS}，校验位：{PARITY}")

# 发送数据，数据以16进制字节流形式传输
    def send_data(self,data):
        # 先将16进制字符串转换为字节
        data_bytes = bytes.fromhex(data)
        # print(f"发送数据: {data}")
        self.ser.write(data_bytes)  # 发送字节数据

# 接收数据，将接收到的数据以16进制显示
    def receive_data(self):
        while True:
            if self.ser.in_waiting > 0:  # 如果有数据待接收
                received_data = self.ser.read(self.ser.in_waiting)  # 读取所有可用的数据
                result = self.hex2data(received_data)
                return result
            time.sleep(0.1)

    def hex2data(self,received_data):
        data_hex_str = ' '.join(f'{byte:02X}' for byte in received_data)
        data_hex_li = data_hex_str.split(" ")
        numb = int(self.hex2decimal(f"{data_hex_li[5]}{data_hex_li[6]}"))/1000
        return (numb if data_hex_li[3]=="00" else -numb)
    
    def hex2decimal(self,hex_string):
        # 去掉16进制字符串中的空格
        hex_string = hex_string.replace(" ", "")
        # 将16进制字符串转换为10进制数
        decimal_value = int(hex_string, 16)
        return decimal_value
# try:
#     send_data("01 03 00 00 00 02 C4 0B")  # 发送16进制数据
#     receive_data()  # 开始接收数据
# except KeyboardInterrupt:
#     print("程序中断")
# finally:
#     ser.close()  # 关闭串口
#     print("串口已关闭")

