# -*- coding: utf-8 -*-
import base64
from io import BytesIO
from fontTools.ttLib import TTFont
import requests
import re
import time
import csv
from lxml import etree
import sys
import citydict

def getRetEtree(url, params=None, **kwargs):
    """
        GET请求 url，并返回etree.HTML对象
    """
    res = requests.get(url, params=params, **kwargs)
    return etree.HTML(res.text), res.text

def houseListByHTML(html):
    return html.xpath('.//ul[@class="house-list"]//li')

def houseLocaltion(url, params=None, **kwargs):
    res = getRetEtree(url, params=params, **kwargs)
    local = res.xpath('.//div[@class="view-more-detailmap view-more"]/a/@href')
    print(local, len(local))
    if len(local) < 1:
        return ""
    return local[0]
 
# url = 'https://km.58.com/chuzu/?PGTID=0d100000-0021-d7e2-ad8d-8d1c095b8eec&ClickID=6'
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

def codeb64Str(s):
    def inner():
        return s
    return inner

def empty():
    return ""

codeb64StrFunc=empty

def decode(string):
    font = TTFont(BytesIO(base64.decodebytes(codeb64StrFunc().encode())))
    c = font.getBestCmap()
    ret_list = []
    for char in string:
        decode_num = ord(char)
        if decode_num in c:
            num = c[decode_num]
            num = int(num[-2:])-1
            ret_list.append(num)
        else:
            ret_list.append(char)
    ret_str_show = ''
    for num in ret_list:
        ret_str_show += str(num)
    return ret_str_show


def matchOrEmpty(onehouse, cond):
    ret = onehouse.xpath(cond)
    if (len(ret) < 1):
        return ""
    return ret[0]

def houseInfo(hlist):
    ret = []
    for one in hlist:
        title = matchOrEmpty(one,'.//div[@class="des"]/h2/a/text()').strip()
        title = decode(title)
        price = matchOrEmpty(one,'.//div[@class="money"]/b/text()')
        price = decode(price)
        adress = matchOrEmpty(one,'.//div[@class="des"]/p/a/text()')
        adress = decode(adress)
        houseInfoURL = matchOrEmpty(one,'.//div[@class="des"]/h2/a/@href')
        # print(houseInfoURL)
        # print(title)
        # print(price)
        # print(adress)
        # [房源名称，地址，月租，房源url地址]
        content = [title, adress, price, houseInfoURL]
        # 判断是否为空
        flag = False
        for i in range(len(content)):
            if content[i] == 0:
                flag = True
                break
        if flag:
            continue
        time.sleep(2)
        # s = ",".join(content)
        ret.append(content)
    return ret


def writeCSV(filename,hlist):
    csv_file = open(filename,"a+")
    csv_writer = csv.writer(csv_file, delimiter=",")
    for i in range(len(hlist)):
        csv_writer.writerow(hlist[i])
    csv_file.close()
    return

# 第一页 https://km.58.com/chuzu/
# 第二页 https://km.58.com/chuzu/pn2
# 第三页 https://km.58.com/chuzu/pn3
# kunming58URL='https://km.58.com/chuzu/'
def page(pageURL, filename):
    html, text = getRetEtree(pageURL, headers=headers)
    bstr = re.findall("charset=utf-8;base64,(.*?)'\)", text)
    if (len(bstr) <1):
        return
    global codeb64StrFunc
    codeb64StrFunc = codeb64Str(bstr[0])
    hlist = houseListByHTML(html)
    content = houseInfo(hlist)
    if (len(hlist) < 1):
        print(pageURL,"获取失败")
        return
    # 写入csv
    writeCSV(filename, content)

def pageInit(url, filename):
    print("fetch ", url, " ...", " save to", filename)
    _, text = getRetEtree(url, headers=headers)
    nums = re.findall(" . . . <a href=.*?\><span>(.*?)</span>", text)
    if (len(nums) < 1):
        print("页数获取失败")
        return
    num = int(nums[0])
    #计算页数
    print("crawl", url, "."*6, "共", num,"页")
    page(url, filename)
    for i in range(num-1):
        time.sleep(5)
        url = url+"{0}{1}".format("pn", i+1)
        print("crawl", url,"."*6, "第", i+1, "页")
        page(url, filename)


def tips():
    tip="""
    此文件只是用来爬取数据的
    ex：
    最小力度为市：
        python crawl.py 北京[市]
        python crawl.py 昆明[市]
        python crawl.py 云南[省] 昆明[市]
    """
    print(tip)
    exit()


chuzu = "https://{0}.58.com/chuzu/"
def matchCity(c):
    for (k, v) in  citydict.cityList.items():
        for (k2, v2) in v.items():
            if k2 == c | k2 == c[:-2]:
                v2 = v2.split("|")
                return chuzu.format(v2[0]),v2[0]
    return ""

def matchCityV2(p, c):
    p2 = citydict.cityList[p]
    if (not p2) & (len(p) > 1):
        p2 = citydict.cityList[p[:-2]]
    if not p2:
        tips()
    c2 = p2[c]
    if (not c2) & (len(c) > 1):
        c2 = p2[c[:-2]]
    if not c2:
        tips()
    v2 = c2.split("|")
    return chuzu.format(v2[0]),v2[0]

if __name__ == "__main__":
    if (len(sys.argv[1:]) < 1 ):
        tips()
    city = sys.argv[1]
    province = ""
    if (len(sys.argv[1:]) > 1):
        province = sys.argv[1]
        city = sys.argv[2]
    
    url = ""
    if province== "":
        url = matchCity(city)
    else:
        url = matchCityV2(province, city)
    
    print(url[0], url[1])
    pageInit(url[0], url[1]+".csv")


""" csv
[房源名称，地址，月租，房源url地址]。
"""



