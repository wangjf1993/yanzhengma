import datetime
import json
import multiprocessing
import random
import re
import time
import urllib
from time import sleep
from urllib.parse import quote, urlparse

import execjs
import pymongo
import requests
from lxml import etree
from redis import Redis

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import json
from collections import OrderedDict




MONGODB_HOST = '192.168.5.247'
# # MONGODB_HOST = '192.168.5.219'
MONGODB_PORT = 27017
# 外部配置
# MONGODB_HOST = '222.212.90.13'
# # MONGODB_HOST = '192.168.5.219'
# MONGODB_PORT = 28017
# MONGODB_PORT = 20000
MONGODB_DBNAME = 'Flight'
# MONGODB_DBNAME = 'data_center'
# MONGODB_DOCNAME = 'company_info'b
MONGODB_DOCNAME = 'weihai_12wwe'
MONGODB_USER = 'gouuse'
MONGODB_PASSSWORD = 'Gouuse@spider'
client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
tdb = client[MONGODB_DBNAME]
tdb.authenticate(MONGODB_USER, MONGODB_PASSSWORD)
port = tdb[MONGODB_DOCNAME]  # 表名


def write_url_to_redis(coll, num, redis_cli, r_key, n_key):
    """
          单独进程执行从mongodb 获取数据并存入redis
          :param coll: mongdb集合名
          :param num: 每次存储数量
          :param redis_cli: redis连接
          :param r_key:公司名键
          :param n_key: 累计存入数量
          :return:
          """
    while True:
        while True:
            if redis_cli.llen(r_key) <= 300:
                print('website in redis is less than 300, start to append!')
                break
            sleep(20)
        start_num = eval(redis_cli.lindex(n_key, 0).decode())[0] if redis_cli.exists(n_key) else 0
        if coll.find().count() < start_num:
            break
        print(f'start: {start_num}, get {num}')
        data_list = list(coll.find().skip(start_num).limit(num))
        for data in data_list:
            try:

                redis_cli.rpush(r_key, str([data['company_name'], str(data['_id'])]))
            except Exception as e:
                print(e)
        print(f'append {num} company_name to redis!')
        try:
            redis_cli.lpush(n_key, str([start_num + num, start_num, num]))
        except Exception as e:
            print(e)


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
            proxies_values = redis_1.lpop('proxy29').decode()
            break
        except Exception as e:
            print(e)
            pass
    return proxies_values


def get_redis_company(redis_key):
    """
    取出公司名字
    :return: 公司名
    """
    REDIS_HOST = '192.168.5.242'
    REDIS_PORT = 6379

    REDIS_DB = 14

    REDIS_PASSWORD = 'Gouuse@spider'
    redis_ = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB,
                   password=REDIS_PASSWORD)
    comapny_name = redis_.spop(f'{redis_key}').decode()
    return comapny_name


def remove_spalce(value):
    if value == '':
        return ""
    else:
        value = re.sub('\n|\r|\xa0', ' ', value).strip()
        value = value.replace('<br>', ';')
        return value


def write_url_to_redis(coll, num, redis_cli, r_key, n_key):
    """
          单独进程执行从mongodb 获取数据并存入redis
          :param coll: mongdb集合名
          :param num: 每次存储数量
          :param redis_cli: redis连接
          :param r_key:公司名键
          :param n_key: 累计存入数量
          :return:
          """
    while True:
        while True:
            if redis_cli.llen(r_key) <= 300:
                print('website in redis is less than 300, start to append!')
                break
            sleep(20)
        start_num = eval(redis_cli.lindex(n_key, 0).decode())[0] if redis_cli.exists(n_key) else 0
        if coll.find().count() < start_num:
            break
        print(f'start: {start_num}, get {num}')
        data_list = list(coll.find().skip(start_num).limit(num))
        for data in data_list:
            try:

                redis_cli.rpush(r_key, str([data['company_name'], str(data['_id'])]))
            except Exception as e:
                print(e)
        print(f'append {num} company_name to redis!')
        try:
            redis_cli.lpush(n_key, str([start_num + num, start_num, num]))
        except Exception as e:
            print(e)


def my_header(header_str):
    """
    传入头部字符串
    :param header_str:
    :return:
    """
    headers = header_str.split('\n')
    item = {}
    for i in headers:
        t = re.findall('(.*)?[:](.*)', i)
        item[t[0][0].strip()] = t[0][1].strip()
    return item


def zzzj_spider(domain, proxies):
    my_headers = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'
]
    headers = {'Host': 'whois.chinaz.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(my_headers),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'}
    headers = headers
    base_url = 'http://whois.chinaz.com/'
    url = base_url + domain
    while True:
        try:
            rep = requests.get(url, headers=headers, allow_redirects=False, proxies=proxies, timeout=20)
            html = etree.HTML(rep.content.decode())
            break
        except Exception as e:
            value = get_random_proxy()
            proxies = {
                'http': 'http://' + value,
                'https': 'https`://' + value
            }
            print(e)

    item = {}
    registrar = html.xpath('//div[contains(text(),"注册商")]/..//span/text()')
    mailbox = html.xpath('//div[contains(text(),"联系邮箱")]/..//span/text()')
    creat_time = html.xpath('//div[contains(text(),"创建时间")]/..//span/text()')
    expiration_time = html.xpath('//div[contains(text(),"过期时间")]/..//span/text()')
    contacts = html.xpath('//div[contains(text(),"联系人")]/..//span/text()')
    if registrar:
        item['registrar'] = registrar[0]
    else:
        item['registrar'] = '无法获取'
    if mailbox:
        item['mailbox'] = mailbox[0]
    else:
        item['mailbox'] = '无法获取'
    if creat_time:
        item['creat_time'] = creat_time[0]
    else:
        item['creat_time'] = '无法获取'
    if expiration_time:
        item['expiration_time'] = expiration_time[0]
    else:
        item['expiration_time'] = '无法获取'
    if contacts:
        item['contacts'] = contacts[0]
    else:
        item['contacts'] = '无法获取'
    print(item)
    return item, proxies


def getResponseHeaders(browser):
    har = json.loads(browser.get_log('har')[0]['message'])
    return OrderedDict(
        sorted([(header["name"], header["value"]) for header in har['log']['entries'][0]['response']["headers"]],
               key=lambda x: x[0]))


def getResponseStatus(browser):
    har = json.loads(browser.get_log('har')[0]['message'])
    return (har['log']['entries'][0]['response']["status"], \
            str(har['log']['entries'][0]['response']["statusText"]))


def if_mobile(domain, driver, dcap):
    item = {}
    for i in range(3):
        try:
            full_url = f'http://www.{domain}'
            res_mft = None
            # res_mft = requests.get(full_url, headers=headers, timeout=20)
            s = time.time()
            driver.get(full_url)
            print("status: ", getResponseStatus(driver))
            # sleep(random.random())
            website = full_url

            # print(len(driver.page_source))
            # print(driver.page_source)

            js = """return document.body.offsetWidth """
            width = driver.execute_script(js)
            # print(width)
            js_1 = """return  document.body.scrollWidth """
            width_1 = driver.execute_script(js_1)
            e = time.time()
            print(e - s)
            # print(width_1)
            html_code = getResponseStatus(driver)
            if html_code != (200, 'OK'):
                print(f'{website}适配移动端！')
                item['if_mobile'] = '页面请求失败'
            elif width == width_1:
                print(f'{website}适配移动端！')
                item['if_mobile'] = 'Y'
            elif (domain in driver.current_url) and (
                    'www.' + domain != urlparse(
                driver.current_url).netloc) and '检查代理服务器、防火墙和 DNS 配置' not in driver.page_source:
                print(f'{website}适配移动端！')
                item['if_mobile'] = 'Y'

            else:
                print('不适配移动端！')
                item['if_mobile'] = 'N'
            print(item)
            break
        except Exception as e:
            driver.quit()
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            driver.set_page_load_timeout(20)
            print(e)
        if i == 2:
            item['if_mobile'] = '页面请求失败'
            break
    return item


def get_cookie(proxies):
    """
    返回cookie
    :param response: 代理ip
    :return: cookie值
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'www.miitbeian.gov.cn',
        'Referer': 'http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_showPage.action',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }

    url = 'http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_showPage.action'
    response = requests.get(url, headers=headers, allow_redirects=False, proxies=proxies, timeout=20)
    __jsluid = response.headers["Set-Cookie"].split(';')[0]
    # 一级解密
    resp_body = response.content.decode('utf-8')
    get_js = re.findall(r'<script>(.*?)</script>', resp_body)[0]
    get_js_1 = get_js.replace('while(z++)try{eval', 'while(z++)try{return')
    resHtml = "function getClearance(){" + get_js_1 + "};"
    ctx = execjs.compile(resHtml)
    temp1 = ctx.call('getClearance')
    # 提取二级js函数
    function_text = temp1.split('cookie')[1].split("Path=/;'")[0] + "Path=/;'"
    t1 = function_text.split("|'+(")[0] + '|'
    tt = function_text.split("|'+(")[1].split(')()+')
    # 找出js执行函数并替换里面的值
    js_function = re.sub(r'document.create.*?firstChild.href', '"{}"'.format(response.url), tt[0])
    js_function = re.sub("function", 'function getClearance', js_function, count=1)
    ctx = execjs.compile(js_function)
    # 二级解密结果
    temp1 = ctx.call('getClearance')
    # 提取cookie值
    jsl_clearance = t1 + temp1
    jsl_clearance = jsl_clearance.replace("='", '')
    jsl_clearance = jsl_clearance.replace("'+(", '')
    print(jsl_clearance)
    return __jsluid + ';' + jsl_clearance


def beian_spider(company_name, proxies,cookies):
    company_item = {}
    while True:
        session = requests.Session()
        try:
            headers0 = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'www.miitbeian.gov.cn',
                'Referer': 'http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_showPage.action',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
                'Cookie': cookies
            }
            url = 'http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_showPage.action'
            res = session.get(url, headers=headers0, allow_redirects=False, proxies=proxies, timeout=20)
            print(res.status_code)
            res_cookies = requests.utils.dict_from_cookiejar(session.cookies)
            session.cookies.update(res_cookies)
            while True:
                headers1 = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Host': 'www.miitbeian.gov.cn',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
                    'Cookie': cookies + '; JSESSIONID={}'.format(res_cookies['JSESSIONID']),
                }

                vc = session.get('http://www.miitbeian.gov.cn/getVerifyCode?33', headers=headers1, proxies=proxies,
                                 timeout=20)
                res_cookies = requests.utils.dict_from_cookiejar(session.cookies)
                session.cookies.update(res_cookies)
                with open('vc.jpg', 'wb') as f:
                    f.write(vc.content)

                headers2 = {
                    'Accept': 'application/json, text/javascript, */*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    'Content-Length': '20',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'www.miitbeian.gov.cn',
                    'Origin': 'http://www.miitbeian.gov.cn',
                    'Referer': 'http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_showPage.action',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Cookie': cookies + '; JSESSIONID={}'.format(res_cookies['JSESSIONID']),
                }

                url_img = 'http://128.1.132.58:5001/b'
                file = {'image_file': ('vc.jpg', open('vc.jpg', 'rb'), 'image/jpeg')}
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
                }
                rep = requests.post(url_img, files=file, headers=headers)
                value = json.loads(rep.text)['value']
                # v_data = input('--------------------：')
                v_data = value
                data = {
                    'validateValue': v_data
                }
                vr = session.post('http://www.miitbeian.gov.cn/common/validate/validCode.action', data=data,
                                  headers=headers2,
                                  proxies=proxies, timeout=20)
                res_cookies = requests.utils.dict_from_cookiejar(session.cookies)
                session.cookies.update(res_cookies)
                v_code = vr.content.decode('utf-8')
                v_code = json.loads(v_code)
                if v_code["result"]:
                    break
                else:
                    print('验证码错误')
            para = {
                'siteName': '',
                'siteDomain': '',
                'siteUrl': '',
                'mainLicense': '',
                'siteIp': '',
                'condition': '5',
                'unitName': company_name,
                'mainUnitNature': '-1',
                'certType': '-1',
                'mainUnitCertNo': '',
                'verifyCode': v_data
            }
            num = urllib.parse.urlencode(para, encoding='gbk')
            headers3 = {

                'Host': 'www.miitbeian.gov.cn',
                'Connection': 'keep-alive',
                'Content-Length': f'{len(num)}',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://www.miitbeian.gov.cn',
                'Upgrade-Insecure-Requests': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_showPage.action',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
                'Cookie': cookies + '; JSESSIONID={}'.format(res_cookies['JSESSIONID']),
            }
            resx = session.post('http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_searchExecute.action',
                                data=num,
                                headers=headers3, timeout=30, proxies=proxies)
            html = etree.HTML(resx.content.decode('gbk'))
            company_name_ = ''
            website = ''
            icp_keep_on_record = ''
            to_examine_time = ''
            num_website = html.xpath('//td[contains(text(),"序号")]/../..//tr')
            company_website = []
            for i in range(1, len(num_website) - 1):
                item = {}
                if num_website[i].xpath('td[6]/div/a/@href'):
                    website = remove_spalce(num_website[i].xpath('td[6]/div/a/@href')[0])
                if num_website[i].xpath('td[2]/text()'):
                    company_name_ = remove_spalce(num_website[i].xpath('td[2]/text()')[0])
                if num_website[i].xpath('td[4]/text()'):
                    icp_keep_on_record = remove_spalce(num_website[i].xpath('td[4]/text()')[0])
                if num_website[i].xpath('td[7]/text()'):
                    to_examine_time = remove_spalce(num_website[i].xpath('td[7]/text()')[0])
                item['company_name'] = company_name_
                item['website'] = website
                item['icp_keep_on_record'] = icp_keep_on_record
                item['to_examine_time'] = to_examine_time
                if item:
                    company_website.append(item)
            # company_item['company'] = company_name
            # company_item['icp_k_o_r'] = company_website
            # print(company_name_1)
            if not num_website:
                continue
            if not company_website:
                print('此公司没有网站备案---------%s' % company_item)
                break
            else:
                print('此公司网站备案--------%s' % company_item)
                break

        except Exception as e:
            print(e)
            while True:

                try:
                    value = get_random_proxy()
                    print(value)

                    proxies = {
                        'http': 'http://' + value,
                        'https': 'https`://' + value
                    }

                    # cookies=get_cookie(proxies)
                    while True:
                        for i in range(3):
                            try:
                                cookies = get_cookie(proxies)
                                break
                            except Exception as e:
                                if i == 1:
                                    value = get_random_proxy()
                                    print(value)
                                    proxies = {
                                        'http': 'http://' + value,
                                        'https': 'https`://' + value
                                    }
                                    print(e)
                        if i==0:
                            break
                    print('换cookie值')
                    break
                except Exception as e:
                    print(e)


    return company_website, proxies,cookies


def spider(name=None):
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap[
    #     "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
    # dcap["phantomjs.page.settings.loadImages"] = False
    # driver = webdriver.PhantomJS(desired_capabilities=dcap)
    # driver.set_page_load_timeout(20)
    n = 0
    value = get_random_proxy()
    print(value)
    proxies = {
        'http': 'http://' + value,
        'https': 'https`://' + value
    }
    while True:
        for i in range(3):
            try:
                cookies = get_cookie(proxies)
                break
            except Exception as e:
                if i==1:
                    value = get_random_proxy()
                    print(value)
                    proxies = {
                        'http': 'http://' + value,
                        'https': 'https`://' + value
                    }
                    print(e)
        if i==0:
            break

    s = time.time()
    while True:

        n += 1
        print(n)
        sleep(1)
        # company_name = '山东冠县众安交通工程有限公司'
        redis_key='chongqing_if_mobile'
        company_name = get_redis_company(redis_key)
        company_name=company_name.split('|')[1]
        print(company_name)

        beian_item = beian_spider(company_name, proxies, cookies)
        website_beian, proxies, cookies = beian_item
        print(website_beian, proxies)
        if website_beian[0]['website']:

            for wesite in website_beian:
                url = urlparse(wesite['website'])
                domain = re.sub('www.', '', url.netloc)
                zzzj, proxies = zzzj_spider(domain, proxies)
                print(zzzj, proxies)
                # mobile = if_mobile(domain, driver, dcap)
                item = {**wesite, **zzzj}
                item["if_mobile"] = ''
                print(item)
                port.insert_one(item)

        else:
            print('’改公司无网站')
        print(company_name)
        v = time.time()
        print(datetime.datetime.now())
        print(v - s)
        print(name)


# 进程
class SougouProcess(multiprocessing.Process):
    def __init__(self, i):
        multiprocessing.Process.__init__(self)

        self.name = str(i)

    def run(self):
        my_str = '进程是_---:%s' % self.name
        # 需要执行的函数
        spider(my_str)







def main():
    for i in range(1):
        SougouProcess(i).start()
    pass




if __name__ == '__main__':
    spider(1)
