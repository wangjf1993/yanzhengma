import datetime
import random
import re
import time
import traceback
from time import sleep

import pymongo
import redis
import requests
import urllib3
# 忽视免验证并不显示
from redis import Redis
from urllib3.exceptions import InsecureRequestWarning

from selenium import webdriver
from urllib.parse import urlparse

# options = webdriver.ChromeOptions()
# options.add_argument('lang=zh_CN.UTF-8')
# prefs = {"profile.managed_default_content_settings.images":2}
# options.add_experimental_option("prefs",prefs)
# options.add_argument('user-agent="Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"')
# 'User-Agent: Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
# driver=webdriver.Chrome(options=options)


# driver.set_window_size(360,640)
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import json
from collections import OrderedDict


def my_mongo(mong_table_name):
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
    MONGODB_DOCNAME = f'{mong_table_name}'
    MONGODB_USER = 'gouuse'
    MONGODB_PASSSWORD = 'Gouuse@spider'
    client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
    tdb = client[MONGODB_DBNAME]
    tdb.authenticate(MONGODB_USER, MONGODB_PASSSWORD)
    port = tdb[MONGODB_DOCNAME]  # 表名
    return port


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
    while True:
        try:
            main_win = driver.current_window_handle  # 记录当前窗口的句柄
            all_win = driver.window_handles
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
                        print(width_1)
                        print(width)
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
                    print(e)
                    driver.quit()
                    driver = webdriver.PhantomJS(desired_capabilities=dcap)
                    driver.set_page_load_timeout(20)
                    driver.set_script_timeout(10)
                    if 'time' in str(traceback.format_exc()):
                        print('页面访问超时')
                    print(e)
                if i == 2:
                    item['if_mobile'] = '页面请求失败'
                    break
            break
        except Exception as e:
            print(e)
            driver.quit()
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            driver.set_page_load_timeout(20)
            driver.set_script_timeout(10)
            item = {}
            item['if_mobile'] = '页面请求失败'
            break

    return item


dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap[
    "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
dcap["phantomjs.page.settings.loadImages"] = False
driver = webdriver.PhantomJS(desired_capabilities=dcap)
driver.set_page_load_timeout(20)
driver.set_script_timeout(10)

if __name__ == '__main__':
    n = 1
    while True:
        n += 1
        company_info = get_redis_company('chongqing_if_mobile')
        print(company_info)
        url = company_info.split('|')[0]
        domain = urlparse(url).netloc.replace('www.', '')
        print(domain)
        t = if_mobile(domain, driver, dcap)
        mongo_port = my_mongo('chongqing_frv_if_mobile')
        mongo_port.insert_one(t)
        print(t)
        print(datetime.datetime.now())
        print(company_info)
        print(n)
        if n == 40:
            driver.quit()
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            driver.set_page_load_timeout(20)
            driver.set_script_timeout(10)
            n = 1
