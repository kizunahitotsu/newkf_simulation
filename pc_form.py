import option_visual

import re
import copy

data_template={
    'Mode':'',
    'Weight':1,
    'Role':'LIN',
    'Name':'',
    'Growth':0,
    'Time':-1, #0白天1黑夜，非雅-1
    'Level':850,
    'Player level':1100,
    'Skill slot':7,
    'Quality':11,
    'Wish':[
        100,100, #绿色
        100,100,100, #蓝色
        200,200,200,200, #黄色
        50,50,50,50,50, #红色
    ],
    'Amulet':{
        'STR':0,
        'AGI':0,
        'INT':0,
        'VIT':0,
        'SPR':0,
        'MND':0,

        'PATK':0,
        'MATK':0,
        'SPD':0,
        'REC':0,
        'HP':0,
        'SLD':0,

        'LCH':0,
        'RFL':0,
        'CRT':0,
        'SKL':0,
        'PDEF':0,
        'MDEF':0,

        'AAA':0,
        'CRTR':0,
        'SKLR':0,
    },
    'Attribute':{
        'Str':1,
        'Agi':1,
        'Int':1,
        'Vit':1,
        'Spr':1,
        'Mnd':1,
    },
    'Weapon':{
        'Type':'BLADE',
        'Level':300,
        'Percentage':[150,150,150,150],
        'Myst':1,
    },
    'Hand':{
        'Type':'RING',
        'Level':300,
        'Percentage':[150,150,150,150],
        'Myst':0,
    },
    'Body':{
        'Type':'CLOAK',
        'Level':300,
        'Percentage':[150,150,150,150],
        'Myst':1,
    },
    'Head':{
        'Type':'TIARA',
        'Level':300,
        'Percentage':[150,150,150,150],
        'Myst':0,
    },
    'Aura':{
        'Amount':7,
        'Skill':['XIN','FENG','DUN','SHANG','ZHI','JU','JUE'],
    },
}

parameter_template={
    'Turn':0, #用于定位
    'Group':1,
    'Number':1,
    'Weight':1, #迭代选择pc的权重，不是pc数据
    'Mark':False, #迭代选择pc的标记
}

pc_template={
    'Data':data_template,
    'Parameter':parameter_template,
}

def data_dict_to_str(data:dict):
    '''
    将pc数据由字典形式转化为字符串
    '''
    #直接列出各项属性，pc格式有变时方便检查
    '''
    ?ATK ?W=2 YA?_a ?G=3 ?M=1 850 1500 7 11
    WISH 0*14
    ?AMULET AAA 10 ENDAMULET
    1 1 1 1 2837 1
    NONE
    NONE
    CLOAK 300 150 150 150 150 1
    NONE
    1 BO
    '''
    s_list=[]

    #第1行
    if(data['Mode']):
        s_list.append(data['Mode']+' ')
    
    if(data['Weight']!=1):
        s_list.append(f"W={data['Weight']} ")
    
    s_list.append(data['Role'])

    if(data['Name']):
        s_list.append('_'+data['Name'])
    
    s_list.append(' ')

    if(data['Growth']):
        s_list.append(f"G={data['Growth']} ")

    if(data['Time']>-1):
        s_list.append(f"M={data['Time']} ")

    s_list.append(f"{data['Level']} ")
    s_list.append(f"{data['Player level']} ")
    s_list.append(f"{data['Skill slot']} ")
    s_list.append(f"{data['Quality']}\n")

    #第2行
    s_list.append(f"WISH {' '.join(map(str,data['Wish']))}\n")

    #第3行
    if(sum(data['Amulet'].values())>0):
        s_list.append('AMULET ')

        for item in data['Amulet']:
            if(data['Amulet'][item]):
                s_list.append(item+' '+str(data['Amulet'][item])+' ')
        
        s_list.append('ENDAMULET\n')
    
    #第4行
    s_list.append(f"{data['Attribute']['Str']} ")
    s_list.append(f"{data['Attribute']['Agi']} ")
    s_list.append(f"{data['Attribute']['Int']} ")
    s_list.append(f"{data['Attribute']['Vit']} ")
    s_list.append(f"{data['Attribute']['Spr']} ")
    s_list.append(f"{data['Attribute']['Mnd']} \n")

    #第5-8行
    s_list.append(f"{data['Weapon']['Type']} ")
    s_list.append(f"{data['Weapon']['Level']} ")
    s_list.append(' '.join(map(str,data['Weapon']['Percentage'])))
    s_list.append(f" {data['Weapon']['Myst']}\n")
    
    s_list.append(f"{data['Hand']['Type']} ")
    s_list.append(f"{data['Hand']['Level']} ")
    s_list.append(' '.join(map(str,data['Hand']['Percentage'])))
    s_list.append(f" {data['Hand']['Myst']}\n")
    
    s_list.append(f"{data['Body']['Type']} ")
    s_list.append(f"{data['Body']['Level']} ")
    s_list.append(' '.join(map(str,data['Body']['Percentage'])))
    s_list.append(f" {data['Body']['Myst']}\n")
    
    s_list.append(f"{data['Head']['Type']} ")
    s_list.append(f"{data['Head']['Level']} ")
    s_list.append(' '.join(map(str,data['Head']['Percentage'])))
    s_list.append(f" {data['Head']['Myst']}\n")

    #第9行
    s_list.append(f"{data['Aura']['Amount']} ")
    s_list.append(f"{' '.join(data['Aura']['Skill'])}")

    s=''.join(s_list)

    return s

def data_str_to_dict(s:str):
    '''
    将pc数据由字符串形式转化为字典
    '''
    data=copy.deepcopy(data_template)
    '''
    ?ATK ?W=2 YA?_a ?G=3 ?M=1 850 1500 7 11
    WISH 0*14
    ?AMULET AAA 10 ENDAMULET
    1 1 1 1 2837 1
    NONE
    NONE
    CLOAK 300 150 150 150 150 1
    NONE
    1 BO
    '''
    pattern_list=[]

    #第1行
    pattern_list.append(r'(?:(?P<Mode>ATK|DEF) )?')
    pattern_list.append(r'(?:W=(?P<Weight>\d+) )?')
    pattern_list.append(r'(?P<Role>[A-Z]+)')
    pattern_list.append(r'(?:_(?P<Name>[^ ]+))? ')
    pattern_list.append(r'(?:G=(?P<Growth>\d+) )?')
    pattern_list.append(r'(?:M=(?P<Time>[01]) )?')
    pattern_list.append(r'(?P<Level>\d+) ')
    pattern_list.append(r'(?P<Player_level>\d+) ')
    pattern_list.append(r'(?P<Skill_slot>\d+) ')
    pattern_list.append(r'(?P<Quality>\d+)\n')

    #第2行
    pattern_list.append(r'(?:WISH (?P<Wish>[\d ]+)\n)')

    #第3行
    pattern_list.append(r'(?:AMULET (?P<Amulet>[A-Z\d ]+) ENDAMULET\n)?')

    #第4行
    pattern_list.append(r'(?P<Attribute>[\d ]+)\n')

    #第5-8行
    pattern_list.append(r'(?P<Weapon>[A-Z]+[\d ]+)\n')
    pattern_list.append(r'(?P<Hand>[A-Z]+[\d ]+)\n')
    pattern_list.append(r'(?P<Body>[A-Z]+[\d ]+)\n')
    pattern_list.append(r'(?P<Head>[A-Z]+[\d ]+)\n')

    #第9行
    pattern_list.append(r'(?P<Aura>\d+[A-Z ]+)')

    pattern=''.join(pattern_list)
    match=re.match(pattern,s)

    if match['Mode']:
        data['Mode']=match['Mode']
    else:
        data['Mode']=''
    
    if match['Weight']:
        data['Weight']=int(match['Weight'])
    else:
        data['Weight']=1
    
    data['Role']=match['Role']

    if match['Name']:
        data['Name']=match['Name']
    else:
        data['Name']=''
    
    if match['Growth']:
        data['Growth']=int(match['Growth'])
    else:
        data['Growth']=0
    
    if match['Time']:
        data['Time']=int(match['Time'])
    elif(option_visual.lib['Role'][match['Role']]['Time']): #有time的角色不显示time默认为0
        data['Time']=0
    else:
        data['Time']=-1
    
    data['Level']=int(match['Level'])
    data['Player level']=int(match['Player_level'])
    data['Skill slot']=int(match['Skill_slot'])
    data['Quality']=int(match['Quality'])

    data['Wish']=list(map(int,match['Wish'].split()))
    
    if match['Amulet']:
        temp=match['Amulet'].split()
        for i in range(0,len(temp),2):
            data['Amulet'][temp[i]]=int(temp[i+1])
        
        del temp

    else:
        for item in data['Amulet']:
            data['Amulet'][item]=0
    
    temp=match['Attribute'].split()
    data['Attribute']['Str']=int(temp[0])
    data['Attribute']['Agi']=int(temp[1])
    data['Attribute']['Int']=int(temp[2])
    data['Attribute']['Vit']=int(temp[3])
    data['Attribute']['Spr']=int(temp[4])
    data['Attribute']['Mnd']=int(temp[5])
    del temp
    
    temp=match['Weapon'].split()
    data['Weapon']['Type']=temp[0]
    data['Weapon']['Level']=int(temp[1])
    data['Weapon']['Percentage']=list(map(int,temp[2:6]))
    data['Weapon']['Myst']=int(temp[6])
    del temp
    
    temp=match['Hand'].split()
    data['Hand']['Type']=temp[0]
    data['Hand']['Level']=int(temp[1])
    data['Hand']['Percentage']=list(map(int,temp[2:6]))
    data['Hand']['Myst']=int(temp[6])
    del temp
    
    temp=match['Body'].split()
    data['Body']['Type']=temp[0]
    data['Body']['Level']=int(temp[1])
    data['Body']['Percentage']=list(map(int,temp[2:6]))
    data['Body']['Myst']=int(temp[6])
    del temp
    
    temp=match['Head'].split()
    data['Head']['Type']=temp[0]
    data['Head']['Level']=int(temp[1])
    data['Head']['Percentage']=list(map(int,temp[2:6]))
    data['Head']['Myst']=int(temp[6])
    del temp
    
    temp=match['Aura'].split()
    data['Aura']['Amount']=int(temp[0])
    data['Aura']['Skill']=temp[1:]
    del temp

    return data

