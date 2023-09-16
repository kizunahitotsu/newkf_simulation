import option_visual
import pc_form

import json
import copy
import random

lib=option_visual.lib
option=option_visual.option

with open('info.json',mode='r',encoding='UTF-8') as f:
    info=json.load(f)

#info={'Step':2,'Turn':1-100}


