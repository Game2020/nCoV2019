#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyecharts.charts import Bar
from pyecharts import options as opts
from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

from nCoV2019 import Data
from fetchData import fetch_data

from pprint import pprint

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

app = Flask(__name__, static_folder="templates")


def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c

def model_to_str(model):
    attrs = vars(model)
    return '\t'.join("%s:\t%s" % item for item in attrs.items())

@app.route("/")
def index():
    data = fetch_data()
    last_update_time = data.last_update_time
    china_total = data.china_total

    c = bar_base()
    return last_update_time + "china_total: " + head + "\n" +  Markup(c.render_embed())


if __name__ == "__main__":
    app.run()
