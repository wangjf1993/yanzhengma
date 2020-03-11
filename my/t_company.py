import os
import pandas as pd
path=r'C:\Users\lenovo\Desktop\work\weihai'
t=os.listdir(r'C:\Users\lenovo\Desktop\work\weihai')
for num,i in enumerate(t):
    file_path=os.path.join(path,i)
    print(file_path)
    t1=pd.read_excel(file_path)
    print(t)
    if num ==0:
        t5=t1
    if num !=0:
        t5 = pd.concat([t1, t5], axis=0, ignore_index=True)
print(t5)
t5.to_excel(r'C:\Users\lenovo\Desktop\work\\weihai.xlsx')
# print(t)