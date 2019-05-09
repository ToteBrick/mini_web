import socket
import threading
import sys
import framework


# 定义web服务器类
class HttpWebServer(object):
    def __init__(self, port):
        # 创建tcp服务端套接字
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口号复用, 程序退出端口立即释放
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定端口号
        tcp_server_socket.bind(("", port))
        # 设置监听
        tcp_server_socket.listen(128)
        # 保存创建成功的服务器套接字
        self.tcp_server_socket = tcp_server_socket

    # 处理客户端的请求
    @staticmethod
    def handle_client_request(new_socket):
        # 代码执行到此，说明连接建立成功
        recv_client_data = new_socket.recv(4096)
        if len(recv_client_data) == 0:
            print("关闭浏览器了")
            new_socket.close()
            return

        # 对二进制数据进行解码
        recv_client_content = recv_client_data.decode("utf-8")
        print(recv_client_content)
        # 根据指定字符串进行分割， 最大分割次数指定2
        request_list = recv_client_content.split(" ", maxsplit=2)

        # 获取请求资源路径
        request_path = request_list[1]
        print(request_path)

        # 判断请求的是否是根目录，如果条件成立，指定首页数据返回
        if request_path == "/":
            request_path = "/index.html"

        # 判断请求的资源路径的后缀是否是.html
        # 如果是.html那么就是动态资源请求
        # 如果不是.html那么就任务是静态资源请求

        if request_path.endswith(".html"):
            """动态资源请求"""
            # 动态资源请求交给web框架处理
            # 准备给web框架程序的数据, 最主要的是请求路径，后续框架有可能还需要请求头信息
            env = {
                "request_path": request_path,
                # 假如框架需要请求头信息信息，可以在额外增加对应的键值对信息即可
            }
            # 处理结果应该返回的信息有:
            # 1.状态信息status 2. 响应头信息headers 3. 处理结果(响应体)response_data
            status, headers, data = framework.handle_request(env)

            # 响应行
            response_line = "HTTP/1.1 %s\r\n" % status
            # 遍历响应头信息[("Server", "PWS5.0")]
            response_header = ""
            for header in headers:
                # header是一个元组，格式化占位符要是有多个，可以使用元组方式进行传参
                # “%s %s” % ('ab', 'bc')
                response_header += "%s: %s\r\n" % header

            # web服务器把处理后的结果拼接程一个http的响应报文发送给浏览器
            response_data = (response_line + response_header +
                             "\r\n" + data).encode("utf-8")

            # 把服务器发送的数据发给浏览器
            new_socket.send(response_data)
            # 关闭套接字
            new_socket.close()

        else:
            """静态资源请求"""
            try:
                # 动态打开指定文件
                with open("static" + request_path, "rb") as file:
                    # 读取文件数据
                    file_data = file.read()
            except Exception as e:
                # 请求资源不存在，返回404数据
                # 响应行
                response_line = "HTTP/1.1 404 Not Found\r\n"
                # 响应头
                response_header = "Server: HJ1.0\r\n"
                with open("../template/error.html", "rb") as file:
                    file_data = file.read()
                # 响应体
                response_body = file_data

                # 拼接响应报文
                response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body
                # 发送数据
                new_socket.send(response_data)
            else:
                # 响应行
                response_line = "HTTP/1.1 200 OK\r\n"
                # 响应头
                response_header = "Server: HJ1.0\r\n"

                # 响应体
                response_body = file_data

                # 拼接响应报文
                response_data = (response_line + response_header + "\r\n").encode("utf-8") + response_body
                # 发送数据
                new_socket.send(response_data)
            finally:
                # 关闭服务与客户端的套接字
                new_socket.close()

    # 启动web服务器进行工作
    def start(self):
        while True:
            # 等待接受客户端的连接请求
            new_socket, ip_port = self.tcp_server_socket.accept()
            # 当客户端和服务器建立连接程，创建子线程
            sub_thread = threading.Thread(target=self.handle_client_request, args=(new_socket,))
            # 设置守护主线程
            sub_thread.setDaemon(True)
            # 启动子线程执行对应的任务
            sub_thread.start()


# 程序入口函数
def main():

    web_server = HttpWebServer(9000)
    # 启动web服务器进行工作
    web_server.start()


if __name__ == '__main__':
    main()
