import option_visual
import pc_form

import json
import random

lib=option_visual.lib
option=option_visual.option
sum_size=option_visual.sum_size

def generate_stats(turn_start:int,turn_end:int):
    '''
    统计turn_start到turn_end（闭区间）的data，对每个角色分别统计Total,Gear,Aura,Attr，保存到stats.json
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
    
    with open('stats.json',mode='w+',encoding='UTF-8') as f:
        json.dump(stats,f,separators=(',',':'),indent=4)

def stats_load():
    '''
    读取stats.json
    '''
    with open('stats.json',mode='r',encoding='UTF-8') as f:
        stats=json.load(f)
    
    return stats

def get_gear_list_weak_limit(role):
    '''
    弱限制：获取role所使用的装备列表，返回形如(item,0/1)组成的列表
    '''
    stats=stats_load()
    total=stats[role]['Total']

    gear_list=[]
    if(total):
        for item in stats[role]['Gear']:
            f=stats[role]['Gear'][item]
            p=f/total+2/3
            if(p>1):
                p=1
            
            x=random.random()
            if(x<=p):
                #item形如'(gear,myst)'，需转化为元组
                gear=item.split(',')[0][1:]
                myst=int(item.split(',')[1][0])
                gear_list.append((gear,myst))
        
    else: #total=0单独处理
        gear_list=get_gear_list_no_limit(role)
    
    return gear_list

def get_aura_list_weak_limit(role):
    '''
    弱限制：获取role所使用的光环列表
    '''
    stats=stats_load()
    total=stats[role]['Total']

    aura_list=[]
    if(total):
        for item in stats[role]['Aura']:
            f=stats[role]['Aura'][item]
            p=f/total+2/3
            if(p>1):
                p=1
            
            x=random.random()
            if(x<=p):
                aura_list.append(item)
        
    else: #total=0单独处理
        aura_list=get_aura_list_no_limit(role)
    
    return aura_list

def get_attr_range_weak_limit(role):
    '''
    弱限制：获取role所受的minattr和maxattr限制列表（返回元组）
    '''
    stats=stats_load()
    
    #获取最大点数
    level=option['Global variable']['Card']['Level']
    quality=option['Global variable']['Card']['Quality']
    point=int((3*level+6)*(1+0.01*quality))

    minattr=[]
    maxattr=[]
    for item in stats[role]['Attr']:
        attr=stats[role]['Attr'][item]
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

        del attr
    
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

