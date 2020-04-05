# -*- coding: utf-8 -*-

url = "https://www.58.com/changecity.html?catepath=chuzu&catename=%E5%87%BA%E7%A7%9F&fullpath=1,37031&PGTID=0d3090a7-0021-df75-555d-ab0ab4718511&ClickID=5"
headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control':'max-age=0',
    'cookie':'f=n; commontopbar_new_city_info=541%7C%E6%98%86%E6%98%8E%7Ckm; commontopbar_ipcity=xuanhan%7C%E5%AE%A3%E6%B1%89%7C0; userid360_xml=C5CCCC32810763013C6516E934D472A1; time_create=1588491018977; myLat=""; myLon=""; id58=h6MO6l6GkxIPvDlJN+cUrg==; mcity=xuanhan; 58tj_uuid=1755d697-493e-4178-8f15-654f69a692dc; als=0; wmda_uuid=209e578c0ebf2a3b862dc046acf8d422; wmda_new_uuid=1; wmda_visited_projects=%3B11187958619315; xxzl_deviceid=KLp7hrXpSv55HfRFu0vZ6lY9Dmr18hzFWJibDfGn%2B4oR%2FvZtU2am9Av2wABcC3Aq; Hm_lvt_ae019ebe194212c4486d09f377276a77=1585899009; Hm_lpvt_ae019ebe194212c4486d09f377276a77=1585899009; f=n; commontopbar_new_city_info=541%7C%E6%98%86%E6%98%8E%7Ckm; city=km; 58home=km; commontopbar_ipcity=xuanhan%7C%E5%AE%A3%E6%B1%89%7C0; Hm_lvt_dcee4f66df28844222ef0479976aabf1=1585908296; Hm_lpvt_dcee4f66df28844222ef0479976aabf1=1585908296; new_uv=4; utm_source=; spm=; wmda_session_id_11187958619315=1585910397642-081273dd-42f7-cb8c; new_session=0; xzfzqtoken=5e%2ByBHvDgFDmc6mhB4%2BQFszXJ8hq8KJUV8G4n1Uc8f%2BJeFHnGV57EC%2FbvY2fb6S1in35brBb%2F%2FeSODvMgkQULA%3D%3D; init_refer=https%253A%252F%252Fwww.shiyanlou.com%252Fcourses%252F599%252Flearning%252F; ppStore_fingerprint=C6952153A9FD9444D324EA48597F8065286DA113ACE99431%EF%BC%BF1585911319389; xxzl_cid=72f9ec92442a46889487f11b9eb74446; xzuid=3df1d8ca-9376-4add-9e8d-fef44b916012',
    'referer':'https://km.58.com/',
    'sec-fetch-dest':'document',
    'sec-fetch-mode':'navigate',
    'sec-fetch-site':'same-origin',
    'sec-fetch-user':'?1',
    'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

import base64
from io import BytesIO
# from fontTools.ttLib import TTFont
import requests
import re
import time
import csv
from lxml import etree


if __name__ == "__main__":
    crawlCity()