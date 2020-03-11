# -*- coding:utf-8 -*-
import cmd
import os
import re
import smtplib

import subprocess
import telnetlib


def if_emaile_sever(domain):
    '''
    判断是否有邮箱服务
    :param domain:域名
    :return: 域名
    '''
    p = subprocess.Popen(f'nslookup -q=mx {domain}', shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    mx = []
    while p.poll() is None:
        line = p.stdout.readline()
        if line:
            if 'mx' in line.decode('gbk'):
                domain_mx = line.decode('gbk').split(',')[1].split('=')[1].replace('\r\n', '').strip()
                mx.append(domain_mx)
    return mx


def if_emaile_ip(mx_name):
    '''
    判断mx 地址
    :param mx_name: mx 名
    :return: 邮箱地址
    '''
    p = subprocess.Popen(f'nslookup -q=mx mx {mx_name}', shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    address = []
    while p.poll() is None:
        line = p.stdout.readline()
        if line:
            if 'Address' in line.decode('gbk'):
                emaile_ip = re.findall(r'.*?(\d+.*)[\r]', line.decode('gbk'))[0]
                address.append(emaile_ip)
                print(address)
    return address

    pass


def email_domestic(name, domain=None):
    '''
    国内小邮箱地址验证
    :param name: 用户名
    :param domain: 域名
    :return: 是否有邮箱
    '''
    if domain:
        try:
            svr = smtplib.SMTP('smtp.%s' % domain, port=25)
            svr.set_debuglevel(1)
            svr.docmd("EHLO server")

            to_addr = name + '@' + domain
            svr.putcmd('MAIL FROM:<m19965412404_84@163.com>')
            svr.getreply()
            svr.putcmd('RCPT TO:<%s>' % to_addr)

            t = svr.getreply()
            print(t)
            if t[0] == 250:
                print('邮箱真实存在')
                print('邮箱为:  %s' % to_addr)
            else:
                print('邮箱不存在')
            svr.close()
        except Exception as e:
            print('域名不存在邮箱')


def emaile_abroad(name, domain=None, ip=None):
    '''
        国内小邮箱地址验证
        :param name: 用户名
        :param domain: 域名
        :return: 是否有邮箱
        '''
    if domain:
        try:
            svr = smtplib.SMTP('%s' % ip, port=25)
            # svr.set_debuglevel(1)
            svr.docmd("EHLO server")

            to_addr = name + '@' + domain
            svr.putcmd('MAIL FROM:<m19965412404_84@163.com>')
            svr.getreply()
            svr.putcmd('RCPT TO:<%s>' % to_addr)

            t = svr.getreply()
            print(t)
            if t[0] == 250:
                print('邮箱真实存在')
                print('邮箱为:  %s' % to_addr)
                svr.close()
                return True

            else:
                svr.close()
                print('邮箱不存在')
                return False

        except Exception as e:
            print('域名不存在邮箱')



def my_telnet():
    '''
    测试
    :return:
    '''
    # t=if_emaile_sever('gouuse.cn')
    # print(t)
    # c= if_emaile_ip('mx-n.global-mail.cn')
    tn = telnetlib.Telnet('201.148.104.130', port=25, timeout=40)
    tn.set_debuglevel(2)
    msg = "my test mail"
    command = 'HELO gouuse.cn'
    tn.write(command.encode('ascii') + b'\n')
    command = 'MAIL FROM:<m19965412404_84@gouuse.cn>'
    tn.write(command.encode('ascii') + b'\n')
    to_addr = input('请输入猜测邮箱：')
    command = 'RCPT TO:<%s>' % to_addr
    tn.write(command.encode('ascii') + b'\n')
    t = tn.read_very_eager()
    print(t.decode('gbk'))
    # tn.write(b"exit\n")


def my_test():
    '''
    测试是否有邮箱
    :return:
    '''
    my_domain = input('请输入域名：')
    domain_mx = if_emaile_sever(my_domain)
    print(domain_mx)
    if domain_mx:
        for domain in my_domain:
            t = if_emaile_ip(domain)
            name = input('请输入猜测：')
            z=emaile_abroad(name=name, domain=my_domain, ip=t[0])
            if z:
                break
    else:
        print('域名无邮箱服务')


def get_abraod(domain):
    '''
    获取国外域名邮箱ip
    :return:
    '''
    mydomain=if_emaile_sever(domain)
    if mydomain:
        t=if_emaile_ip(mydomain[0])
        print(t)
    pass



def main():
    name = input('请输入猜测名：')
    domain = input('请输入域名：')
    email_ip = input('请输入ip:')
    emaile_abroad(name=name, domain=domain, ip=email_ip)
    pass


if __name__ == '__main__':
    # while True:
    #     my_test()
        # main()
        # domain = input('请输入域名：')
        # get_abraod(domain)
    my_list=[1]
    my_list.append(2)
    print(my_list)
