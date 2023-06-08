import pytesseract as pss
pss.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image
import json
# from I_image2text import wave,kpay
def imageDetect(image):
    img = Image.open(image)
    text = pss.image_to_string(img)
    #print(text)

    want = ['Transaction Time', 'Transaction No.', 'Transaction Type', 'Transfer To', 'Amount', 'Notes']
    data = {}
    for i in want:
        z = text[text.find(i):]
        z = z[:z.find('\n')]
        data.update({i: z.replace(i, '')})

    print(json.dumps(data, indent=4))

# def imageDetect(image):
#     data = kpay.extract_text(image)
#     print(data)

# imageDetect('./../media/orderImages/bay.jpg')
# ./../meida/orderImages/bay3_shhytsj.jpg'