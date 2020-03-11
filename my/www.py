from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotVisibleException
import time
import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from check_ticket import Check
from verify import Code
import json

class Buy_Ticket():
    def __init__(self, start_station, end_station, date, username, password, purpose):
        self.num = 1
        self.start = start_station
        self.end = end_station
        self.date = date
        self.username = username
        self.password = password
        self.purpose = purpose
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'

    def login(self):
        browser.get(self.login_url)
        try:
            input_name = browser.find_element_by_id('username')
            input_pd = browser.find_element_by_id('password')
            button = browser.find_element_by_id('loginSub')
            time.sleep(1)
            input_name.send_keys(self.username)
            input_pd.send_keys(self.password)
            c = Code(browser)       #调用验证码识别模块
            c.main()
            button.click()
            time.sleep(2)
            #等待页面跳转，如果验证码识别错误，就执行下面的while语句
            while browser.current_url == self.login_url + '#':
                c = Code(browser)
                c.main()
                button.click()
                time.sleep(2)
            #self.get_passenger()
            self.check()
        except NoSuchElementException:
            self.login()

    def check(self):
        #调用余票查询模块
        check = Check(self.date, self.start, self.end, self.purpose)
        start_end = check.look_up_station()
        self.num = check.get_info()
        #cookie的添加，json.dumps把以汉字形式呈现的起始、终点站转化成unicode编码，可在审查元素里查看cookie
        browser.add_cookie({'name':'_jc_save_fromStation', 'value':json.dumps(self.start).strip('"').replace('\\', '%') + '%2C' + start_end[0]})
        browser.add_cookie({'name':'_jc_save_toStation', 'value':json.dumps(self.end).strip('"').replace('\\', '%') + '%2C' + start_end[1]})
        browser.add_cookie({'name':'_jc_save_fromDate', 'value':self.date})
        browser.get(self.ticket_url)
        if self.purpose == '学生':
            btn = browser.find_element_by_id('sf2')
            time.sleep(1)
            btn.click()
        button = browser.find_element_by_id('query_ticket')
        time.sleep(1)
        button.click()

    def book_ticket(self):
        print('开始预订车票...')
        #先查找出所有车次对应的预订按钮，再根据余票查询模块返回的车次序号，点击相应的预订按钮
        button = browser.find_elements_by_class_name('btn72')
        button[self.num-1].click()
        time.sleep(3)
        button2 = browser.find_element_by_id('normalPassenger_0')  #按实际情况，可自行修改，这里就选择的第一个常用联系人，
                                                                    #第二个是normalPassenger_1，依此类推
        button2.click()
        button3 = browser.find_element_by_id('submitOrder_id')
        time.sleep(1)
        button3.click()
        time.sleep(3)  #等待页面加载完毕，不然后面可能会报错,等待时间自行决定
        try:
            button4 = browser.find_element_by_id('qr_submit_id')
            button4.click()
        except ElementNotVisibleException:
            button4 = browser.find_element_by_id('qr_submit_id')
            button4.click()
        print('车票预定成功！请在30分钟内完成付款！')

    def main(self):
        self.login()
        self.book_ticket()

if __name__ == '__main__':
    begin = time.time()
    browser = webdriver.Chrome()
    b = Buy_Ticket('渠县', '广州', '2019-02-09', '452883314@qq.com', 'lijun7870305', 'ADULT')  #账号、密码自行修改
    b.main()
    end = time.time()
    print('总耗时：%d秒' % int(end-begin))
    #browser.close()
