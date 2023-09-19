import calculate

import json
import random

with open('pc.json',mode='r',encoding='UTF-8') as f:
    pc_list=json.load(f)

#使用index_list记录未选择过的pc
index_list=[]
for i in range(len(pc_list)):
    if(pc_list[i]['Parameter']['Mark']==False):
        index_list.append(i)

def reset():
    '''
    随机选择一个Mark为False的pc，将其Data更新为apc后的结果，Mark更新为True，然后保存至pc_list
    '''
    index=random.choice(index_list)
    pc_chosen=pc_list[index]
    
    group=pc_chosen['Parameter']['Group']
    number=pc_chosen['Parameter']['Number']

    new_data=calculate.apc_all(group,number)

    pc_chosen['Data']=new_data
    pc_chosen['Parameter']['Mark']=True

    pc_list[index]=pc_chosen
    with open('pc.json',mode='w+',encoding='UTF-8') as f:
        json.dump(pc_list,f,separators=(',',':'),indent=4)
    
    index_list.remove(index)

