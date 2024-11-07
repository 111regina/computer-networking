# udpserver.py
# 服务器端UDP文件传输程序
# 运行环境：
# - Python 3.13.0
# - 操作系统：Windows, Linux
# 配置选项：
# - 服务器监听的IP地址和端口号（默认：127.0.0.1:12000）
# - 服务器可以接收文件并保存到本地（默认保存为 "received_file"）
# 使用方法：
# - 启动此脚本后，服务器将监听指定的端口（默认为12000），等待客户端的文件发送。
# - 接收到的文件内容将被保存到当前目录下的 "received_file" 文件中。
# - 程序会打印接收到的文件内容和每个接收块的详细信息。
#https://github.com/111regina/computer-networking.git
from socket import *

serverName = '127.0.0.1'
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind((serverName, serverPort))
print("服务器已准备好接收数据，监听端口", serverPort)

full_message = ""

# 设置接收超时（单位：秒）
serverSocket.settimeout(10)  # 超过10秒未接收到数据，则抛出TimeoutError

while True:
    try:
        # 接收来自客户端的数据
        message, clientAddress = serverSocket.recvfrom(2048)
        print(f"收到来自 {clientAddress} 的数据块:")

        if message.decode('utf-8') == "EOF":
            print("文件接收完毕，接收到结束标志 EOF。")
            break  # 结束接收

        # 打印接收到的文件内容（部分）
        print(f"当前接收到的文件内容（部分）:")
        print(message.decode())  # 打印接收到的文件内容

        # 拼接接收到的数据
        full_message += message.decode('utf-8')

        # 向客户端发送响应
        serverSocket.sendto("数据接收中".encode(), clientAddress)

    except TimeoutError:
        print("服务器接收超时，没有在规定时间内接收到数据。")
        break

    except Exception as e:
        print(f"服务器发生错误: {e}")
        break

# 保存接收到的文件内容到文件
with open("received_file.txt", "w", encoding='utf-8') as file:
    file.write(full_message)

print("\n文件已保存为 'received_file.txt'.")

serverSocket.close()
