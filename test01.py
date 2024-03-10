# ระบบจริง โดยนำรูปภาพจากเว็บมาใส่เข้าไป

from bs4 import BeautifulSoup
import requests
import cv2
import numpy as np
from PIL import Image
import time
from datetime import datetime, timedelta

# ฟังก์ชันสำหรับส่งข้อความและรูปภาพที่ถูกครอบไปที่ Line Notify
def send_line_notify_with_cropped_image(message, token, cropped_image):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message': message}
    files = {'imageFile': cropped_image}
    requests.post(url, headers=headers, data=data, files=files)

# ฟังก์ชันสำหรับตรวจจับฝนจากภาพ detect_rai  # กำลังพัฒนา 
# กำลังพัฒนา 











# ฟังก์ชันสำหรับดาวน์โหลดภาพและตรวจสอบฝนทุก 15 นาที กำลังพัฒนา
def download_and_detect():
    while True:
        # รอรับคำสั่งจากผู้ใช้เพื่อเริ่มต้นดาวน์โหลดและตรวจสอบ กำลังพัฒนา
        input("กด Enter เพื่อเริ่มต้นดาวน์โหลดและตรวจสอบฝนทุก 15 นาที:")
        
        # เริ่มต้นดาวน์โหลดภาพและตรวจสอบฝนทุก 15 นาที กำลังพัฒนา
        while True:
                url = 'https://weather.tmd.go.th/kkn.php'
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                image_url = soup.find('img', id='radimg')['src']
                full_image_url = 'https://weather.tmd.go.th' + image_url.strip('.')
                response = requests.get(full_image_url)
                with open('rain_image.gif', 'wb') as f:
                    f.write(response.content)
                img_gif = Image.open("rain_image.gif") # แปลงรูปภาพให้กลายเป็น JPG เพื่อทำ Imagr processing ได้ดีขึ้น
                img_gif.convert("RGB").save("rain_image.jpg")
                image_path = 'rain_image.jpg'
                line_notify_token1 = "Token ของเจ้าของหรือไลน์กลุ่มที่ต้องการส่งข้อความเข้าไป"
                line_notify_token2 = "Token ของเจ้าของหรือไลน์กลุ่มที่ต้องการส่งข้อความเข้าไป"
                detect_rain(image_path, line_notify_token1, line_notify_token2)
                time.sleep(900)  # รอ 15 นาที
            # else: 
                time.sleep(1)  # รอ 1 วินาที เพื่อป้องกันการใช้งาน CPU เกินไป

# เรียกใช้งานฟังก์ชัน download_and_detect
if __name__ == "__main__":
    download_and_detect()
