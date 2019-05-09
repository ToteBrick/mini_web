import time
"""处理动态资源请求的框架程序"""


# 获取首页数据
def index():
    # 1.读取模板文件数据
    with open("../template/index.html", "r",encoding='utf-8') as file:
        file_data = file.read()

    # 2.从数据库查询数据
    # 3.把查询的数据插入到模板文件中

    # 模拟返回的数据库数据
    data = time.ctime()

    # 状态
    status = "200 OK"
    # 响应头
    headers = [("Server", "HJ5.0")]
    # 这里的data是模板文件数据+数据库里面的数据
    data = file_data.replace("{%content%}", data)
    # 把处理结果进行返回
    return status, headers, data


# 获取个人中心数据
def center():
    # 1.读取模板文件数据
    with open("../template/center.html", "r",encoding='utf-8') as file:
        file_data = file.read()

    # 2.从数据库查询数据
    # 3.把查询的数据插入到模板文件中

    # 模拟返回的数据库数据
    data = time.ctime()

    # 状态
    status = "200 OK"
    # 响应头
    headers = [("Server", "PWS5.0")]
    # 这里的data是模板文件数据+数据库里面的数据
    data = file_data.replace("{%content%}", data)
    # 把处理结果进行返回
    return status, headers, data


# 处理动态资源不存在的请求
def not_found():
    # 状态
    status = "404 Not Found"
    # 响应头
    headers = [("Server", "PWS5.0")]
    # 响应头
    data = "not found"
    # 把处理结果进行返回
    return status, headers, data

# 路由列表 模仿django方式开发
route_list = [
    ("/index.html", index),
    ("/center.html", center)
]


# 处理动态资源请求的函数
def handle_request(env):
    # 通过key取值
    request_path = env["request_path"]
    print("接收到的动态资源路径是:", request_path)

    # 遍历路由列表，根据请求的动态资源逻辑获取处理的请求函数
    for path, func in route_list:
        if request_path == path:
            # 处理动态资源请求需要的数据
            result = func()
            # 把处理后的结果返回给web服务器
            return result
    else:
        # 404,没有找到url对应的处理函数
        result = not_found()
        return result

    # if request_path == "/index.html":
    #     # 使用index函数处理动态资源请求需要的数据
    #     result = index()
    #     # 把处理后的结果返回给web服务器
    #     return result
    # elif request_path == "/center.html":
    #     result = center()
    #     return result
    # else:
    #     # 404
    #     result = not_found()
    #     return result