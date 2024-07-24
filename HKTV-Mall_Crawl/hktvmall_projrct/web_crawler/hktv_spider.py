import threading
import time
from wsgiref import headers
import numpy as np
import requests
import json
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from hktvmall_projrct.config_data import UA_HEADERS
from .data_clean import clean_hktv_origin_list, clean_hktv_product_name_list, clean_hktv_product_price_list, \
    clean_hktv_product_sales_list
import re


class HKTV_Spider:

    def __init__(self):
        self.url_list = []
        self.driver = webdriver.Chrome()
        self.hktv_origin_list = []
        self.hktv_product_sales_list = []
        self.hktv_product_name_list = []
        self.hktv_product_discount_price_list = []
        self.hktv_product_delivery_date_list = []
        self.hktv_brand_store_rating_list = []
        self.hktv_product_package_list = []
        self.hktv_product_rating_list = []
        self.hktv_product_rating_num_list = []
        self.hktv_product_price_list = []
        self.hktv_product_brand_list = []

        
    def spider(self, url_list):
        i = 0
        # 循環所有url 爬取每個url的數據
        # print(f'Thread{threading.current_thread().name}started with arg:{arg}')
        # time.sleep(2)
        # print(f'Thread{threading.current_thread().name}started with arg:"finished"')

        # clean data
        self.hktv_product_sales_list = clean_hktv_product_sales_list(self.hktv_product_sales_list)

        self.hktv_product_name_list = clean_hktv_product_name_list(self.hktv_product_name_list)

        self.hktv_product_price_list = [str(price) for price in self.hktv_product_price_list]
        self.hktv_product_price_list = clean_hktv_product_price_list(self.hktv_product_price_list)

        self.hktv_product_discount_price_list = clean_hktv_product_price_list(self.hktv_product_discount_price_list)

        self.hktv_origin_list = clean_hktv_origin_list(self.hktv_origin_list)

        # convert to df and return

        df = pd.DataFrame({
            'product_url': self.url_list,
            'product_name': self.hktv_product_name_list,
            'product_package': self.hktv_product_package_list,
            'product_sales': self.hktv_product_sales_list,
            'product_num_of_raters': self.hktv_product_rating_num_list,
            'product_delivery_date': self.hktv_product_delivery_date_list,
            'product_brand': self.hktv_product_brand_list,
            'product_price': self.hktv_product_price_list,
            'product_discount_price': self.hktv_product_discount_price_list,
            'product_rating': self.hktv_product_rating_list,
            'product_origin': self.hktv_origin_list,
            'brand_store_rating': self.hktv_brand_store_rating_list
        })
        return df
