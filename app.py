#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyecharts.charts import Bar, Map, Pie
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


def map_area_tree(china_nodes, last_update_time) -> Map:
    c = (
        Map(init_opts=opts.InitOpts(width="6"))
        .add(
            "全国确诊",
            [[node.name, node.total.confirm] for node in china_nodes]
        )
        .add(
            "疑似病例",
            [[node.name, node.total.suspect] for node in china_nodes]
        )
        .add(
            "死亡人数",
            [[node.name, node.total.dead] for node in china_nodes]
        )
        .add(
            "痊愈人数",
            [[node.name, node.total.heal] for node in china_nodes]
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(min_=-1000, max_=1000, border_color="#ccc", border_width=2,
                                              background_color="#eee",

                                              range_color=[
                                                  "lightskyblue", "lightyellow", "red"],
                                              range_opacity=0.5),
            title_opts=opts.TitleOpts(title="{} {}".format("", last_update_time)),
        )
    )
    return c


def map_province_area_tree(province_nodes, last_update_time) -> Map:
    c = (
        Map(init_opts=opts.InitOpts())
        .add(
            "确诊",
            [["{}{}".format(node.name, "市"), node.total.confirm] for node in province_nodes],
            maptype="湖北",
        )
        .add(
            "疑似病例",
            [["{}{}".format(node.name, "市"), node.total.suspect] for node in province_nodes],
            maptype="湖北",
        )
        .add(
            "死亡人数",
            [["{}{}".format(node.name, "市"), node.total.dead] for node in province_nodes],
            maptype="湖北",
        )
        .add(
            "痊愈人数",
            [["{}{}".format(node.name, "市"), node.total.heal] for node in province_nodes],
            maptype="湖北",
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(min_=-1000, max_=1000, border_color="#ccc", border_width=2,
                                              background_color="#eee",

                                              range_color=[
                                                  "lightskyblue", "lightyellow", "red"],
                                              range_opacity=0.5),
            title_opts=opts.TitleOpts(title="{} {}".format("湖北", last_update_time)),
        )
    )
    return c


def pie_area_tree(china_nodes, last_update_time) -> Pie:
    c = (
        Pie()
        .add(
            last_update_time,
            [[node.name, node.total.confirm] for node in china_nodes],
            radius=["40%", "75%"],
            rosetype="area",
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=" "),
            legend_opts=opts.LegendOpts(
                orient="vertical", pos_top="15%", pos_left="2%"
            ),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c


def dead_pie_area_tree(total, title) -> Pie:
    c = (
        Pie()
        .add(
            title,
            total,
            radius=["40%", "75%"],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=" "),
            legend_opts=opts.LegendOpts(
                orient="vertical", pos_top="15%", pos_left="2%"
            ),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c


def bar_china_day_list(china_day_list, last_update_time) -> Bar:
    c = (
        Bar()
        .add_xaxis([item.date for item in china_day_list])
        .reversal_axis()
        .add_yaxis("确诊", [item.confirm for item in china_day_list])
        .add_yaxis("疑似", [item.suspect for item in china_day_list])
        .set_global_opts(title_opts=opts.TitleOpts(title="2019 nCoV 确诊/疑似", subtitle=last_update_time))
    )
    return c


def bar_china_day_list_dead(china_day_list, last_update_time) -> Bar:
    c = (
        Bar()
        .add_xaxis([item.date for item in china_day_list])
        .reversal_axis()
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


@app.route("/bar")
def bar():
    c = bar_base()
    return Markup(c.render_embed())


@app.route("/area_tree")
def area_tree():
    data = fetch_data()
    last_update_time = data.last_update_time
    area_tree = data.area_tree
    china_nodes = area_tree[0].children

    c = map_area_tree(china_nodes, last_update_time)
    return Markup(c.render_embed())


@app.route("/hubei_area_tree")
def hubei_area_tree():
    data = fetch_data()
    last_update_time = data.last_update_time
    area_tree = data.area_tree
    china_nodes = area_tree[0].children
    hubei_nodes = china_nodes[0].children

    c = map_province_area_tree(hubei_nodes, last_update_time)
    return Markup(c.render_embed())


@app.route("/pie")
def area_tree_pie():
    data = fetch_data()
    last_update_time = data.last_update_time
    area_tree = data.area_tree
    china_nodes = area_tree[0].children

    c = pie_area_tree(china_nodes, last_update_time)
    return Markup(c.render_embed())


@app.route("/dead_pie")
def dead_area_tree_pie():
    data = fetch_data()
    last_update_time = data.last_update_time
    china_total = data.china_total

    total = [["未治愈人数", china_total.confirm - china_total.heal - china_total.dead],
         ["治愈人数", china_total.heal], ["死亡人数", china_total.dead]]

    c = dead_pie_area_tree(total, last_update_time)
    return Markup(c.render_embed())


@app.route("/china_day_list")
def china_day_list():
    data = fetch_data()
    last_update_time = data.last_update_time
    china_total = data.china_total
    china_day_list = data.china_day_list

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
