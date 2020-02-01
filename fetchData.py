#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import json
from nCoV2019 import Data, n_data_from_dict


def print_model(m):
    attrs = vars(m)
    print("="*80)
    print('\n'.join("%s:\t%s" % item for item in attrs.items()))


def fetch_html_text(url):
    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res.text
    except:
        print("fetch error")
        return None


def fetch_data():
    china_url = r"https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"

    html_text = fetch_html_text(china_url)

    if html_text is None:
        return

    json_str = json.loads(html_text)
    json_data_str = json_str["data"]
    result = n_data_from_dict(json.loads(json_data_str))

    return result


if __name__ == "__main__":
    data = fetch_data()
    print_model(data)

    china_total = data.china_total
    print_model(china_total)

    last_update_time = data.last_update_time
    print(last_update_time)