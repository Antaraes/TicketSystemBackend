# -*- coding: utf-8 -*-
"""
Created on Wed May 31 13:24:32 2023

@author: User
"""

import json
import re
import pytesseract as pss
from PIL import Image
import json
# pss.pytesseract.tesseract_cmd=r'Tesseract-OCR\tesseract.exe'
pss.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def findd(aa):
    for i in range(len(aa)):
        if re.search('Su[a-z]+ful',aa[i]):       return i
    else:   return -1
    
def extract_wave(image):
    img = Image.open(image)
    m_data=pss.image_to_string(img).split('\n')
    
    want=['Name','Phone','Type','Amount','Date','Transaction Id']
    in_m=['-','-','Type','Amount','Date','Transaction ID']
    regrex=['([A-Z][a-zA-Z]+\s*)+',
            '(9|09)([0-9]{10}|[0-9]{9})',
            '([A-Za-z]+\s*)+',
            '[0-9][0-9]+ [A-Za-z]*',
            '[0-9]+( |.)[A-Z][a-z]+( |.)[0-9]+',
            '[0-9][0-9]+']
    cond=[lambda a,b: re.search(regrex[b],a),
          lambda a,b: re.search(regrex[b],a),
          lambda a,b: 'Wave' in a or 'Type' in a or re.search(regrex[b],a),
          lambda a,b: 'Amount' in a or re.search(regrex[b],a),
          lambda a,b: 'Date' in a or re.search(regrex[b],a),
          lambda a,b: 'Transaction' in a or 'ID' in a or re.search(regrex[b],a)]
    want_id=0
    #print(m_data)
    m_data=m_data[findd(m_data)+1:]
    #print(m_data)
    data={}
    for d in m_data:
        #if want_id==1: print(d,cond[want_id](d,want_id))
        if want_id<len(want) and cond[want_id](d,want_id):
            #print(d,d.replace(in_m[want_id],'').strip(),re.search(regrex[want_id],d.replace(in_m[want_id],'').strip()))
            data.update({want[want_id]:re.search(regrex[want_id],d.replace(in_m[want_id],'').strip())[0]})
            #m_data.remove(d)
            want_id+=1
    # print(data)

    return  data

# test with kpay
# print(extract_text('images/wave1.jpg'))
# extract_text('./../../media/orderImages/bay.jpg')
#test with 10 wave images
# datas=[]
# for i in range(0,10):
#     img=Image.open('images/wave{}.jpg'.format(i))
#     datas.append(extract_text(img))
# print(datas)