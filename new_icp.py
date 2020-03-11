import re

import execjs
import requests
from redis import Redis

headers={
    'Host': 'www.miitbeian.gov.cn',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cookie': '__jsluid=7b548afe06d2c22be83b927c800bfdba; __jsl_clearance=1546848698.493|0|RrcyhGE70SjtdUm%2FOAT%2B3pMijPo%3D; JSESSIONID=ZBknZy6eEb_rw7o3G36_D85VjS4P6SXkWKZ8xq7Ghb9vrqGbHjFH!507975912'
}
url = "http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_showPage.action"

def get_random_proxy():
    """
    代理
    :return:
    """
    REDIS_HOST = '192.168.5.242'
    REDIS_PORT = 6379
    REDIS_DB = 7
    REDIS_PASSWORD = 'Gouuse@spider'
    redis_1 = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB,
                    password=REDIS_PASSWORD)
    while True:
        try:
            proxies_values = redis_1.lpop('proxy4').decode()
            break
        except:
            pass
    print(proxies_values)
    return proxies_values
value = get_random_proxy()
proxies = {'http': 'http://' + re.findall('.*?([\d].*)', value)[0],
           'https': 'https://' + re.findall('.*?([\d].*)', value)[0]}
s=requests.session()
url='http://www.miitbeian.gov.cn/publish/query/indexFirst.action'
# rep=s.get(url,headers=headers,verify=False,allow_redirects=False,proxies=proxies)

response=s.get(url,headers=headers,verify=False,allow_redirects=False,proxies=proxies)
resp_body=response.content.decode('utf-8')
__jsluid = response.headers["Set-Cookie"].split(';')[0]
cookie1 = __jsluid
print(cookie1)
# 解密

get_js = re.findall(r'<script>(.*?)</script>', resp_body)[0].replace('eval', 'return')
resHtml = "function getClearance(){" + get_js + "};"
print(resHtml)
ctx = execjs.compile(resHtml)
# 一级解密结果
temp1 = ctx.call('getClearance')
# temp1=js2py.eval_js(resHtml)
print(temp1)


s = 'var a' + temp1.split('cookie')[1].split("Path=/;'")[0]+"Path=/;'"
print(s)
# print s
resHtml = "function getClearance(){" + s + "};"
print(resHtml)
#
ctx = execjs.compile(resHtml)
print(ctx)
# 二级解密结果
jsl_clearance = ctx.call('getClearance')

print(jsl_clearance)
jsl_clearance =jsl_clearance.split(';')[0]
print(jsl_clearance)

headers={
    'Host': 'www.miitbeian.gov.cn',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': f'__jsluid={cookie1}'
}
s.get(url,headers=headers,proxies=proxies)

# j="""
# function getClearance(){var a='__jsl_clearance=1546932154.184|0|'+(function(){var _2v=[(-~~~[]-~[-~{}+((-~[]<<-~[]))*[(-~[]<<-~[])]]+[[]][0]),[-~!{}-~(+!'')-~((-~[]<<-~[])+(-~[]<<-~[]))],(-~[2]+[]+[[]][0]),((+!'')+(+!'')+[[]][0])+((+!'')+(+!'')+[[]][0]),(-~!{}+[]+[[]][0])+(-~!{}+[]+[[]][0]),(-~!{}+[]+[[]][0])+[~~[]],[2+3],(4+[]+[]),(-~!{}+[]+[[]][0])+(-~~~[]-~[-~{}+((-~[]<<-~[]))*[(-~[]<<-~[])]]+[[]][0]),(-~!{}+[]+[[]][0])+(-~[2]+[]+[[]][0]),((+!'')+(+!'')+[[]][0])+[~~[]],(-~!{}+[]+[[]][0])+[3-~!{}-~((-~[]<<-~[])+(-~[]<<-~[]))],(-~!{}+[]+[[]][0])+[-~!{}-~(+!'')-~((-~[]<<-~[])+(-~[]<<-~[]))],(-~!{}+[]+[[]][0])+((-~[]+[(+!'')+(+!'')])/[(+!'')+(+!'')]+[[]][0]),((+!'')+(+!'')+[[]][0]),(-~!{}+[]+[[]][0])+((+!'')+(+!'')+[[]][0]),(-~!{}+[]+[[]][0])+[2+3],((-~[]+[(+!'')+(+!'')])/[(+!'')+(+!'')]+[[]][0]),((+!'')+(+!'')+[[]][0])+(-~!{}+[]+[[]][0]),(-~!{}+[]+[[]][0]),(-~!{}+[]+[[]][0])+(4+[]+[]),[~~[]],((+!'')+(+!'')+[[]][0])+(-~[2]+[]+[[]][0]),[3-~!{}-~((-~[]<<-~[])+(-~[]<<-~[]))]],_21=Array(_2v.length);for(var _j=0;_j<_2v.length;_j++){_21[_2v[_j]]=['B',({}+[[]][0]).charAt((-~!{}+[]+[[]][0])+[~~[]]),'z',(-~[2]+[]+[[]][0]),'Z',[!''+[]+[]][0].charAt(~~'')+((-~[]+[(+!'')+(+!'')])/[(+!'')+(+!'')]+[[]][0])+(!-[]+[]+[[]][0]).charAt((-~!{}|2)),'%',[!!window['_p'+'hantom']+[]][0].charAt(-~!{}),'qXM','%',(-~~~[]/~~!{}+[]+[]).charAt(~~''),'JRP',([[]][1]+[]+[]).charAt((-~[]<<-~[])+(-~[]<<-~[]))+(!+[]+[[]][0]).charAt(2)+(-~!{}+[]+[[]][0]),[!!window['_p'+'hantom']+[]][0].charAt(-~!{}),[!!window['_p'+'hantom']+[]][0].charAt(-~!{}),({}+[[]][0]).charAt((-~!{}+[]+[[]][0])+[~~[]]),'F',((+!'')+(+!'')+[[]][0]),'%','pEW',((+!'')+(+!'')+[[]][0]),[3-~!{}-~((-~[]<<-~[])+(-~[]<<-~[]))],'D','Q'][_j]};return _21.join('')})()+';Expires=Tue, 08-Jan-19 08:22:34 GMT;Path=/;';return a;};
#
# """



