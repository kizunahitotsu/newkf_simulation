import option_visual
import pc_form
import limit

import json
import copy
import random
import re
import os

lib=option_visual.lib
option=option_visual.option

def no_limit(role):
    '''
    无限制：获取迭代所使用的参数(gear_list,aura_list,attr_range)
    '''
    gear_list=limit.get_gear_list_no_limit(role)
    aura_list=limit.get_aura_list_no_limit(role)
    attr_range=limit.get_attr_range_no_limit(role)

    param_limit=(gear_list,aura_list,attr_range)

    return param_limit

def weak_limit(role):
    '''
    弱限制：获取迭代所使用的参数(gear_list,aura_list,attr_range)
    '''
    gear_list=limit.get_gear_list_limit(role)
    aura_list=limit.get_aura_list_limit(role)
    attr_range=limit.get_attr_range_weak_limit(role)

    param_limit=(gear_list,aura_list,attr_range)

    return param_limit

def medium_limit(role):
    pass

def strong_limit(role):
    pass

def generate_newkf_in_for_apc(group,number,role,time=-1,limit=no_limit):
    '''
    为计算apc，对于第group组第number号位的role和time，生成对应newkf.in
    '''
    #获取信息
    g=option['Group'][group]

    #获取Card Wish Amulet Gear
    card=copy.deepcopy(option['Global variable']['Card'])
    for item in g['Card']:
        card[item]=g['Card'][item]

    wish=copy.deepcopy(option['Global variable']['Wish'])
    if(g['Wish']):
        wish=copy.deepcopy(g['Wish'])

    amulet=copy.deepcopy(option['Global variable']['Amulet'])
    for item in g['Amulet']:
        amulet[item]=g['Amulet'][item]

    gear=copy.deepcopy(option['Global variable']['Gear'])
    for item in g['Gear']:
        gear[item]=g['Gear'][item]
    
    #获取gear_list,aura_list,minattr,maxattr
    param_limit=limit(role)
    gear_list=param_limit[0]
    aura_list=param_limit[1]
    attr_range=param_limit[2]
    minattr=attr_range[0]
    maxattr=attr_range[1]
    
    #获取算点参数
    option_visual.iteration_load() #更新iteration信息，方便修改调试
    threads=option['Iteration']['Threads']
    seedmax=option['Iteration']['Seedmax']
    tests=option['Iteration']['Tests_apc']
    citest=option['Iteration']['Citest_apc']
    verbose=option['Iteration']['Verbose']
    
    #获取pc列表
    with open('pc.json',mode='r',encoding='UTF-8') as f:
        pc_list=json.load(f)

    #填写newkf.in
    '''
    280

    YA G=3 M=1 850 909 6 10
    WISH 44 43 43 30 36 30 29 53 38 21 17 17 17 17
    AMULET AAA 10 ENDAMULET
    1 1 1 1 1 1
    NONE
    NONE
    NONE
    NONE
    0

    NPC
    ENDNPC

    PC


    ENDPC

    GEAR

    ENDGEAR

    THREADS 12
    TESTS 10000
    CITEST 0
    MAXATTR 0 0 0 0 0 0
    SEEDMAX 50000
    AURAFILTER TIAO_YA
    DEFENDER 0
    VERBOSE 1
    '''
    newkf_in_list=[]
    #第1-2行
    newkf_in_list.append(f"{g['Aura value']}\n\n")

    #第3行
    newkf_in_list.append(role+' ')

    if(lib['Role'][role]['Growth']):
        newkf_in_list.append(f"G={card['Growth']} ")
    
    if(lib['Role'][role]['Time']):
        newkf_in_list.append(f"M={time} ")
    
    newkf_in_list.append(f"{card['Level']} ")
    newkf_in_list.append(f"{g['Player level']} ")
    newkf_in_list.append(f"{card['Skill slot']} ")
    newkf_in_list.append(f"{card['Quality']}\n")

    #第4行
    newkf_in_list.append(f"WISH {' '.join(map(str,wish))}\n")

    #第5行
    if(sum(amulet.values())>0):
        newkf_in_list.append('AMULET ')

        for item in amulet:
            if(amulet[item]):
                newkf_in_list.append(item+' '+str(amulet[item])+' ')
        
        newkf_in_list.append('ENDAMULET\n')
    
    #第6行：minattr
    newkf_in_list.append(' '.join(map(str,minattr))+' \n')
    
    #第7-12行
    newkf_in_list.append('NONE\n'*4+'0\n\n')

    #第13-15行
    newkf_in_list.append('NPC\nENDNPC\n\n')
    
    #第16+行：pc列表
    newkf_in_list.append('PC\n')
    for pc in pc_list:
        if(pc['Parameter']['Group']==group and pc['Parameter']['Number']==number):
            pass
        else:
            newkf_in_list.append(pc_form.data_dict_to_str(pc['Data'])+'\n\n')

    newkf_in_list.append('ENDPC\n\n')

    #gear列表
    newkf_in_list.append('GEAR\n')

    for item in gear_list:
        newkf_in_list.append(item[0]+' ')
        newkf_in_list.append(f"{gear['Level']} ")
        if(item[1]): #神秘
            newkf_in_list.append(' '.join(map(str,gear['Myst percentage'])))
        else: #非神秘
            newkf_in_list.append(' '.join(map(str,gear['Percentage'])))
        
        newkf_in_list.append(f" {item[1]}\n")
    
    newkf_in_list.append('ENDGEAR\n\n')

    #配置部分：8行
    newkf_in_list.append(f"THREADS {threads}\n")
    newkf_in_list.append(f"TESTS {tests}\n")
    newkf_in_list.append(f"CITEST {citest}\n")
    newkf_in_list.append(f"MAXATTR {' '.join(map(str,maxattr))}\n")
    newkf_in_list.append(f"SEEDMAX {seedmax}\n")

    #AURAFILTER，暂时默认禁用TIAO和YA
    aurafilter=[]
    for item in lib['Aura']:
        if(item not in aura_list):
            aurafilter.append(item)
    
    newkf_in_list.append('AURAFILTER TIAO_YA')
    if(aurafilter):
        newkf_in_list.append('_')
        newkf_in_list.append('_'.join(aurafilter))
    
    newkf_in_list.append('\n')

    newkf_in_list.append('DEFENDER 0\n') #暂时不分攻守
    newkf_in_list.append(f"VERBOSE {verbose}\n")

    newkf_in=''.join(newkf_in_list)
    
    with open('newkf.in',mode='w+',encoding='UTF-8') as f:
        f.write(newkf_in)

def apc():
    '''
    进行apc算点，结果输出至output.txt
    '''
    with open('input.txt',mode='w+',encoding='UTF-8') as f:
        f.write('apc\nq\n')
    
    os.system('newkf_64.exe < input.txt > output.txt')

def apc_result():
    '''
    apc计算完成后，读取output.txt，返回算点结果（字符串）和胜率组成的元组
    '''
    with open('output.txt',mode='r',encoding='UTF-8') as f:
        output=f.readlines()
    
    #定位到'Attribute Result:'
    while True:
        output=output[1:]
        if(output[0]=='Attribute Result:\n'):
            break
    
    #再往下1行为算点结果
    output=output[1:]
    result_list=[]

    #定位到算点结果后面的空行
    while True:
        result_list.append(output[0])
        output=output[1:]
        if(output[0]=='\n'):
            break
    
    result_list[-1]=result_list[-1].rstrip() #去掉最后一个\n，保持格式
    result=''.join(result_list)
    
    #定位到'Average Win Rate :'
    while True:
        output=output[1:]
        if(output[0].startswith('Average Win Rate :')):
            break
    
    win_rate=float(re.search(r'[\d\.]+',output[0]).group())
    
    return (result,win_rate)

def apc_all(group,number,limit=no_limit):
    '''
    对第group组第number号位，以其他pc为对手进行apc，取所有role胜率最高的，返回最终算点结果（字典）
    '''
    result_win_rate_list=[]
    for role in lib['Role']:
        if(lib['Role'][role]['Time']):
            #等计算器作者把雅的问题修了就加上这段
            '''
            generate_newkf_in_for_apc(group,number,role,time=0,limit=limit)
            apc()
            result_win_rate_list.append(apc_result())
            '''

            generate_newkf_in_for_apc(group,number,role,time=1,limit=limit)
            apc()
            result_win_rate_list.append(apc_result())
        else:
            generate_newkf_in_for_apc(group,number,role,time=-1,limit=limit)
            apc()
            result_win_rate_list.append(apc_result())
        
    result_win_rate_list.sort(key=lambda t:t[1],reverse=True) #对胜率从高到低排序
    result_dict=pc_form.data_str_to_dict(result_win_rate_list[0][0])
    result_dict['Name']=f"({group},{number})" #计算结果不包含Name，补上

    #等计算器作者把雅的问题修了就删掉这段
    if(result_dict['Role']=='YA'):
        result_dict['Time']=1
    return result_dict

def generate_newkf_in_for_vb():
    '''
    为计算vb，生成newkf.in
    '''
    #获取pc列表
    with open('pc.json',mode='r',encoding='UTF-8') as f:
        pc_list=json.load(f)
    
    #获取算点参数
    option_visual.iteration_load() #更新iteration信息，方便修改调试
    threads=option['Iteration']['Threads']
    seedmax=option['Iteration']['Seedmax']
    tests=option['Iteration']['Tests_vb']
    citest=option['Iteration']['Citest_vb']
    verbose=option['Iteration']['Verbose']

    '''
    280

    YA 850 900 7 11
    1 1 1 1 1 1 
    NONE
    NONE
    NONE
    NONE
    0

    NPC
    ENDNPC

    PC


    ENDPC

    GEAR
    ENDGEAR

    THREADS 12
    TESTS 10000
    CITEST 0
    SEEDMAX 50000
    DEFENDER 0
    VERBOSE 0
    '''
    newkf_in_list=[
        '280\n\n', #第1-2行
        'YA 850 900 7 11\n', #第3行
        '1 1 1 1 1 1 \n', #第4行
        'NONE\n'*4, #第5-8行
        '0\n\n', #第9-10行
        'NPC\nENDNPC\n\n', #第11-13行
        'PC\n',
    ]

    for pc in pc_list:
        newkf_in_list.append(pc_form.data_dict_to_str(pc['Data'])+'\n\n')
    
    newkf_in_list.append('ENDPC\n\n')
    newkf_in_list.append('GEAR\nENDGEAR\n\n')

    #配置部分
    newkf_in_list.append(f"THREADS {threads}\n")
    newkf_in_list.append(f"TESTS {tests}\n")
    newkf_in_list.append(f"CITEST {citest}\n")
    newkf_in_list.append(f"SEEDMAX {seedmax}\n")
    newkf_in_list.append('DEFENDER 0\n')
    newkf_in_list.append(f"VERBOSE {verbose}\n")

    newkf_in=''.join(newkf_in_list)
    
    with open('newkf.in',mode='w+',encoding='UTF-8') as f:
        f.write(newkf_in)

def vb(pc_name_atk:str,pc_name_def:str):
    '''
    进行apc算点，结果输出至output.txt
    '''
    with open('input.txt',mode='w+',encoding='UTF-8') as f:
        f.write(f"vb PC {pc_name_atk} PC {pc_name_def}\nq\n")
    
    os.system('newkf_64.exe < input.txt > output.txt')

def vb_result():
    '''
    vb计算完成后，读取output.txt，返回(胜场数,败场数,平场数)元组
    '''
    with open('output.txt',mode='r',encoding='UTF-8') as f:
        output=f.readlines()
    
    #定位到'Win Rate :'
    while True:
        output=output[1:]
        if(output[0].startswith('Win Rate :')):
            break
    
    match=re.search(r'(\d+)/(\d+)',output[0]) #胜场数/非平场数
    win=int(match[1])
    lose=int(match[2])-win

    match=re.search(r'D=(\d+)',output[0])
    draw=int(match[1])

    return (win,lose,draw)

