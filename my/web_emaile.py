from flask import Flask, request, jsonify, render_template

app = Flask(__name__)




'''
在线验证邮箱真实性
'''
import os
import random
import re
import smtplib
import logging
import subprocess
import time
import traceback

import dns.resolver

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s: %(message)s')

logger = logging.getLogger()

# 需要安装 pip install PySocks
import socks

#


def if_emaile_ip(mx_name):
    '''
    判断mx 地址
    :param mx_name: mx 名
    :return: 邮箱地址
    '''
    p = subprocess.Popen(f'nslookup -q=mx mx {mx_name}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    address = []
    while p.poll() is None:
        line = p.stdout.readline()
        if line:
            if 'Address' in line.decode('gbk'):
                emaile_ip = re.findall(r'.*?(\d+.*)[\r]', line.decode('gbk'))[0]
                address.append(emaile_ip)
                print(address)
    return address
    # t = os.popen(f'nslookup -q=mx mx {mx_name}')
    # text = t.read()
    # print(text)
    # t = re.findall('.*?(\d+.*\d+).*', text)
    # print(t)
    return t
    pass


def fetch_mx(host):
    '''
    解析服务邮箱
    :param host:
    :return:
    '''
    try:
        logger.info('正在查找邮箱服务器')
        answers = dns.resolver.query(host, 'MX')
        res = [str(rdata.exchange)[:-1] for rdata in answers]
        logger.info('查找结果为：%s' % res)
        return res
    except Exception as e:
        print(e)
    return None


def verify_istrue_1(email):
    '''
    :param email:
    :return:
    '''
    email_list = []
    email_obj = {}
    final_res = {}
    if isinstance(email, str) or isinstance(email, bytes):
        email_list.append(email)
    else:
        email_list = email

    for em in email_list:
        name, host = em.split('@')
        if email_obj.get(host):
            email_obj[host].append(em)
        else:
            email_obj[host] = [em]

    for key in email_obj.keys():

        # host = random.choice(fetch_mx(key))
        num = 0
        mx_list = fetch_mx(key)
        for host in mx_list:
            num += 1
            try:
                logger.info('正在连接服务器...：%s' % host)
                while True:
                    try:
                        s = smtplib.SMTP(host, timeout=20)
                        break
                    except Exception as e:
                        host = if_emaile_ip(host)[0]
                name = ''
                name_1 = ''
                for need_verify in email_obj[key]:
                    name = need_verify
                    helo = s.docmd('HELO chacuo.net')
                    logger.debug(helo)

                    send_from = s.docmd(f'MAIL FROM:<3125147@chacuo.net>')
                    logger.debug(send_from)
                    send_from = s.docmd('RCPT TO:<%s>' % need_verify)
                    logger.debug(send_from)
                    if send_from[0] == 250 or send_from[0] == 451:
                        final_res[need_verify] = True  # 存在
                    elif send_from[0] == 550:
                        final_res[need_verify] = False  # 不存在
                    else:
                        final_res[need_verify] = None  # 未知

                    # 验证
                    my_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                               's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                    test_name = ''
                    for i in range(20):
                        test_name += random.choice(my_list)
                    test_name = test_name + '@' + key
                    name_1 = test_name
                    helo = s.docmd('HELO chacuo.net')
                    logger.debug(helo)

                    send_from = s.docmd(f'MAIL FROM:<3125147@chacuo.net>')
                    logger.debug(send_from)
                    send_from = s.docmd('RCPT TO:<%s>' % test_name)
                    logger.debug(send_from)
                    if send_from[0] == 250 or send_from[0] == 451:
                        final_res[test_name] = True  # 存在
                    elif send_from[0] == 550:
                        final_res[test_name] = False  # 不存在
                    else:
                        final_res[test_name] = None  # 未知
                    print(final_res[name])
                    print(final_res[name_1])
                    if final_res[name] == final_res[name_1]:
                        final_res[name] = None
                        final_res.pop(name_1)

                s.close()

                if final_res[name] != None:
                    break



            except Exception as e:
                print(e)

    return final_res


def choice_mx_smtp(test_emaile,mx):
    for i in mx:
        try:
            logger.info('正在连接服务器...：%s' % i)

            smtp = smtplib.SMTP(i, timeout=20)
            helo = smtp.docmd('HELO chacuo.net')
            logger.debug(helo)
            send_from = smtp.docmd('MAIL FROM:<3121113@chacuo.net>')
            logger.debug(send_from)
            send_from = smtp.docmd('RCPT TO:<%s>' % test_emaile)
            if send_from[0] != 450:
                return smtp, send_from
        except Exception as e:
            print(e)
    pass



def link_semtp(mx):
    for i in mx:
        try:
            logger.info('正在连接服务器...：%s' % i)
            s = smtplib.SMTP(i, timeout=20)
            return s,i
        except Exception as e:
            print(e)

    return None

def verify_istrue(email):
    '''
    :param email:
    :return:
    '''
    email_list = []
    email_obj = {}
    final_res = {}
    if isinstance(email, str) or isinstance(email, bytes):
        email_list.append(email)
    else:
        email_list = email

    for em in email_list:
        name, host = em.split('@')
        if email_obj.get(host):
            email_obj[host].append(em)
        else:
            email_obj[host] = [em]

    for key in email_obj.keys():
        try:
            mx = fetch_mx(key)
            len(mx)
        except Exception  as e:
            for need_verify in email_obj[key]:
                final_res[need_verify] = None
            continue
        while True:
            try:
                s,host = link_semtp(mx)
                break
            except Exception as e:
                pass
        name = ''
        name_1 = ''
        for need_verify in email_obj[key]:
            name = need_verify
            try:
                helo = s.docmd('HELO chacuo.net')
                logger.debug(helo)
                send_from = s.docmd('MAIL FROM:<3121113@chacuo.net>')
                logger.debug(send_from)
                send_from = s.docmd('RCPT TO:<%s>' % need_verify)
            except Exception as e:
                s, send_from = choice_mx_smtp(need_verify, mx)
                # err = traceback.format_exc()

            logger.debug(send_from)

            if send_from[0] == 450:
                s, send_from = choice_mx_smtp(need_verify,mx)

            if send_from[0] == 250:
                final_res[need_verify] = True  # 存在
            elif send_from[0] == 550 or send_from[0] == 451 or send_from[0] == 554:
                final_res[need_verify] = False  # 不存在
            else:
                final_res[need_verify] = None  # 未知
                # 验证
            my_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                       's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            test_name = ''
            for i in range(20):
                test_name += random.choice(my_list)
            test_name = test_name + '@' + key
            name_1 = test_name
            try:
                helo = s.docmd('HELO chacuo.net')
                logger.debug(helo)

                send_from = s.docmd(f'MAIL FROM:<3125147@chacuo.net>')
                logger.debug(send_from)
                send_from = s.docmd('RCPT TO:<%s>' % test_name)
            except Exception as e:
                s, send_from = choice_mx_smtp(test_name, mx)
                pass
            logger.debug(send_from)

            if send_from[0] == 250:
                final_res[name_1] = True  # 存在
            elif send_from[0] == 550 or send_from[0] == 451:
                final_res[name_1] = False  # 不存在
            else:
                final_res[name_1] = None  # 未知

            if final_res[name] == final_res[name_1]:
                if  not final_res[name]:
                    pass
                else:
                    final_res[name] = None
            final_res.pop(name_1)

        s.close()
    return final_res

@app.route('/b', methods=['POST','GET'])
def index():
    if request.method == 'POST' and request.files.get('image_file'):
        result={'sdsad':1}
        return jsonify(result)

    elif request.method == 'GET':
        return render_template("test.html")



if __name__ == "__main__":
    app.run(debug=True)