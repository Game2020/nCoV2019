#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyecharts.charts import Bar
from pyecharts import options as opts
from flask import Flask, render_template
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


def bar_china_day_list(china_day_list, last_update_time) -> Bar:
    c = (
        Bar()
        .add_xaxis([item.date for item in china_day_list])
        .add_yaxis("确诊", [item.confirm for item in china_day_list])
        .add_yaxis("疑似", [item.suspect for item in china_day_list])
        .set_global_opts(title_opts=opts.TitleOpts(title="2019 nCoV 确诊/疑似", subtitle=last_update_time))
    )
    return c


def bar_china_day_list_dead(china_day_list, last_update_time) -> Bar:
    c = (
        Bar()
        .add_xaxis([item.date for item in china_day_list])
        .add_yaxis("死亡", [item.dead for item in china_day_list])
        .add_yaxis("治愈", [item.heal for item in china_day_list])
        .set_global_opts(title_opts=opts.TitleOpts(title="2019 nCoV 死亡/治愈", subtitle=last_update_time))
    )
    return c


def model_to_str(model):
    attrs = vars(model)
    return '\t'.join("%s:\t%s" % item for item in attrs.items())


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/china_day_list")
def china_day_list():
    data = fetch_data()
    last_update_time = data.last_update_time
    china_total = data.china_total
    china_day_list = data.china_day_list

    # c = bar_base()
    c = bar_china_day_list(china_day_list, last_update_time)
    return Markup(c.render_embed())


@app.route("/china_day_list_dead")
def china_day_list_dead():
    data = fetch_data()
    last_update_time = data.last_update_time
    china_total = data.china_total
    china_day_list = data.china_day_list

    c = bar_china_day_list_dead(china_day_list, last_update_time)
    return Markup(c.render_embed())


if __name__ == "__main__":
    app.run()
