from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts.charts import Gauge, Page

app = Flask(__name__, static_folder="templates")

# 柱形图
def bar_base() -> Bar:
    c = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
            .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c


# 各个城市招聘情况
city_nms_top10 = ['北京', '上海', '深圳', '成都', '广州', '杭州', '武汉', '南京', '苏州', '郑州']
city_nums_top10 = [149, 95, 77, 22, 17, 17, 16, 13, 7, 5]

# 饼图
def pie_base() -> Pie:
    c = (
        Pie()
            .add("", [list(z) for z in zip(city_nms_top10, city_nums_top10)])
            .set_global_opts(title_opts=opts.TitleOpts(title="招聘情况"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c

# radius 饼图
def pie_radius() -> Pie:
    c = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(city_nms_top10, city_nums_top10)],
            radius=["40%", "75%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Python岗位"),
            legend_opts=opts.LegendOpts(
                orient="vertical", pos_top="15%", pos_left="2%"
            ),
        )
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{a}: {b}"))
    )
    return c

# 仪表盘
def gauge_base() -> Gauge:
    c = (
        Gauge()
            .add("", [("完成率", 66.6)])
            .set_global_opts(title_opts=opts.TitleOpts(title="Gauge"))
    )
    return c


@app.route("/")
def index():
    c = bar_base()
    return Markup(c.render_embed())


@app.route("/pie")
def pie():
    c = pie_base()
    return Markup(c.render_embed())


@app.route("/radius")
def radius():
    c = pie_radius()
    return Markup(c.render_embed())


@app.route("/gauge")
def gauge():
    c = gauge_base()
    return Markup(c.render_embed())


if __name__ == "__main__":
    app.run()
