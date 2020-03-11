
import telnetlib




# tn = telnetlib.Telnet('201.148.104.130', port=25, timeout=40)
# tn.set_debuglevel(2)
# msg = "my test mail"
# command = 'HELO gouuse.cn'
# tn.write(command.encode('ascii') + b'\n')
# command = 'MAIL FROM:<m19965412404_84@gouuse.cn>'
# tn.write(command.encode('ascii') + b'\n')
# to_addr = input('请输入猜测邮箱：')
# command = 'RCPT TO:<%s>' % to_addr
# tn.write(command.encode('ascii') + b'\n')
# t = tn.read_very_eager()
# print(t.decode('gbk'))
l=['betty_kirklin@lapptannehill.com', 'betty.kirklin@lapptannehill.com', 'kb@lapptannehill.com', 'kirklin_betty@lapptannehill.com', 'kirklinbetty@lapptannehill.com', 'kirklinb@lapptannehill.com', 'kirklin_b@lapptannehill.com', 'kirklin.betty@lapptannehill.com', 'kbetty@lapptannehill.com', 'betty.k@lapptannehill.com', 'b.k@lapptannehill.com', 'b_kirklin@lapptannehill.com', 'bettykirklin@lapptannehill.com', 'kirklin.b@lapptannehill.com', 'b.kirklin@lapptannehill.com', 'bkirklin@lapptannehill.com', 'b_k@lapptannehill.com', 'bk@lapptannehill.com', 'k_b@lapptannehill.com', 'bettyk@lapptannehill.com', 'k_betty@lapptannehill.com', 'betty_k@lapptannehill.com', 'k.betty@lapptannehill.com', 'k.b@lapptannehill.com', 'k-betty@lapptannehill.com', 'kirklin-betty@lapptannehill.com', 'betty-k@lapptannehill.com', 'b-kirklin@lapptannehill.com', 'kirklin-b@lapptannehill.com', 'k-b@lapptannehill.com', 'betty-kirklin@lapptannehill.com', 'b-k@lapptannehill.com', 'bkirklin02@lapptannehill.com', 'betty@lapptannehill.com', 'bkirklin01@lapptannehill.com', 'kirklin@lapptannehill.com', 'bkirkl01@lapptannehill.com', 'bkirkl@lapptannehill.com', 'bkirkl02@lapptannehill.com', 'bkirklin@lapptannehill.com', 'tureisnotture@lapptannehill.com']

# set_1={}
# for k,v in l.items():
#     if v !=None:
#         set_1[k]=v
#
# print(set_1)
# print(len(set_1))
l_1={'betty_kirklin@lapptannehill.com': False, 'betty.kirklin@lapptannehill.com': False, 'kb@lapptannehill.com': False, 'kirklin_betty@lapptannehill.com': False, 'kirklinbetty@lapptannehill.com': False, 'kirklinb@lapptannehill.com': False, 'kirklin_b@lapptannehill.com': False, 'kirklin.betty@lapptannehill.com': False, 'kbetty@lapptannehill.com': False, 'betty.k@lapptannehill.com': False, 'b.k@lapptannehill.com': False, 'b_kirklin@lapptannehill.com': False, 'bettykirklin@lapptannehill.com': False, 'kirklin.b@lapptannehill.com': False, 'b.kirklin@lapptannehill.com': False, 'bkirklin@lapptannehill.com': False, 'b_k@lapptannehill.com': False, 'bk@lapptannehill.com': False, 'k_b@lapptannehill.com': False, 'bettyk@lapptannehill.com': False, 'k_betty@lapptannehill.com': False, 'betty_k@lapptannehill.com': False, 'k.betty@lapptannehill.com': False, 'k.b@lapptannehill.com': False, 'k-betty@lapptannehill.com': False, 'kirklin-betty@lapptannehill.com': False, 'betty-k@lapptannehill.com': False, 'b-kirklin@lapptannehill.com': False, 'kirklin-b@lapptannehill.com': False, 'k-b@lapptannehill.com': False, 'betty-kirklin@lapptannehill.com': False, 'b-k@lapptannehill.com': False, 'bkirklin02@lapptannehill.com': False, 'betty@lapptannehill.com': False, 'bkirklin01@lapptannehill.com': False, 'kirklin@lapptannehill.com': False, 'bkirkl01@lapptannehill.com': False, 'bkirkl@lapptannehill.com': False, 'bkirkl02@lapptannehill.com': False, 'tureisnotture@lapptannehill.com': False}

print(len(l_1))
print(len(l))

for k,v in l_1.items():
    print(k,' ',v)










