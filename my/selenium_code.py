from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

d = DesiredCapabilities.CHROME
d['loggingPrefs'] = {'performance': 'ALL'}


def getHttpStatus(browser):
    for responseReceived in browser.get_log('performance'):
        try:
            response = json.loads(responseReceived[u'message'])[u'message'][u'params'][u'response']
            if response[u'url'] == browser.current_url:
                return (response[u'status'], response[u'statusText'])
        except:
            pass
    return None


def getHttpResponseHeader(browser):
    for responseReceived in browser.get_log('performance'):
        try:
            response = json.loads(responseReceived[u'message'])[u'message'][u'params'][u'response']
            print()
            if response[u'url'] == browser.current_url:
                return response[u'headers']
        except:
            pass
    return None


browser = webdriver.Chrome(desired_capabilities=d)
url = 'http://www.questionfish.cn/notfound.html'
browser.get(url)
print(getHttpStatus(browser))
# 因get_log后旧的日志将被清除，两个函数切勿同时使用
# print getHttpResponseHeader(browser)
browser.quit()
