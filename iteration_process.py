import option_visual
import pc_form
import calculate

import json
import copy
import random
import os

with open('info.json',mode='r',encoding='UTF-8') as f:
    info=json.load(f)

with open('pc.json',mode='r',encoding='UTF-8') as f:
    pc_list=json.load(f)

try:
    with open('win_rate.json',mode='r',encoding='UTF-8') as f:
        win_rate_table=json.load(f)
except:
    win_rate_table={}

def pc_list_save():
    '''
    保存pc_list
    '''
    with open('pc.json',mode='w+',encoding='UTF-8') as f:
        json.dump(pc_list,f,separators=(',',':'),indent=4)

def win_rate_table_save():
    '''
    保存win_rate_table
    '''
    with open('win_rate.json',mode='w+',encoding='UTF-8') as f:
        json.dump(win_rate_table,f,separators=(',',':'),indent=4)

def set_weight():
    '''
    设定pc在迭代中选择的权重
    '''
    #暂定权重=pc数量*2=200
    for pc in pc_list:
        pc['Parameter']['Weight']=option_visual.sum_size*2
    
    pc_list_save()

def generate_win_rate_table():
    '''
    生成胜率表，并保存至win_rate.json
    '''
    for i in range(option_visual.sum_size-1):
        name_atk=pc_list[i]['Data']['Name']
        for j in range(i+1,option_visual.sum_size):
            name_def=pc_list[j]['Data']['Name']

            calculate.vb(name_atk,name_def)
            rates=calculate.vb_result()
            key=f"({name_atk},{name_def})"
            win_rate_table[key]=rates
            print('已完成'+key)
    
    win_rate_table_save()

def record_turn0():
    '''
    将pc_list和win_rate复制一份保存到/data中
    '''
    file=info['File']
    with open(file+'\\pc_turn0.json',mode='w+',encoding='UTF-8') as f:
        with open('pc.json',mode='r',encoding='UTF-8') as f2:
            f.write(f2.read())
    
    with open(file+'\\win_rate_turn0.json',mode='w+',encoding='UTF-8') as f:
        with open('win_rate.json',mode='r',encoding='UTF-8') as f2:
            f.write(f2.read())

def get_win_rate(pc_atk:tuple,pc_def:tuple):
    '''
    获取pc_atk和pc_def的胜率
    '''
    if(pc_atk<pc_def):


def iterate_simple():
    '''
    低精度迭代：根据权重随机选取一个号位，检查其胜率，若不超过所在组平均胜率的一半则更新其data
    '''
    #index_list=list(range(option_visual.sum_size))
    weight_list=[]
    for pc in pc_list:
        weight_list.append(pc['Parameter']['Weight'])

    while True:
        pc_chosen=random.choices(pc_list,weights=weight_list)[0]
        break

    return pc_chosen

print(iterate_simple())