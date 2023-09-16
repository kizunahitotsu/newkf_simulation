import option_visual
import pc_form
import initialize

import json
import os
import time

with open('info.json',mode='r',encoding='UTF-8') as f:
    info=json.load(f)

def iterate():
    '''
    迭代：分为9个步骤
    '''
    if(info['Step']==1):
        #第1步：初始化
        if(initialize.check_wish()):
            initialize.initialize()

            info['Step']+=1
            with open('info.json',mode='w+',encoding='UTF-8') as f:
                json.dump(info,f,separators=(',',':'),indent=4)

    if(info['Step']==2):
        #第2步：重置pc
        pass

def test():
    info={
        'Step':1,
        'Turn':0,
    }

    with open('info.json',mode='w+',encoding='UTF-8') as f:
        json.dump(info,f,separators=(',',':'),indent=4)

#test()
iterate()
