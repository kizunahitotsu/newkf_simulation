'''
import json

info={
    'Section':1,
    'Turn':0,
}

with open('info.json',mode='w+',encoding='UTF-8') as f:
    json.dump(info,f,separators=(',',':'),indent=4)
'''
print('a'==True)