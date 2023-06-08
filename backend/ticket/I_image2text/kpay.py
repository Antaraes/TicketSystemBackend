

import json
import re
import pytesseract as pss
from PIL import Image
import json
#print(re.search('\W[0-9]([0-9]|\W)*[0-9]+ [A-Za-z]*',' Amount -50,500.00 Ks'))
# pss.pytesseract.tesseract_cmd=r"Tesseract-OCR\tesseract.exe"
pss.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def findd(aa):
    for i in range(len(aa)):
        if re.search('Su[a-z]+ful',aa[i]):       return i
    else:   return -1
    
def extract_kpay(image):
    img = Image.open(image)
    m_data=pss.image_to_string(img).split('\n')
    
    want=['Date','Transaction Id','Type','Name','Amount']
    in_m=['Transaction Time','Transaction ID','Transaction Type','Transfer To','Amount']
    regrex=['[0-9]{2}\D[0-9]{2}\D[0-9]{4}\D[0-9]{2}\D[0-9]{2}\D[0-9]{2}',
            '[0-9]{10}[0-9]+',
            '([A-Za-z]+\s*)+',
            '([A-Z][a-zA-Z]+\s*)+',
            '\W[0-9]([0-9]|\W)*[0-9]+ [A-Za-z]*',]
    cond=[lambda a,b: 'Transaction' in a or 'Time' in a or re.search(regrex[b],a),
          lambda a,b: 'Transaction' in a or 'No' in a or re.search(regrex[b],a),
          lambda a,b: 'Type' in a or re.search(regrex[b],a),
          lambda a,b: 'Transfer' in a or re.search(regrex[b],a),
          lambda a,b: 'Amount' in a or re.search(regrex[b],a),]
    want_id=0
    #print(m_data)
    m_data=m_data[findd(m_data)+1:]
    #print(m_data)
    data={}
    for d in m_data:
        #if want_id==1: print(d,cond[want_id](d,want_id))
        if want_id<len(want) and cond[want_id](d,want_id):
            #print(d,d.replace(in_m[want_id],'').strip(),re.search(regrex[want_id],d.replace(in_m[want_id],'').strip()))
            ss=re.search(regrex[want_id],d.replace(in_m[want_id],'').strip())
            if ss:   data.update({want[want_id]:ss[0]})
            if want_id==3:    
                pp=re.search('\W+[0-9]+\W*', d)
                if pp: data.update({'Phone':pp[0].strip()})
            #m_data.remove(d)
            want_id+=1
            
    return data
    # print(data)
#test with wave
# print(extract_text(Image.open('images/wave4.jpg')))
# datas=[]

#test with 10 kpay images
# extract_text('./../../media/orderImages/bay.jpg')
# img=Image.open('images/bay0.jpg')
