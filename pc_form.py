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
    'Turn':1, #用于定位
    'Group':1,
    'Number':1,
    'Weight':1,
    'Mark':False,
}

pc_template={
    'Data':data_template,
    'Parameter':parameter_template,
}

def data_dict_to_str(data):
    #直接列出各项属性，PC格式有变时方便检查
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
    s=''
    if(data['Mode']):
        s+=data['Mode']+' '
    
    if(data['Weight']!=1):
        s+=f"W={data['Weight']} "
    
    s+=data['Role']

    if(data['Name']):
        s+='_'+data['Name']
    
    s+=' '

    if(data['Growth']):
        s+=f"G={data['Growth']} "

    if(data['Time']>-1):
        s+=f"M={data['Time']} "

    s+=f"{data['Level']} "
    s+=f"{data['Player level']} "
    s+=f"{data['Skill slot']} "
    s+=f"{data['Quality']}\n"

    s+=f"WISH {' '.join(map(str,data['Wish']))}\n"
    
    if(sum(data['Amulet'].values())>0):
        s+='AMULET '

        for item in data['Amulet']:
            if(data['Amulet'][item]):
                s+=item+' '+str(data['Amulet'][item])+' '
        
        s+='ENDAMULET\n'
    
    s+=f"{data['Attribute']['Str']} "
    s+=f"{data['Attribute']['Agi']} "
    s+=f"{data['Attribute']['Int']} "
    s+=f"{data['Attribute']['Vit']} "
    s+=f"{data['Attribute']['Spr']} "
    s+=f"{data['Attribute']['Mnd']} \n"

    s+=f"{data['Weapon']['Type']} "
    s+=f"{data['Weapon']['Level']} "
    s+=' '.join(map(str,data['Weapon']['Percentage']))
    s+=f" {data['Weapon']['Myst']}\n"
    
    s+=f"{data['Hand']['Type']} "
    s+=f"{data['Hand']['Level']} "
    s+=' '.join(map(str,data['Hand']['Percentage']))
    s+=f" {data['Hand']['Myst']}\n"
    
    s+=f"{data['Body']['Type']} "
    s+=f"{data['Body']['Level']} "
    s+=' '.join(map(str,data['Body']['Percentage']))
    s+=f" {data['Body']['Myst']}\n"
    
    s+=f"{data['Head']['Type']} "
    s+=f"{data['Head']['Level']} "
    s+=' '.join(map(str,data['Head']['Percentage']))
    s+=f" {data['Head']['Myst']}\n"

    s+=f"{data['Aura']['Amount']} "
    s+=f"{' '.join(data['Aura']['Skill'])}"
    return s

def data_str_to_dict(s):
    data=copy.deepcopy(data_template)

    pattern=r'(?:(?P<Mode>ATK|DEF) )?'
    pattern+=r'(?:W=(?P<Weight>\d+) )?'
    pattern+=r'(?P<Role>[A-Z]+)'
    pattern+=r'(?:_(?P<Name>[^ ]+))? '
    pattern+=r'(?:G=(?P<Growth>\d+) )?'
    pattern+=r'(?:M=(?P<Time>[01]) )?'
    pattern+=r'(?P<Level>\d+) '
    pattern+=r'(?P<Player_level>\d+) '
    pattern+=r'(?P<Skill_slot>\d+) '
    pattern+=r'(?P<Quality>\d+)\n'

    pattern+=r'(?:WISH (?P<Wish>[\d ]+)\n)'

    pattern+=r'(?:AMULET (?P<Amulet>[A-Z\d ]+) ENDAMULET\n)?'

    pattern+=r'(?P<Attribute>[\d ]+)\n'

    pattern+=r'(?P<Weapon>[A-Z]+[\d ]+)\n'
    pattern+=r'(?P<Hand>[A-Z]+[\d ]+)\n'
    pattern+=r'(?P<Body>[A-Z]+[\d ]+)\n'
    pattern+=r'(?P<Head>[A-Z]+[\d ]+)\n'

    pattern+=r'(?P<Aura>\d+[A-Z ]+)'

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

