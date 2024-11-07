# udp_client.py
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

import argparse
from socket import *

# 设置命令行参数解析器
parser = argparse.ArgumentParser(description="UDP File Transfer Client")
parser.add_argument('server_ip', type=str, help="IP address of the server")
parser.add_argument('server_port', type=int, help="Port number of the server")
parser.add_argument('filename', type=str, help="File to send")
args = parser.parse_args()

serverName = args.server_ip  # 服务器的IP地址
serverPort = args.server_port  # 服务器的端口号
filename = args.filename  # 需要发送的文件路径

# 创建UDP客户端套接字
clientSocket = socket(AF_INET, SOCK_DGRAM)

# 设置接收超时（例如 5 秒）
clientSocket.settimeout(5)

try:
    # 打开文件进行读取（二进制模式）
    with open(filename, 'rb') as file:
        file_content = file.read()

    # 将文件大小发送给服务器，通知服务器开始接收文件
    file_size = len(file_content)
    clientSocket.sendto(f"FILE_SIZE {file_size}".encode(), (serverName, serverPort))

    # 发送文件内容（分块发送）
    chunk_size = 1024  # 每次发送1024字节
    for i in range(0, file_size, chunk_size):
        clientSocket.sendto(file_content[i:i+chunk_size], (serverName, serverPort))

    # 发送结束标志
    clientSocket.sendto(b"END_OF_FILE", (serverName, serverPort))

    # 等待服务器的回应
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print('来自服务器的回应:', modifiedMessage.decode())

except FileNotFoundError:
    print(f"错误: 文件 '{filename}' 未找到。")
except timeout:
    print("等待服务器回应超时，请检查服务器是否正确运行。")
except Exception as e:
    print(f"发生错误: {e}")

finally:
    clientSocket.close()
