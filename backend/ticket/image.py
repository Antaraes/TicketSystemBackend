import pytesseract as pss
pss.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image
import json

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

# imageDetect('./../media/orderImages/bay3_gb8pDah.jpg')
# ./../meida/orderImages/bay3_shhytsj.jpg'