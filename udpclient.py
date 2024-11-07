# udpclient.py
# 客户端UDP文件传输程序
# 运行环境：
# - Python 3.13.0
# - 操作系统：Windows, Linux
# 配置选项：
# - 服务器IP地址和端口号（从命令行参数传入）
# - 需要发送的文件路径（从命令行参数传入）
# 使用方法：
# - 运行此脚本后，客户端会将指定路径的文件通过UDP协议发送到服务器。
# - 向服务器发送文件大小信息后，文件内容会被分块发送。
# - 服务器成功接收文件后，客户端将收到来自服务器的确认信息。
#https://github.com/111regina/computer-networking.git
import argparse
from socket import *
import time

# 设置命令行参数解析器
parser = argparse.ArgumentParser(description="UDP File Transfer Client")
parser.add_argument('server_ip', type=str, help="IP address of the server")
parser.add_argument('server_port', type=int, help="Port number of the server")
parser.add_argument('filename', type=str, help="File to send")
args = parser.parse_args()

serverName = args.server_ip
serverPort = args.server_port
filename = args.filename

# 创建UDP客户端套接字
clientSocket = socket(AF_INET, SOCK_DGRAM)

# 设置接收超时（单位：秒）
clientSocket.settimeout(5)  # 超过5秒未接收到服务器的响应，则抛出TimeoutError

try:
    # 打开文件进行读取
    with open(filename, 'r', encoding='utf-8') as file:
        file_content = file.read()

    # 分段发送
    buffer_size = 1024  # 每次发送1KB
    for i in range(0, len(file_content), buffer_size):
        chunk = file_content[i:i + buffer_size]
        clientSocket.sendto(chunk.encode('utf-8'), (serverName, serverPort))
        print(f"发送数据块: {chunk[:100]}...")  # 打印发送的数据块（前100个字符）

    # 发送结束标志
    clientSocket.sendto("EOF".encode('utf-8'), (serverName, serverPort))
    print("文件发送完成，发送结束标志 EOF。")

    # 等待服务器的回应
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)  # 接收响应
    print('来自服务器的回应:', modifiedMessage.decode())

except FileNotFoundError:
    print(f"错误: 文件 '{filename}' 未找到。")

except TimeoutError:
    print("错误: 超过指定时间没有收到服务器的响应。")

finally:
    clientSocket.close()
