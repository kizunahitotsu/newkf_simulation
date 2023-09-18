import option_visual
import pc_form

import json
import copy
import random

lib=option_visual.lib
option=option_visual.option

with open('info.json',mode='r',encoding='UTF-8') as f:
    info=json.load(f)

#info={'Step':1,'Turn':0}

def check_wish():
    '''
    检查Wish列表长度是否为14
    '''
    if(option['Global variable']['Wish']):
        if(len(option['Global variable']['Wish'])!=14):
            print('Global variable的Wish列表长度不为14，请检查！')
            return False
    
    for group in option['Group']:
        if(option['Group'][group]['Wish']):
            if(len(option['Group'][group]['Wish'])!=14):
                print(f"第{group}组的Wish列表长度不为14，请检查！")
                return False
    
    return True

def generate_data(group:int):
    '''
    随机生成第group组的pc数据，返回data
    '''
    g=option['Group'][group]
    data=copy.deepcopy(pc_form.data_template)

    #初始化Card Wish Amulet Gear
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

    #生成固定项目
    data['Mode']=card['Mode']
    data['Level']=card['Level']
    data['Player level']=g['Player level']
    data['Skill slot']=card['Skill slot']
    data['Quality']=card['Quality']
    data['Wish']=wish
    data['Amulet']=amulet

    #生成随机Role Growth Time
    role=random.choice(list(lib['Role'].keys()))
    data['Role']=role
    
    if(lib['Role'][role]['Growth']):
        data['Growth']=card['Growth']

    if(lib['Role'][role]['Time']):
        data['Time']=random.choice([0,1])
    
    #生成随机Attribute
    point=int((3*data['Level']+6)*(1+0.01*data['Quality']))
    #随机前5项，需要满足和小于总点数
    while(True):
        attribute=[]
        for i in range(5):
            attribute.append(random.randrange(1,point))
        
        if(sum(attribute)<point):
            break
    
    attribute.append(point-sum(attribute))

    data['Attribute']['Str']=attribute[0]
    data['Attribute']['Agi']=attribute[1]
    data['Attribute']['Int']=attribute[2]
    data['Attribute']['Vit']=attribute[3]
    data['Attribute']['Spr']=attribute[4]
    data['Attribute']['Mnd']=attribute[5]

    #生成随机Gear
    #用(item,0/1)的形式记录装备名+神秘，只在模板基础上修改各装备属性
    weapon_list=[]
    hand_list=[]
    body_list=[]
    head_list=[]
    for item in lib['Gear']:
        if(lib['Gear'][item]['Position']=='Weapon'):
            weapon_list.append((item,0))
            if(lib['Gear'][item]['Myst']==True or lib['Gear'][item]['Myst']==role):
                weapon_list.append((item,1))
        
        elif(lib['Gear'][item]['Position']=='Hand'):
            hand_list.append((item,0))
            if(lib['Gear'][item]['Myst']==True or lib['Gear'][item]['Myst']==role):
                hand_list.append((item,1))
        
        elif(lib['Gear'][item]['Position']=='Body'):
            body_list.append((item,0))
            if(lib['Gear'][item]['Myst']==True or lib['Gear'][item]['Myst']==role):
                body_list.append((item,1))
        
        elif(lib['Gear'][item]['Position']=='Head'):
            head_list.append((item,0))
            if(lib['Gear'][item]['Myst']==True or lib['Gear'][item]['Myst']==role):
                head_list.append((item,1))

    weapon=random.choice(weapon_list)
    data['Weapon']['Type']=weapon[0]
    data['Weapon']['Level']=gear['Level']
    data['Weapon']['Myst']=weapon[1]
    if(weapon[1]):
        data['Weapon']['Percentage']=gear['Myst percentage']
    else:
        data['Weapon']['Percentage']=gear['Percentage']
    
    hand=random.choice(hand_list)
    data['Head']['Type']=hand[0]
    data['Head']['Level']=gear['Level']
    data['Head']['Myst']=hand[1]
    if(hand[1]):
        data['Head']['Percentage']=gear['Myst percentage']
    else:
        data['Head']['Percentage']=gear['Percentage']

    body=random.choice(body_list)
    data['Body']['Type']=body[0]
    data['Body']['Level']=gear['Level']
    data['Body']['Myst']=body[1]
    if(body[1]):
        data['Body']['Percentage']=gear['Myst percentage']
    else:
        data['Body']['Percentage']=gear['Percentage']
    
    head=random.choice(head_list)
    data['Head']['Type']=head[0]
    data['Head']['Level']=gear['Level']
    data['Head']['Myst']=head[1]
    if(head[1]):
        data['Head']['Percentage']=gear['Myst percentage']
    else:
        data['Head']['Percentage']=gear['Percentage']
    
    #生成随机Aura
    #不考虑300光环，那么由于SHI XIN FENG的存在，非0光环最少也能选4个，于是固定7技能
    data['Aura']['Amount']=7
    #直接随机会得到乱序，先随机选index，排序后再选取光环
    aura_list=list(lib['Aura'].keys())
    while(True):
        choice=random.sample(range(len(aura_list)),7)
        s=0
        for i in choice:
            s+=lib['Aura'][aura_list[i]]
        
        if(s<=g['Aura value']):
            break
    
    choice.sort()
    aura=[]
    for i in choice:
        aura.append(aura_list[i])
    
    data['Aura']['Skill']=aura
    
    return data

def initialize():
    '''
    初始化：随机生成初始data，添加参数形成pc，最后存储至pc.json
    '''
    #check_wish()放到iterate中进行，方便控制流程
    pc_list=[]

    for group in option['Group']:
        for number in range(1,option['Group'][group]['Size']+1):
            data=generate_data(group)
            data['Name']=f"({group},{number})"
            
            parameter=copy.deepcopy(pc_form.parameter_template)
            parameter['Group']=group
            parameter['Number']=number

            pc_list.append({'Data':data,'Parameter':parameter})

    with open('pc.json',mode='w+',encoding='UTF-8') as f:
        json.dump(pc_list,f,separators=(',',':'),indent=4)

