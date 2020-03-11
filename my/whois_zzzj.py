import re

import requests
from redis import Redis
from lxml import etree


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
            proxies_values = redis_1.lpop('proxy1').decode()
            break
        except:
            pass
    return proxies_values


def zzzj_spider(domain):
    s = """Host: whois.chinaz.com
    Connection: keep-alive
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
    Accept-Encoding: gzip, deflate
    Accept-Language: zh-CN,zh;q=0.9"""
    value = get_random_proxy()
    proxies = {
        'http': 'http://' + value,
        'https': 'https`://' + value
    }

    headers = my_header(s)
    base_url = 'http://whois.chinaz.com/'
    url = base_url + domain
    rep = requests.get(url, headers=headers, allow_redirects=False, proxies=proxies,timeout=20)
    html=etree.HTML(rep.content.decode())
    item = {}
    registrar = html.xpath('//div[contains(text(),"注册商")]/..//span/text()')
    mailbox = html.xpath('//div[contains(text(),"联系邮箱")]/..//span/text()')
    creat_time = html.xpath('//div[contains(text(),"创建时间")]/..//span/text()')
    expiration_time = html.xpath('//div[contains(text(),"过期时间")]/..//span/text()')
    contacts = html.xpath('//div[contains(text(),"联系人")]/..//span/text()')
    if registrar:
        item['registrar'] = registrar[0]
    else:
        item['registrar'] = ''
    if mailbox:
        item['mailbox'] = mailbox[0]
    else:
        item['mailbox'] = ''
    if creat_time:
        item['creat_time'] = creat_time[0]
    else:
        item['creat_time'] = ''
    if expiration_time:
        item['expiration_time'] = expiration_time[0]
    else:
        item['expiration_time'] = ''
    if contacts:
        item['contacts'] = contacts[0]
    else:
        item['contacts'] = ''
    print(item)
    return item




def main():
    zzzj_spider('300.cn')


if __name__ == '__main__':
    main()
