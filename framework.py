import time
import pymysql
import json
import logging
"""处理动态资源请求的框架程序"""

# 路由列表 模仿django方式开发的
route_list = []



# 带有参数的装饰器
def my_route(path):
    # 装饰器
    def decorator(fn):
        # 当装饰器装饰函数的时候就需要给路由列表添加路由
        route_list.append((path, fn))

        def inner():
            return fn()

        return inner

    return decorator

# 错误页面
@my_route('/error.html')
def error():
    # open() if encoding is not specified the encoding used is platform dependent
    with open("template/error.html", "r", encoding='utf-8') as file:
        file_data = file.read()
    # 状态
    status = "404 Not find"
    # 响应头
    headers = [("Server", "HJ5.0")]

    # 把处理结果进行返回
    return status, headers, file_data

# grand页面
@my_route('/grand.html')
def grand():
    # open() if encoding is not specified the encoding used is platform dependent
    with open("template/grand.html", "r", encoding='utf-8') as file:
        file_data = file.read()
    # 状态
    status = "200 OK"
    # 响应头
    headers = [("Server", "HJ5.0")]

    # 把处理结果进行返回
    return status, headers, file_data
# 获取首页数据
@my_route("/index.html")
def index():
    # 1.读取模板文件数据
    # open() if encoding is not specified the encoding used is platform dependent
    with open("template/index.html", "r",encoding='utf-8') as file:
        file_data = file.read()

    # 2.从数据库查询数据
    conn = pymysql.connect(host="localhost", port=3306,
                    user="root", password="mysql",
                    database="stock_db", charset="utf8")

    # 获取游标
    cursor = conn.cursor()
    # 定义sql
    sql = "select * from info;"
    # 执行sql
    cursor.execute(sql)
    # 获取结果集
    result = cursor.fetchall()
    print(result)

    # 遍历每一条数据，把数据封装程一个tr标签把数据放到td里面
    # 前后端不分离
    data = ""
    for row in result:
        data += '''<tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td><input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000007"></td>
           </tr>''' % row

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

    # 3.把查询的数据插入到模板文件中

    # 状态
    status = "200 OK"
    # 响应头
    headers = [("Server", "HJ5.0")]
    # 这里的data是模板文件数据+数据库里面的数据
    data = file_data.replace("{%content%}", data)
    # 把处理结果进行返回
    return status, headers, data


@my_route("/center_data.html")
def center_data():
    # 2.从数据库查询数据
    conn = pymysql.connect(host="localhost", port=3306,
                           user="root", password="mysql",
                           database="stock_db", charset="utf8")

    # 获取游标
    cursor = conn.cursor()
    try:
        sql = '''select i.code, i.short, i.chg, 
                i.turnover, i.price, i.highs, 
                f.note_info from info as i inner join focus as f 
                on i.id = f.info_id'''
        # 执行sql
        cursor.execute(sql)
        # 获取结果集
        result = cursor.fetchall()
        print(result)
    except Exception as e:
        print('错误信息为：', e)
    finally:
        cursor.close()
        conn.close()

    # 个人中心数据列表
    center_list = list()
    # 遍历每一条记录，把数据转成字典
    for row in result:
        # 把元组转成字典
        center_dict = dict()
        center_dict["code"] = row[0]
        center_dict["short"] = row[1]
        center_dict["chg"] = row[2]
        center_dict["turnover"] = row[3]
        center_dict["price"] = str(row[4])
        center_dict["highs"] = str(row[5])
        center_dict["note_info"] = row[6]
        # 把字典添加到列表
        center_list.append(center_dict)


    # 把列表字典转成json字符串, dumps 不能把Decimal转成json数据
    # ensure_ascii 表示不使用ascii编码
    json_str = json.dumps(center_list, ensure_ascii=False)

    print(json_str)
    # 状态
    status = "200 OK"
    # 响应头
    headers = [("Server", "HJ5.0"), ("Content-Type", "text/html;charset=utf-8")]
    return status, headers, json_str


# 获取个人中心数据
@my_route("/center.html")  # 1. decorator = my_route("/center.html") 2. @decorator
# 3. center =  decorator(center)  cenre = inner
def center():
    # 1.读取模板文件数据
    with open("template/center.html", "r",encoding='utf-8') as file:
        file_data = file.read()
    # 2.从数据库查询数据
    # 3.把查询的数据插入到模板文件中
    data = ""
    # 状态
    status = "200 OK"
    # 响应头
    headers = [("Server", "HJ5.0")]
    # 这里的data是模板文件数据+数据库里面的数据
    data = file_data.replace("{%content%}", data)
    # 把处理结果进行返回
    return status, headers, data


# 处理动态资源不存在的请求, 此函数已不可用，移交到error.html页面
def not_found():
    # 状态
    status = "404 Not Found"
    # 响应头
    headers = [("Server", "HJ5.0")]
    # 响应头
    data = "not found"
    # 把处理结果进行返回
    return status, headers, data


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
        logging.error("没有设置相关路径配置:" + request_path)
        result = not_found()
        return result

if __name__ == '__main__':
    # print(route_list)
    center_data()