#!/usr/bin/env python
#encoding: utf-8
import re


s="""www.zajtgc.com	
www.wanjie999.com	Y
www.teanhepak.com	Y
www.sxlhxny.com	N
www.stjskj.cn	Y
www.sqgda.com	N
www.shuangyingsd.com	N
www.sdzhisun.com	无法访问
www.sdwljtss.com	N
www.sdthfs.com	Y
www.sdsyhb.cn	Y
www.sdslbb.cn	Y
www.sd-sanrong.com；www.ssepec.net.cn	y
www.sdmyjs.com	Y
www.sdlonsin.com	N
www.sdlcct.com/	N
www.sdkxdd.com	N
www.sdjjzz.com	N
www.sdhsgl123.com	Y
www.sdhljt.cn	Y
www.sdhczcgs.cn	Y
www.sdgxyhjt.com	N
www.sdgxmt.com	N
www.sdgsjxkj.com	Y
www.sddqchb.com	Y
www.sdboanjt.com	Y
www.oydsd.com	Y
www.nuode123.com	Y
www.lqhongfa.com	Y
www.lcxyhbsb.com	N
www.lcsylhbkj.cn	N
www.lcsjzhbsb.com	Y
www.lchyhb.com	N
www.lchtscl.com	
www.lchhwy.cn	Y
www.huahangguanye.com	N
www.hongfengzhineng.com	N
www.hengyuanyikang.com	
www.hengfenghb.com	
www.guoyuzl.com	N
www.dxswny.cn	Y
www.2880505.com	N
sddxsj.com	Y
kxingchina.com	
hongxiu2008.com	Y
gsb.77991.com	Y
# fire-end.cn	Y"""
#
# def my_header(header_str):
#     """
#     传入头部字符串
#     :param header_str:
#     :return:
#     """
#     headers = header_str.split('\n')
#     item = {}
#     for i in headers:
#         t = re.findall('(.*)?[\t]+(.*)', i)
#         item[t[0][0].strip()] = t[0][1].strip()
#     return item
# t=my_header(s)
# print(t)
#
# t='huahangguanye.com'
# domain = t.split('；')[0]
# print(domain)
# t='http://www.hongfengzhineng.com'
#
#
# from urllib.parse import urlparse
#
# v=urlparse(t)
# print(v. netloc)




import requests

requests.get('http://www.jinyangmaoyi.com',allow_redirects=False)