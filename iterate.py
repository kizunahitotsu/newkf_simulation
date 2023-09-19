import option_visual
import pc_form
import initialize
import reset

import json
import os
import time

option=option_visual.option

try:
    open('info.json')
except:
    info={'Step':1,'Turn':0}
    with open('info.json',mode='w+',encoding='UTF-8') as f:
        json.dump(info,f,separators=(',',':'),indent=4)

with open('info.json',mode='r',encoding='UTF-8') as f:
    info=json.load(f)

def info_load():
    global info
    with open('info.json',mode='r',encoding='UTF-8') as f:
        info=json.load(f)

def info_save():
    with open('info.json',mode='w+',encoding='UTF-8') as f:
        json.dump(info,f,separators=(',',':'),indent=4)


def iterate():
    '''
    迭代：分为9个步骤
    '''
    sum_size=0
    for group in option['Group']:
        sum_size+=option['Group'][group]['Size']
    
    if(info['Step']==1):
        #第1步：初始化
        if(initialize.check_wish()): #先检查填写是否正确，否则迭代不开始
            initialize.initialize()

            info['Step']+=1
            info_save()

    if(info['Step']==2):
        #第2步：重置pc
        while(True):
            if(info['Turn']==sum_size):
                break
            
            start_time=time.time()
            reset.reset()
            end_time=time.time()

            #保存结果至json，使得可以中断
            info['Turn']+=1
            info_save()
            print(f"已完成Step 2 Turn {info['Turn']}，用时{end_time-start_time} s！")
        
        info['Step']+=1
        info_save()
    
    if(info['Step']==3):
        pass


iterate()

