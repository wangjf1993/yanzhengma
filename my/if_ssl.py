import datetime
import json
import re
import signal
import time
import traceback

import threading

from collections import OrderedDict
from urllib.parse import urlparse

import pymongo
import requests
from redis import Redis
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from w3lib.html import remove_tags


import unittest

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}


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
    try:
        har = browser.get_log('status')
        return har

    except :
        har = json.loads(browser.get_log('har')[0]['message'])
        return (har['log']['entries'][0]['response']["status"], str(har['log']['entries'][0]['response']["statusText"]))


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


def decode_response(response):
    """
    解码
    :param response:
    :return:
    """
    decoded_response = ''
    for num,charset in enumerate(['utf-8', 'ascii', 'gbk', 'gb2312', 'ISO8859-1']):
        try:
            decoded_response = response.decode(charset)
            break
        except Exception as e:
            if num == 4:
                decoded_response = response.decode('utf-8','ignore')
            pass
    return decoded_response

def find_competitor_1(x):
    if x == '':
        return '页面无法访问'
    x = decode_response(x)
    if x == '':
        return "无法获取"
    if re.findall(r'中企动力', x):
        return '中企动力'
#     reg = re.compile(r'技术支持：(w+)|设计维护:(w+)|网站制作：(w+)|策划设计：(w+)')
    x=remove_tags(x)
    reg = re.compile(r'设计维护[:|：]\s?(\w+)')
    if re.findall(reg, x):
        result = re.findall(reg, x)[0]
        return result
    reg = re.compile(r'网站制作[:|：]\s?(\w+)')
    if re.findall(reg, x):
        result = re.findall(reg, x)[0]
        return result
    reg = re.compile(r'本站由(\w+)提供网站建设')
    if re.findall(reg, x):
        result = re.findall(reg, x)[0]
        return result
    reg = re.compile(r'策划设计[:|：]\s?(\w+)')
    if re.findall(reg, x):
        result = re.findall(reg, x)[0]
        return result
    reg = re.compile(r'技术支持[:|：|【]\s?(\w+)')
    if re.findall(reg, x):
        result = re.findall(reg, x)[0]
        return result
    x= re.sub(r'\t','',x)
    result=re.findall(r'本站使用(\w+)搭建', x)[0]if re.findall(r'本站使用(\w+)搭建', x) else "无法获取"
    return result


def if_mobile(domain, driver, dcap):
    print('mobilestart')
    while True:
        item = {}

        full_url = f'http://www.{domain}'
        # res_mft = None
        # res_mft = requests.get(full_url, headers=headers, timeout=20)
        # s = time.time()

        try:
            print('')
            start_time=time.time()
            driver.implicitly_wait(16)
            # my_thead=MyTheading(driver)
            # my_thead.start()

            driver.get(full_url)

            locator = (By.XPATH, '/html/head')
            # 隐性等待
            WebDriverWait(driver, 3, 1).until(EC.presence_of_element_located(locator))
            try:
                # 获取alert对话框的按钮，点击按钮，弹出alert对话框
                # driver.find_element_by_id('alert').click()
                time.sleep(1)
                # 获取alert对话框
                dig_alert = driver.switch_to.alert
                time.sleep(1)
                # 打印警告对话框内容
                print(dig_alert.text)
                # alert对话框属于警告对话框，我们这里只能接受弹窗
                dig_alert.accept()
            except Exception as e:

                pass
                # print(e)

            try:
                # driver.find_element_by_id('confirm').click()
                # time.sleep(1)
                # 获取confirm对话框
                dig_confirm = driver.switch_to.alert
                time.sleep(1)
                # 打印对话框的内容
                print(dig_confirm.text)
                # 点击“确认”按钮
                dig_confirm.accept()
            except Exception as e:
                pass
                # print(e)
            try:
                # driver.find_element_by_id('prompt').click()
                # time.sleep(1)
                # 获取prompt对话框
                dig_prompt = driver.switch_to.alert
                time.sleep(1)
                # 打印对话框内容
                print(dig_prompt.text)
                # 在弹框内输入信息
                dig_prompt.send_keys("Loading")
                # 点击“确认”按钮，提交输入的内容
                dig_prompt.accept()
            except Exception as e:

                pass
                # print(e)
        except Exception  as e:

            print(time.time()-start_time)

            # driver.refresh()
            # alls=driver.window_handles
            driver.execute_script('window.stop()')
            print('1111111111111111111111111111')
            # driver.switch_to_window(alls[0])



            # print(e)
                # if 'time' in str(traceback.format_exc()):
                #     print('页面访问超时')
                #     driver.quit()
                #     print('关掉浏览器')
                #     options.add_argument('lang=zh_CN.UTF-8')
                #     prefs = {"profile.managed_default_content_settings.images": 2}
                #     options.add_experimental_option("prefs", prefs)
                #     options.add_argument(
                #         'user-agent="Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"')
                #     options.add_argument('--headless')
                #     driver = webdriver.Chrome(options=options)
                #     driver.set_page_load_timeout(20)
                #     driver.set_script_timeout(20)
                #     print('重启浏览器')


        # print("status: ", getResponseStatus(driver))
        # sleep(random.random())
        # website = full_url

        # print(len(driver.page_source))
        # print(driver.page_source)
        # stats=getResponseStatus(driver)
        # print(stats)
        js = """return document.body.offsetWidth """
        width = driver.execute_script(js)

        # print(width)
        js_1 = """return  document.body.scrollWidth """
        width_1 = driver.execute_script(js_1)
        e = time.time()
        html_code = getResponseStatus(driver)
        print(html_code)
        # if html_code[0] != 200:
        #     item['if_mobile'] = '页面请求失败'
        print(driver.current_url)

        try:
            if html_code['status'] in [404]:
                item['if_mobile']='页面请求失败'
                return item
        except:
            pass
        if width == width_1:
            print(width_1)
            print(width)
            item['if_mobile'] = 'Y'

        else:
            item['if_mobile'] = 'N'
        break

    print('mobileend')
    return item


def ssl_spider(url):
    print('sssl开始')
    # url='http://www.qhtxff.com'
    item = {}
    url_1 = url.replace('http', 'https')
    try:
        rep = requests.get(url=url_1, headers=headers, verify=False, timeout=20)

        if rep.status_code == 200:
            item['if_ssl'] = 'Y'

            item['html_content'] = find_competitor_1(rep.content)
            return item

        try:
            rep = requests.get(url, headers, timeout=20, verify=False)
            if rep.status_code == 200:
                item['if_ssl'] = 'N'
                item['html_content'] = find_competitor_1(rep.content)
                return item
            else:
                item['if_ssl'] = '页面请求失败'
                item['html_content'] = '页面请求失败'
        except Exception  as e:
            item['if_ssl'] = '页面请求失败'
            item['html_content'] = '页面请求失败'
    except Exception as e:
        try:
            rep = requests.get(url, headers, timeout=20,verify=False)
            if rep.status_code == 200:
                item['if_ssl'] = 'N'
                item['html_content'] = find_competitor_1(rep.content)
            else:
                item['if_ssl'] = '页面请求失败'
                item['html_content'] = '页面请求失败'
        except Exception  as e:
            item['if_ssl'] = '页面请求失败'
            item['html_content'] = '页面请求失败'
    print('sssl结束')
    return item

    pass



class MyTheading(threading.Thread):
    def __init__(self,driver):
        threading.Thread.__init__(self)
        self.driver = driver

    def run(self):
        time.sleep(10)
        self.driver.execute_script('window.stop()')
        print('232423333333333')
        pass




dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap[
    "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
dcap["phantomjs.page.settings.loadImages"] = False
# driver = webdriver.PhantomJS(desired_capabilities=dcap)
# driver.set_page_load_timeout(20)
# driver.set_script_timeout(20)
# options = webdriver.ChromeOptions()
# options.add_argument('lang=zh_CN.UTF-8')
# prefs = {"profile.managed_default_content_settings.images":2}
# options.add_experimental_option("prefs",prefs)
# options.add_argument('user-agent="Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"')
# # options.add_argument('--headless')
# driver=webdriver.Chrome(options=options)
# driver.set_page_load_timeout(20)
# driver.set_script_timeout(20)
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')



driver=webdriver.Firefox(executable_path=r'C:\Users\lenovo\Desktop\geckodriver.exe',firefox_profile=profile)
driver.set_page_load_timeout(20)
driver.set_script_timeout(20)

def main():
    while True:
        company_info = get_redis_company('chongqing_if_mobile')
        url = company_info.split('|')[0]
        while True:
            try:
                # urls=['http://www.cqlao51.com',  'http://www.lisgo.cn', 'http://www.10010hjhp.com', 'http://www.337x.com']
                # for url in urls:
                # url='hhttp://www.lmhxyg.comhttp://www.lmhxyg'
                # url='http://www.lmhxyg.com'
                # url='http://www.同辉.网址'
                # url='http://www.cqfeedi.com'
                # url='http://www.china-cqhl.com'
                # url='http://www.300.cn'
                # url='http://www.wstty.com'
                # http://www.xinhuibio.com
                # url='http://www.sydhwsm.com'
                # url='http://www.chinahajk.com'
                # url='http://www.cn-yysw.com'
                # url='http://www.bzcljt.com'
                # url='http://www.mijdao.com'
                # url='http://www.mijdao.com'
                print(url)
                while True:
                    item = ssl_spider(url)
                    if item:
                        break
                domain = url.replace('http://www.', '')
                mobile = {}
                if item['if_ssl'] != '页面请求失败':
                    mobile = if_mobile(domain, driver, dcap)
                else:
                    mobile['if_mobile'] = '页面请求失败'
                item = {**item, **mobile}

                item['website']=url
                my_mongo('chongqingtest_ssl_mobile_html_1').insert_one(item)
                print(item)
                print(datetime.datetime.now())
                break
            except Exception as e:
                pass


if __name__ == '__main__':
    main()
