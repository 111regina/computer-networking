# udp_server.py
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

from socket import *

serverName = '127.0.0.1'
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# 绑定到指定的 IP 和端口
serverSocket.bind((serverName, serverPort))
print("服务器已准备好接收数据，监听端口", serverPort)

while True:
    try:
        # 接收来自客户端的文件大小信息
        message, clientAddress = serverSocket.recvfrom(2048)
        if message.decode().startswith("FILE_SIZE"):
            # 获取文件大小
            file_size = int(message.decode().split()[1])
            print(f"准备接收文件，文件大小: {file_size} 字节")

        # 初始化文件接收
        received_data = b''  # 存储接收到的数据

        # 接收文件内容（分块接收）
        while True:
            # 接收数据块
            message, clientAddress = serverSocket.recvfrom(1024)
            if message == b"EOF":
                print("接收完毕，文件传输结束")
                break  # 文件接收完毕
            received_data += message  # 将数据块拼接起来

        # 将接收到的文件内容保存到本地
        with open("received_file", 'wb') as f:
            f.write(received_data)
        print("文件保存成功")

        # 向客户端发送响应
        serverSocket.sendto("文件接收成功".encode(), clientAddress)

        # 文件接收和保存成功后关闭进程
        break  # 退出服务器循环

    except Exception as e:
        print(f"服务器发生错误: {e}")
        break  # 出现错误时退出循环

# 关闭服务器套接字
serverSocket.close()
print("服务器已关闭")
