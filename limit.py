import option_visual
import pc_form

import json
import random

lib=option_visual.lib
option=option_visual.option
sum_size=option_visual.sum_size

def stat(turn_start:int,turn_end:int):
    '''
    统计turn_start到turn_end（闭区间）的data，对每个角色分别统计Total,Gear,Aura,Attr，返回统计结果的字典
    '''
    #初始化stats的格式
    stats={}
    for role in lib['Role']:
        stats[role]={'Total':0,'Gear':{},'Aura':{},'Attr':{}}

        for item in lib['Gear']:
            stats[role]['Gear'][f"({item},0)"]=0
            if(lib['Gear'][item]['Myst']==True or lib['Gear'][item]['Myst']==role):
                stats[role]['Gear'][f"({item},1)"]=0
        
        for item in lib['Aura']:
            stats[role]['Aura'][item]=0
        
        for item in ['Str','Agi','Int','Vit','Spr','Mnd']:
            stats[role]['Attr'][item]=[0,0]

        del role
    
    with open('data 23-09-21\pc_turn0.json',mode='r',encoding='UTF-8') as f:
        pc_list=json.load(f)

    for i in range(1,turn_end+1):
        #按顺序获取pc_list
        with open(f"data 23-09-21\pc_turn{i}.json",mode='r',encoding='UTF-8') as f:
            pc_new=json.load(f)
    
        for j in range(sum_size):
            if(pc_list[j]['Data']['Name']==pc_new['Data']['Name']):
                pc_list[j]=pc_new
                break
        
        if(i<turn_start): #从i==turn_start才开始统计
            continue
        
        for pc in pc_list:
            role=pc['Data']['Role']
            stats[role]['Total']+=1

            for pos in ['Weapon','Hand','Body','Head']:
                gear=pc['Data'][pos]['Type']
                myst=pc['Data'][pos]['Myst']
                stats[role]['Gear'][f"({gear},{myst})"]+=1
                del gear,myst
            
            for aura in pc['Data']['Aura']['Skill']:
                stats[role]['Aura'][aura]+=1
            
            for item in ['Str','Agi','Int','Vit','Spr','Mnd']:
                attr=stats[role]['Attr'][item]
                attr_value=pc['Data']['Attribute'][item]

                if(attr[0]==0):
                    attr[0]=attr_value

                elif(attr_value<attr[0]):
                    attr[0]=attr_value
                
                if(attr_value>attr[1]):
                    attr[1]=attr_value

                del attr,attr_value
    
    return stats

def get_gear_list_no_limit(role):
    '''
    无限制：获取role所使用的装备列表，返回形如(item,0/1)组成的列表
    '''
    gear_list=[]

    for item in lib['Gear']:
        gear_list.append((item,0))
        if(lib['Gear'][item]['Myst']==True or lib['Gear'][item]['Myst']==role):
            gear_list.append((item,1))

    return gear_list

def get_aura_list_no_limit(role):
    '''
    无限制：获取role所使用的光环列表
    '''
    aura_list=[]
    for item in lib['Aura']:
        aura_list.append(item)

    return aura_list

def get_attr_range_no_limit(role):
    '''
    无限制：获取role所受的minattr和maxattr限制列表（返回元组）
    '''
    minattr=[1,1,1,1,1,1]
    maxattr=[0,0,0,0,0,0]
    attr_range=(minattr,maxattr)

    return attr_range

def generate_weak_limit():
    '''
    根据stats进行弱限制，得到概率分布，并保存至limit.json
    '''
    turn=option['Iteration']['Turns']
    stats=stat(1,turn)

    limit={}
    for role in lib['Role']:
        total=stats[role]['Total']
        limit[role]={'Gear':{},'Aura':{},'Attr':{}}
        if(total):
            for item in stats[role]['Gear']:
                f=stats[role]['Gear'][item]
                p=f/total+2/3
                if(p>1):
                    p=1
                limit[role]['Gear'][item]=p
            
            for item in stats[role]['Aura']:
                f=stats[role]['Aura'][item]
                p=f/total+2/3
                if(p>1):
                    p=1
                limit[role]['Aura'][item]=p
            
            for item in stats[role]['Attr']:
                limit[role]['Attr'][item]=stats[role]['Attr'][item]
        
        else: #total=0
            for item in stats[role]['Gear']:
                limit[role]['Gear'][item]=1
            
            for item in stats[role]['Aura']:
                limit[role]['Aura'][item]=1
            
            for item in stats[role]['Attr']:
                limit[role]['Attr'][item]=[0,0]
    
    #保存
    with open('limit.json',mode='w+',encoding='UTF-8') as f:
        json.dump(limit,f,separators=(',',':'),indent=4)

def generate_medium_limit():
    '''
    根据stats进行中限制，得到概率分布，并保存至limit.json
    '''
    turn=option['Iteration']['Turns']
    stats=stat(turn+1,turn*2)

    limit={}
    for role in lib['Role']:
        total=stats[role]['Total']
        if(total):
            limit[role]={'Gear':{},'Aura':{},'Attr':{}}

            for item in stats[role]['Gear']:
                f=stats[role]['Gear'][item]
                p=(f/total+0.5)/1.5
                limit[role]['Gear'][item]=p
            
            for item in stats[role]['Aura']:
                f=stats[role]['Aura'][item]
                p=(f/total+0.5)/1.5
                limit[role]['Aura'][item]=p
            
            for item in stats[role]['Attr']:
                limit[role]['Attr'][item]=stats[role]['Attr'][item]

        else: #total=0
            for item in stats[role]['Gear']:
                limit[role]['Gear'][item]=1
            
            for item in stats[role]['Aura']:
                limit[role]['Aura'][item]=1
            
            for item in stats[role]['Attr']:
                limit[role]['Attr'][item]=[0,0]
    
    #保存
    with open('limit.json',mode='w+',encoding='UTF-8') as f:
        json.dump(limit,f,separators=(',',':'),indent=4)

def generate_strong_limit():
    '''
    根据stats进行强限制，得到概率分布，并保存至limit.json
    '''
    turn=option['Iteration']['Turns']
    stats=stat(turn*2+1,turn*3)

    limit={}
    for role in lib['Role']:
        total=stats[role]['Total']
        if(total): #total为0时需特殊处理
            limit[role]={'Gear':{},'Aura':{},'Attr':{}}

            for item in stats[role]['Gear']:
                f=stats[role]['Gear'][item]
                p=(f/total+0.5)/1.5
                limit[role]['Gear'][item]=p
            
            for item in stats[role]['Aura']:
                f=stats[role]['Aura'][item]
                p=(f/total+0.5)/1.5
                limit[role]['Aura'][item]=p
            
            for item in stats[role]['Attr']:
                limit[role]['Attr'][item]=stats[role]['Attr'][item]

        else: #total=0
            for item in stats[role]['Gear']:
                limit[role]['Gear'][item]=1
            
            for item in stats[role]['Aura']:
                limit[role]['Aura'][item]=1
            
            for item in stats[role]['Attr']:
                limit[role]['Attr'][item]=[0,0]
    
    #保存
    with open('limit.json',mode='w+',encoding='UTF-8') as f:
        json.dump(limit,f,separators=(',',':'),indent=4)

def limit_load():
    '''
    读取limit.json，返回limit
    '''
    with open('limit.json',mode='r',encoding='UTF-8') as f:
        limit=json.load(f)
    
    return limit

def get_gear_list_limit(role):
    '''
    弱/中/强限制：获取role所使用的装备列表，返回形如(item,0/1)组成的列表
    '''
    limit=limit_load()
    
    gear_list=[]
    for item in limit[role]['Gear']:
        p=limit[role]['Gear'][item]
        x=random.random()
        if(x<=p):
            #item形如'(gear,myst)'，需转化为元组
            gear=item.split(',')[0][1:]
            myst=int(item.split(',')[1][0])
            gear_list.append((gear,myst))

            del gear,myst
    
    return gear_list

def get_aura_list_limit(role):
    '''
    弱/中/强限制：获取role所使用的光环列表
    '''
    limit=limit_load()
    
    aura_list=[]
    for item in limit[role]['Aura']:
        p=limit[role]['Aura'][item]
        x=random.random()
        if(x<=p):
            aura_list.append(item)
    
    return aura_list

def get_attr_range_weak_limit(role):
    '''
    弱限制：获取role所受的minattr和maxattr限制列表（返回元组）
    '''
    limit=limit_load()
    
    #获取最大点数
    level=option['Global variable']['Card']['Level']
    quality=option['Global variable']['Card']['Quality']
    point=int((3*level+6)*(1+0.01*quality))

    minattr=[]
    maxattr=[]
    for item in limit[role]['Attr']:
        attr=limit[role]['Attr'][item]
        x=random.random()
        if(x<=1/3): #1/3概率
            minattr.append(int((1+attr[0])/2))
        else:
            minattr.append(1)
        
        y=random.random()
        if(y<=1/3): #1/3概率
            maxattr.append(int((point+attr[1])/2))
        else:
            maxattr.append(0)

        del attr,x,y
    
    attr_range=(minattr,maxattr)
    return attr_range

def get_attr_range_medium_limit():
    '''
    中限制：获取role所受的minattr和maxattr限制列表（返回元组）
    '''

def get_attr_range_strong_limit():
    '''
    强限制：获取role所受的minattr和maxattr限制列表（返回元组）
    '''

