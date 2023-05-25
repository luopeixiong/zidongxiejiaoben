# -*- coding: utf-8 -*-
from ..items import *


class Spider(scrapy.Spider):
    mun = 0
    zuihou_time = 999
    shi = shi()

    name = ''
    items_cource = ''  # 不要加前面数字
    lei_ming = ''
    headers = {'Content-Type': ''}

    start_datas = []
    allowed_domains = []