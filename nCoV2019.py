#-*- coding: utf-8 -*-

# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = n_co_v2019_from_dict(json.loads(json_string))

from datetime import datetime
import dateutil.parser


def from_int(x):
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x):
    assert isinstance(x, str)
    return x


def from_list(f, x):
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_none(x):
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c, x):
    assert isinstance(x, c)
    return x.to_dict()


def from_datetime(x):
    return dateutil.parser.parse(x)


class Today:
    def __init__(self, confirm, suspect, dead, heal):
        self.confirm = confirm
        self.suspect = suspect
        self.dead = dead
        self.heal = heal

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        confirm = from_int(obj.get("confirm"))
        suspect = from_int(obj.get("suspect"))
        dead = from_int(obj.get("dead"))
        heal = from_int(obj.get("heal"))
        return Today(confirm, suspect, dead, heal)

    def to_dict(self):
        result = {}
        result["confirm"] = from_int(self.confirm)
        result["suspect"] = from_int(self.suspect)
        result["dead"] = from_int(self.dead)
        result["heal"] = from_int(self.heal)
        return result


class AreaTree:
    def __init__(self, name, children, total, today):
        self.name = name
        self.children = children
        self.total = total
        self.today = today

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        children = from_union([lambda x: from_list(AreaTree.from_dict, x), from_none], obj.get("children"))
        total = Today.from_dict(obj.get("total"))
        today = Today.from_dict(obj.get("today"))
        return AreaTree(name, children, total, today)

    def to_dict(self):
        result = {}
        result["name"] = from_str(self.name)
        result["children"] = from_union([lambda x: from_list(lambda x: to_class(AreaTree, x), x), from_none], self.children)
        result["total"] = to_class(Today, self.total)
        result["today"] = to_class(Today, self.today)
        return result


class China:
    def __init__(self, date, confirm, suspect, dead, heal):
        self.date = date
        self.confirm = confirm
        self.suspect = suspect
        self.dead = dead
        self.heal = heal

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        date = from_str(obj.get("date"))
        confirm = int(from_str(obj.get("confirm")))
        suspect = int(from_str(obj.get("suspect")))
        dead = int(from_str(obj.get("dead")))
        heal = int(from_str(obj.get("heal")))
        return China(date, confirm, suspect, dead, heal)

    def to_dict(self):
        result = {}
        result["date"] = from_str(self.date)
        result["confirm"] = from_str(str(self.confirm))
        result["suspect"] = from_str(str(self.suspect))
        result["dead"] = from_str(str(self.dead))
        result["heal"] = from_str(str(self.heal))
        return result


class Data:
    def __init__(self, china_total, last_update_time, area_tree, china_day_list):
        self.china_total = china_total
        self.last_update_time = last_update_time
        self.area_tree = area_tree
        self.china_day_list = china_day_list

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        china_total = China.from_dict(obj.get("chinaTotal"))
        last_update_time = from_datetime(obj.get("lastUpdateTime"))
        area_tree = from_list(AreaTree.from_dict, obj.get("areaTree"))
        china_day_list = from_list(China.from_dict, obj.get("chinaDayList"))
        return Data(china_total, last_update_time, area_tree, china_day_list)

    def to_dict(self):
        result = {}
        result["chinaTotal"] = to_class(China, self.china_total)
        result["lastUpdateTime"] = self.last_update_time.isoformat()
        result["areaTree"] = from_list(lambda x: to_class(AreaTree, x), self.area_tree)
        result["chinaDayList"] = from_list(lambda x: to_class(China, x), self.china_day_list)
        return result


class NCoV2019:
    def __init__(self, ret, data):
        self.ret = ret
        self.data = data

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)
        ret = from_int(obj.get("ret"))
        data = Data.from_dict(obj.get("data"))
        return NCoV2019(ret, data)

    def to_dict(self):
        result = {}
        result["ret"] = from_int(self.ret)
        result["data"] = to_class(Data, self.data)
        return result


def n_co_v2019_from_dict(s):
    return NCoV2019.from_dict(s)


def n_co_v2019_to_dict(x):
    return to_class(NCoV2019, x)


def n_data_from_dict(s):
    return Data.from_dict(s)


def n_data_to_dict(x):
    return to_class(Data, x)

