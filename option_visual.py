import json

lib={
    'Role':{
        'WU':{'Growth':True,'Time':False},
        'MO':{'Growth':False,'Time':False},
        'LIN':{'Growth':False,'Time':False},
        'AI':{'Growth':False,'Time':False},
        'MENG':{'Growth':False,'Time':False},
        'WEI':{'Growth':False,'Time':False},
        'YI':{'Growth':False,'Time':False},
        'MING':{'Growth':False,'Time':False},
        'MIN':{'Growth':False,'Time':False},
        'XI':{'Growth':True,'Time':False},
        'XIA':{'Growth':True,'Time':False},
        'YA':{'Growth':False,'Time':True},
    },
    'Gear':{
        'SWORD':{'Position':'Weapon','Myst':False},
        'BOW':{'Position':'Weapon','Myst':False},
        'STAFF':{'Position':'Weapon','Myst':False},
        'BLADE':{'Position':'Weapon','Myst':True},
        'ASSBOW':{'Position':'Weapon','Myst':True},
        'DAGGER':{'Position':'Weapon','Myst':'AI'},
        'WAND':{'Position':'Weapon','Myst':'MO'},
        'SHIELD':{'Position':'Weapon','Myst':True},
        'CLAYMORE':{'Position':'Weapon','Myst':True},
        'SPEAR':{'Position':'Weapon','Myst':True},
        'COLORFUL':{'Position':'Weapon','Myst':'YI'},
        'LIMPIDWAND':{'Position':'Weapon','Myst':'XIA'},

        'GLOVES':{'Position':'Hand','Myst':False},
        'BRACELET':{'Position':'Hand','Myst':True},
        'VULTURE':{'Position':'Hand','Myst':True},
        'RING':{'Position':'Hand','Myst':'WU'},
        'DEVOUR':{'Position':'Hand','Myst':'MING'},
        'REFRACT':{'Position':'Hand','Myst':'MIN'},

        #'PLATE':{'Position':'Body','Myst':False},
        #'LEATHER':{'Position':'Body','Myst':False},
        #'CLOTH':{'Position':'Body','Myst':False},
        #禁用三废甲
        'CLOAK':{'Position':'Body','Myst':True},
        'THORN':{'Position':'Body','Myst':True},
        'WOOD':{'Position':'Body','Myst':True},
        'CAPE':{'Position':'Body','Myst':True},
        
        'SCARF':{'Position':'Head','Myst':False},
        'TIARA':{'Position':'Head','Myst':'MENG'},
        'RIBBON':{'Position':'Head','Myst':'LIN'},
        'HUNT':{'Position':'Head','Myst':'WEI'},
        'FIERCE':{'Position':'Head','Myst':'YA'},
    },
    'Aura':{
        'SHI':0,
        'XIN':0,
        'FENG':0,
        #'TIAO':0,
        #'YA':0,
        #禁用TIAO和YA，因为等级都一样
        
        'BI':20,
        'MO':20,
        'DUN':20,
        'XUE':20,
        'XIAO':20,
        'SHENG':20,
        'E':20,
        
        'SHANG':30,
        'SHEN':30,
        'CI':30,
        'REN':30,
        'RE':30,
        'DIAN':30,
        'WU':30,
        'ZHI':30,
        'SHAN':30,
        
        'FEI':100,
        'BO':100,
        'JU':100,
        'HONG':100,
        'JUE':100,
        'HOU':100,
        'DUNH':100,
        'ZI':100,
    },
}

option={
    'Iteration':{
        'Turns':300,
        'Threads':12,
        'Seedmax':10000,
        'Tests_apc':10, #citest=0时test才生效
        'Citest_apc':20,
        'Tests_vb':10000,
        'Citest_vb':1,
        'Verbose':0, #verbose=1用于调试，平时=0
    },
    'Global variable':{
        'Card':{
            'Mode':'',
            'Level':900, #护符的苹果部分归入等级
            'Growth':100000,
            'Skill slot':7,
            'Quality':11,
        },
        'Wish':[
            100,100, #绿色
            94,94,94, #蓝色 抵消模拟成900级变高的部分
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

            'PATK':10,
            'MATK':10,
            'SPD':10,
            'REC':10,
            'HP':10,
            'SLD':10,

            'LCH':10,
            'RFL':10,
            'CRT':10,
            'SKL':10,
            'PDEF':10,
            'MDEF':10,

            'AAA':10,
            'CRTR':3,
            'SKLR':3,
        },
        'Gear':{
            'Level':300,
            'Percentage':[150,150,150,150],
            'Myst percentage':[140,140,140,140],
        },
    },
    #若分组内变量为空，则使用相应全局变量
    #支持单独设置Card Amulet Gear（会覆盖全局变量相应项），支持单独设置Wish（应为完整14项列表）

    #钦定800-1600的一个近似正态分布，总数为100
    'Group':{
        1:{'Player level':800,'Aura value':270,'Size':3,
            'Card':{},'Wish':[],'Amulet':{},'Gear':{},},
        2:{'Player level':900,'Aura value':270,'Size':7,
            'Card':{},'Wish':[],'Amulet':{},'Gear':{},},
        3:{'Player level':1000,'Aura value':280,'Size':12,
            'Card':{},'Wish':[],'Amulet':{},'Gear':{},},
        4:{'Player level':1100,'Aura value':280,'Size':18,
            'Card':{},'Wish':[],'Amulet':{},'Gear':{},},
        5:{'Player level':1200,'Aura value':280,'Size':20,
            'Card':{},'Wish':[],'Amulet':{},'Gear':{},},
        6:{'Player level':1300,'Aura value':280,'Size':18,
            'Card':{},'Wish':[],'Amulet':{},'Gear':{},},
        7:{'Player level':1400,'Aura value':280,'Size':12,
            'Card':{},'Wish':[],'Amulet':{},'Gear':{},},
        8:{'Player level':1500,'Aura value':290,'Size':10,
            'Card':{},'Wish':[],'Amulet':{},'Gear':{},}, #1500和1600一样，10=7+3
        #9:{'Player level':1600,'Aura value':290,'Size':3,
            #'Card':{},'Wish':[],'Amulet':{},'Gear':{},},
    },
}

def iteration_save():
    '''
    为了迭代参数随时可修改，将iteration信息保存至json
    '''
    with open('iteration.json',mode='w+',encoding='UTF-8') as f:
        json.dump(option['Iteration'],f,separators=(',',':'),indent=4)

def iteration_load():
    '''
    读取可能被修改的iteration信息，内容更新到option中
    '''
    #如果iteration.json不存在，先执行一次save
    try:
        open('iteration.json')
    except:
        iteration_save()
    
    with open('iteration.json',mode='r',encoding='UTF-8') as f:
        option['Iteration']=json.load(f)

sum_size=0
for group in option['Group']:
    sum_size+=option['Group'][group]['Size']

iteration_save()
