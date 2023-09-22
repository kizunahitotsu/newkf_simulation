import option_visual
import pc_form
import calculate

import json
import copy
import random
import os

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
            win_rate=calculate.vb_result()
            item=f"({name_atk},{name_def})"
            win_rate_table[item]=win_rate
            print('已完成'+item)
    
    win_rate_table_save()

def record_turn0():
    '''
    将pc_list和win_rate复制一份保存到/data中
    '''
    with open('info.json',mode='r',encoding='UTF-8') as f:
        info=json.load(f)
    
    file=info['File']
    with open(file+'\\pc_turn0.json',mode='w+',encoding='UTF-8') as f:
        with open('pc.json',mode='r',encoding='UTF-8') as f2:
            f.write(f2.read())
    
    with open(file+'\\win_rate_turn0.json',mode='w+',encoding='UTF-8') as f:
        with open('win_rate.json',mode='r',encoding='UTF-8') as f2:
            f.write(f2.read())

def get_win_rate(pc_atk:tuple,pc_def:tuple):
    '''
    获取pc_atk和pc_def的胜率（元组）
    '''
    #使用tuple传参是为了方便比较
    #win_rate可能来源于文件(list)，也可能来源于迭代时的修改(tuple)，因此统一转换类型
    if(pc_atk<pc_def):
        item=f"(({pc_atk[0]},{pc_atk[1]}),({pc_def[0]},{pc_def[1]}))"
        win_rate=win_rate_table[item]
    
    elif(pc_atk>pc_def):
        item=f"(({pc_def[0]},{pc_def[1]}),({pc_atk[0]},{pc_atk[1]}))"
        win_rate=win_rate_table[item]
        #交换胜负场数
        win=win_rate[1]
        lose=win_rate[0]
        win_rate=(win,lose,win_rate[2])

    return tuple(win_rate)

def average_win_rate(pc_tuple:tuple):
    '''
    获取(group,number)号pc的平均胜率
    '''
    win_rate_list=[]
    for pc in pc_list:
        pc_def=(pc['Parameter']['Group'],pc['Parameter']['Number'])
        if(pc_def!=pc_tuple):
            win_rate=get_win_rate(pc_tuple,pc_def)
            if(win_rate[0]==0 and win_rate[1]==0): #只有不是全平场的才放入列表
                pass
            else:
                win_rate_list.append(win_rate)
            del win_rate
    
    if(win_rate_list): #有非平场
        sum_win=0
        sum_lose=0
        sum_draw=0
        for win_rate in win_rate_list:
            sum_test=sum(win_rate)
            sum_win+=win_rate[0]/sum_test
            sum_lose+=win_rate[1]/sum_test
            sum_draw+=win_rate[2]/sum_test

        return sum_win/(sum_win+sum_lose)
    
    else: #全平场
        return 0.5

def iterate_simple():
    '''
    低精度迭代：根据权重随机选取一个号位，检查其胜率，若不超过所在组平均胜率的则更新其data，然后保存相关信息
    '''
    #根据权重随机index
    index_list=list(range(option_visual.sum_size))
    weight_list=[]
    for pc in pc_list:
        weight_list.append(pc['Parameter']['Weight'])
        #初始化pc_list的mark
        pc['Parameter']['Mark']=False
    
    #选取一个胜率不超过所在组平均胜率的pc
    while True:
        index_chosen=random.choices(index_list,weights=weight_list)[0]
        pc_chosen=pc_list[index_chosen]
        if(pc_chosen['Parameter']['Mark']): #选中mark为False的才继续判断
            continue

        group=pc_chosen['Parameter']['Group']
        number=pc_chosen['Parameter']['Number']

        #检查胜率
        size=option_visual.option['Group'][group]['Size']
        win_rate_group=[]
        for n in range(1,size+1):
            win_rate_group.append(average_win_rate((group,n)))
        
        average=sum(win_rate_group)/size
        if(win_rate_group[number-1]<=average): #选中
            break
        else:
            pc_chosen['Parameter']['Mark']=True

    #更新data
    calculate.Unlimited=True
    new_data=calculate.apc_all(group,number)
    pc_chosen['Data']=new_data

    #更新parameter
    with open('info.json',mode='r',encoding='UTF-8') as f:
        info=json.load(f)
    
    turn=info['Turn']+1
    pc_chosen['Parameter']['Turn']=turn

    if(pc_chosen['Parameter']['Weight']>=option_visual.sum_size):
        #若被选中的权重>=pc数，则将其权重减去pc数并分配给所有pc（一次不减少太多）
        pc_chosen['Parameter']['Weight']-=option_visual.sum_size

        for pc in pc_list:
            pc['Parameter']['Weight']+=1
    
    else:
        #否则将该权重归零，并随机分配给所有pc
        to_distribute=random.choices(index_list,k=chosen['Parameter']['Weight'])
        pc_chosen['Parameter']['Weight']=0
        for i in to_distribute:
            pc_list[i]['Parameter']['Weight']+=1

    #更新胜率表
    calculate.generate_newkf_in_for_vb()
    win_rate_new={}
    for i in range(option_visual.sum_size):
        if(i==index_chosen):
            continue

        elif(i<index_chosen):
            name_atk=pc_list[i]['Data']['Name']
            name_def=f"({group},{number})"
        elif(i>index_chosen):
            name_atk=f"({group},{number})"
            name_def=pc_list[i]['Data']['Name']
        
        calculate.vb(name_atk,name_def)
        win_rate=calculate.vb_result()
        item=f"({name_atk},{name_def})"
        win_rate_table[item]=win_rate
        win_rate_new[item]=win_rate
    
    win_rate_table_save()
    pc_list_save()

    #记录新胜率表
    file=info['File']
    with open(f"{file}\\win_rate_turn{turn}.json",mode='w+',encoding='UTF-8') as f:
        json.dump(win_rate_new,f,separators=(',',':'),indent=4)

    #记录新pc
    with open(f"{file}\\pc_turn{turn}.json",mode='w+',encoding='UTF-8') as f:
        json.dump(pc_chosen,f,separators=(',',':'),indent=4)

