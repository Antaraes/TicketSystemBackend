from .kpay import extract_kpay
from .wave import  extract_wave
# import wave,kpay
def imageDetect(image):
    data = extract_kpay(image)
    if not(data) or "Date" and "Transaction Id" not in data:
        data = extract_wave(image)
    if "Date" and "Transaction Id" not in data :
        data = False
    return data

# imageDetect('./images/wave3.jpg')