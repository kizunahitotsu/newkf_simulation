import option_visual
import pc_form
import calculate
import initialize
import reset
import iteration_process
import limit

import json
import os
import time

try:
    open('info.json')
except:
    file_name='data '+time.strftime('%y-%m-%d',time.localtime())
    os.mkdir(file_name)

    info={'Step':1,'Turn':0,'File':file_name}
    with open('info.json',mode='w+',encoding='UTF-8') as f:
        json.dump(info,f,separators=(',',':'),indent=4)

with open('info.json',mode='r',encoding='UTF-8') as f:
    info=json.load(f)

def info_load():
    '''
    读取info
    '''
    global info
    with open('info.json',mode='r',encoding='UTF-8') as f:
        info=json.load(f)

def info_save():
    '''
    保存info
    '''
    with open('info.json',mode='w+',encoding='UTF-8') as f:
        json.dump(info,f,separators=(',',':'),indent=4)

turns=option_visual.option['Iteration']['Turns']

def iterate():
    '''
    迭代：分为9个步骤
    '''
    if(info['Step']==1):
        #第1步：初始化
        if(initialize.check_wish()): #先检查填写是否正确，否则迭代不开始
            initialize.initialize()

            info['Step']+=1
            info_save()

    if(info['Step']==2):
        #第2步：重置pc
        while True:
            if(info['Turn']>=option_visual.sum_size):
                break
            
            start_time=time.time()
            reset.reset()
            end_time=time.time()

            #保存结果至json，使得可以中断
            info['Turn']+=1
            info_save()
            print(f"已完成Step 2 Turn {info['Turn']}，用时{end_time-start_time} s！")
        
        info['Step']+=1
        info['Turn']=0
        info_save()
    
    if(info['Step']==3):
        #第3步：无限制迭代
        #初始化
        if(info['Turn']==0):
            iteration_process.set_weight()
            iteration_process.generate_win_rate_table()
            iteration_process.record_turn0()
        
        while True:
            if(info['Turn']>=turns):
                break

            start_time=time.time()
            iteration_process.iterate_main(limit=calculate.no_limit)
            end_time=time.time()

            info['Turn']+=1
            info_save()
            print(f"已完成Step 3 Turn {info['Turn']}，用时{end_time-start_time} s！")
    
        info['Step']+=1
        info_save()
    
    if(info['Step']==4):
        #第4步：统计，弱限制
        limit.generate_stats(1,turns)

        info['Step']+=1
        info_save()
    
    if(info['Step']==5):
        #第5步：弱限制迭代
        while True:
            if(info['Turn']>=turns*2):
                break

            start_time=time.time()
            iteration_process.iterate_main(limit=calculate.weak_limit)
            end_time=time.time()

            info['Turn']+=1
            info_save()
            print(f"已完成Step 3 Turn {info['Turn']}，用时{end_time-start_time} s！")
    
        info['Step']+=1
        info_save()

if __name__=='__main__':
    iterate()
    input()

