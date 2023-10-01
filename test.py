import option_visual
import pc_form

import json

lib=option_visual.lib
sum_size=option_visual.sum_size

with open('data 23-09-21\pc_turn0.json',mode='r',encoding='UTF-8') as f:
    pc_list=json.load(f)
'''
role_stats={}
for role in lib['Role']:
    role_stats[role]=0

gear_stats={}
for gear in lib['Gear']:
    gear_stats[gear]=0
    if(lib['Gear'][gear]['Myst']):
        gear_stats['M_'+gear]=0

aura_stats={}
for aura in lib['Aura']:
    aura_stats[aura]=0

for i in range(1,600+1):
    with open(f"data 23-09-21\pc_turn{i}.json",mode='r',encoding='UTF-8') as f:
        pc_new=json.load(f)
    
    for j in range(sum_size):
        if(pc_list[j]['Data']['Name']==pc_new['Data']['Name']):
            pc_list[j]=pc_new
            break
    
    if(i<=300):
        continue
    
    for j in range(sum_size):
        r=pc_list[j]['Data']['Role']
        role_stats[r]+=1

        g1=pc_list[j]['Data']['Weapon']
        if(g1['Myst']):
            gear_stats['M_'+g1['Type']]+=1
        else:
            gear_stats[g1['Type']]+=1
        
        g2=pc_list[j]['Data']['Hand']
        if(g2['Myst']):
            gear_stats['M_'+g2['Type']]+=1
        else:
            gear_stats[g2['Type']]+=1
        
        g3=pc_list[j]['Data']['Body']
        if(g3['Myst']):
            gear_stats['M_'+g3['Type']]+=1
        else:
            gear_stats[g3['Type']]+=1
        
        g4=pc_list[j]['Data']['Head']
        if(g4['Myst']):
            gear_stats['M_'+g4['Type']]+=1
        else:
            gear_stats[g4['Type']]+=1
        
        a_list=pc_list[j]['Data']['Aura']['Skill']
        for a in a_list:
            aura_stats[a]+=1

print(role_stats,gear_stats,aura_stats,sep='\n')
'''
with open('pcs.txt',mode='w+',encoding='UTF-8') as f:
    for pc in pc_list:
        f.write(pc_form.data_dict_to_str(pc['Data']))
        f.write(f"\n// turn {pc['Parameter']['Turn']}\n\n")

for i in range(1,600+1):
    with open(f"data 23-09-21\pc_turn{i}.json",mode='r',encoding='UTF-8') as f:
        pc_new=json.load(f)
    
    with open('pcs.txt',mode='a+',encoding='UTF-8') as f:
        f.write(pc_form.data_dict_to_str(pc_new['Data']))
        f.write(f"\n// turn {pc_new['Parameter']['Turn']}\n\n")

input()
