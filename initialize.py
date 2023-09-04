import option_visual
import pc_form

import json
import copy
import random

lib=option_visual.lib
option=option_visual.option

def generate_data(group):
    g=option['Group'][group]
    data=copy.deepcopy(pc_form.data_template)

    #初始化Card Wish Amulet Gear
    card=copy.deepcopy(option['Global variable']['Card'])
    for item in g['Card']:
        card[item]=g['Card'][item]

    wish=copy.deepcopy(option['Global variable']['Wish'])
    if(g['Wish']):
        #确保Wish是14项列表，若不是则按照全局变量
        if(len(g['Wish'])==14):
            wish=copy.deepcopy(g['Wish'])
        else:
            print(f"第{group}组内Wish列表长度有误！")

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
    #并不是完全均匀的随机，不过管他呢
    point=int((3*data['Level']+6)*(1+0.01*data['Quality']))
    point-=6 #每个属性至少分配1点
    rand=[]
    attribute=[]
    for i in range(6):
        rand.append(random.random())
    
    s=sum(rand)
    for i in range(6):
        rand[i]/=s
        attribute.append(int(point*rand[i]))
    
    #由于取整，属性和可能比point少，随机补足
    while(sum(attribute)<point):
        attribute[random.randrange(0,6)]+=1
    
    #最后补上至少分配的1点属性
    data['Attribute']['Str']=attribute[0]+1
    data['Attribute']['Agi']=attribute[1]+1
    data['Attribute']['Int']=attribute[2]+1
    data['Attribute']['Vit']=attribute[3]+1
    data['Attribute']['Spr']=attribute[4]+1
    data['Attribute']['Mnd']=attribute[5]+1

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
    
    return data


#data['Name']=f"({group},{number})"
print(pc_form.data_dict_to_str(generate_data(1)))
