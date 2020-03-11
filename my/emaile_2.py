import os
import re
import subprocess

# import dns.resolver
# A = dns.resolver.query('avconstrucciones.cl','mx')
# print(A)
# for i in A:
#        print(i)

s="""li.j.qiang@gouuse.cn;

lijunqiang@gouuse.cn;

qiangli@gouuse.cn;

li.q@gouuse.cn;

lj.qiang@gouuse.cn;

qiangl@gouuse.cn;

l.j.qiang@gouuse.cn;

l_jqiang@gouuse.cn;

l.junqiang@gouuse.cn;

lqiang@gouuse.cn;

l.q@gouuse.cn;

l_qiang@gouuse.cn;

l_q@gouuse.cn;

q.l@gouuse.cn;

li_q@gouuse.cn;

l.jqiang@gouuse.cn;

li_qiang@gouuse.cn;

li@gouuse.cn;

lq@gouuse.cn;

liq@gouuse.cn;

qiang@gouuse.cn;

ljqiang@gouuse.cn;

liqiang@gouuse.cn;

qiang_li@gouuse.cn;

q.li@gouuse.cn;

ql@gouuse.cn;

li-qiang@gouuse.cn;

qiang-li@gouuse.cn;

li-q@gouuse.cn;

l-qiang@gouuse.cn;

l-q@gouuse.cn;

l.qiang@gouuse.cn;

li.qiang@gouuse.cn;

qiang.li@gouuse.cn;

li-jun-qiang@gouuse.cn;

lj_qiang@gouuse.cn;

li_j_qiang@gouuse.cn;

li_jun_qiang@gouuse.cn;

li-j-qiang@gouuse.cn;

l_junqiang@gouuse.cn;

ljunqiang@gouuse.cn;

lijqiang@gouuse.cn;

li.jun.qiang@gouuse.cn;

lj-qiang@gouuse.cn;

tureisnotture@gouuse.cn """


t=s.split(';')
print(t)
my_lsit=[i.replace('\n\n','') for i in t]
print(my_lsit)
