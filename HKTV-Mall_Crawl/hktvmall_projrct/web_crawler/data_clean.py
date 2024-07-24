"""
clean the hktv_product_sales_list
"""
import re

import numpy as np


def clean_hktv_product_sales_list(hktv_product_sales_list):
    sales_list = []
    for item in hktv_product_sales_list:
        if item is None:
            sales_list.append(None)
        else:
            price_match = re.search(r'[\d,]+', str(item))
            if price_match:
                price = price_match.group().replace(',', '')
                sales_list.append(price)
            else:
                sales_list.append(None)
    return sales_list


"""
clean the hktv_product_name_list
"""


def clean_hktv_product_name_list(hktv_product_name_list):
    new_list = []
    for item in hktv_product_name_list:
        result = re.search(r"\s-\s(.*)", item)
        if result:
            new_list.append(result.group(1))
        else:
            new_list.append(item)
    return new_list


"""
clean the hktv_product_discount_price_list
/ hktv_product_price_list
"""

def clean_hktv_product_price_list(hktv_product_price_list):
    new_price_list = []
    for price in hktv_product_price_list:
        if price == np.nan:
            new_price_list.append(None)
        else:
            clean_price = str(price).replace('$', '').strip()
            new_price_list.append(clean_price)
    return new_price_list



"""
clean the hktv_origin_list
"""


def clean_hktv_origin_list(hktv_origin_list):
    origin_list = []
    for origin in hktv_origin_list:
        if origin is None:
            origin_list.append(None)
        else:
            hktv_origin = re.findall(r"\n(.*)", origin)
            if hktv_origin:
                origin_list.append(hktv_origin[2])  # 只获取第一个匹配结果
            else:
                origin_list.append(None)


    return origin_list

if __name__ == '__main__':
    hktv_product_name_list = [
        "大發 - 【30 件】大發鱈魚香絲 8G *9556353920089_30",
        "小牧味屋 - (一箱裝)小牧高鈣奶鹽梳打餅 x 1箱 (12包)",
        "森永 - Pakkuncho 迪士尼朱古力味夾心餅 43g x2 [平行進口] (不同包裝隨機發貨)",
        "有機抹茶餅（盒裝 四顆入）"
    ]

    new_list = clean_hktv_product_name_list(hktv_product_name_list)
    print(new_list)