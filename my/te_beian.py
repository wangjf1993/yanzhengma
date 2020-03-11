import random
import re

import requests
from redis import Redis

import execjs


def get_random_proxy():
    """
    代理
    :return:
    """
    # REDIS_HOST = '222.212.90.13'
    # REDIS_PORT = 6579
    REDIS_DB = 7

    REDIS_HOST = '192.168.5.242'
    REDIS_PORT = 6379
    REDIS_DB = 7

    REDIS_PASSWORD = 'Gouuse@spider'
    redis_1 = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB,
                    password=REDIS_PASSWORD)
    while True:
        try:
            proxies_values = redis_1.lpop('proxy10').decode()
            break
        except:
            pass
    # proxies_values='121.232.194.66:41888'
    return proxies_values


value = get_random_proxy()
print(value)
proxies = {
    'http': 'http://' + value,
    'https': 'https`://' + value
}
headers={
'Host': 'www.miitbeian.gov.cn',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer': 'http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_showPage.action',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
}

url='http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_showPage.action'

print(proxies)
t=requests.get(url,headers=headers,allow_redirects=False,proxies=proxies)
print(proxies)


def get_cookie(response):
    __jsluid = response.headers["Set-Cookie"].split(';')[0]
    # 一级解密
    resp_body = response.content.decode('utf-8')

    get_js = re.findall(r'<script>(.*?)</script>', resp_body)[0]
    get_js_1 = get_js.replace('while(z++)try{eval', 'while(z++)try{return')
    resHtml = "function getClearance(){" + get_js_1 + "};"
    ctx = execjs.compile(resHtml)
    # 二级级解密结果
    temp1 = ctx.call('getClearance')
    # 提取二级js函数
    function_text = temp1.split('cookie')[1].split("Path=/;'")[0] + "Path=/;'"
    t1 = function_text.split('function()')[0]
    tt = function_text.split('function()')[1].split(')()+')
    js_function = 'function getClearance()' + tt[0]
    ctx = execjs.compile(js_function)
    # 二级解密结果
    temp1 = ctx.call('getClearance')
    jsl_clearance = t1 + temp1
    jsl_clearance = jsl_clearance.replace("='", '')
    jsl_clearance = jsl_clearance.replace("'+(", '')
    print(jsl_clearance)
    return __jsluid+';'+jsl_clearance
# __jsluid = t.headers["Set-Cookie"].split(';')[0]
# # 一级解密
# resp_body=t.content.decode('utf-8')
#
# get_js = re.findall(r'<script>(.*?)</script>', resp_body)[0]
# get_js_1=get_js.replace('while(z++)try{eval','while(z++)try{return')
# y=get_js.split('eval')
# resHtml = "function getClearance(){" + get_js_1 + "};"
# ctx = execjs.compile(resHtml)
# # 二级级解密结果
# temp1 = ctx.call('getClearance')
# t = temp1.split('cookie')[1].split("Path=/;'")[0]+"Path=/;'"
# t1=t.split('function()')[0]
# tt=t.split('function()')[1].split(')()+')
# t='function getClearance()'+tt[0]
# ctx = execjs.compile(t)
# # 二级解密结果
# temp1 = ctx.call('getClearance')
# jsl_clearance=t1+temp1
# jsl_clearance=jsl_clearance.replace("='",'')
# jsl_clearance=jsl_clearance.replace("'+(",'')
# print(jsl_clearance)
cookie=get_cookie(t)

headers={
'Host': 'www.miitbeian.gov.cn',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer': 'http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_showPage.action',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie':cookie
}
s=requests.session()
print(proxies)
t=s.get(url,headers=headers,allow_redirects=False,proxies=proxies)
print(t.status_code)
t=s.get('http://www.miitbeian.gov.cn/getVerifyCode?%s'%random.randint(1,100),headers=headers,proxies=proxies)
print(t.status_code)

