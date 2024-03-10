# ระบบจริง โดยนำรูปภาพจากเว็บมาใส่เข้าไป
# โค้ดนี้จำเป็นต้องเชื่อมต่ออินเทอร์เน็ตเพื่อดาวน์โหลดภาพจากเว็บไซต์ 

# ตัวนี้จะไม่ครอปรูปนะครับ

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

# ฟังก์ชันสำหรับตรวจจับฝนจากภาพ
def detect_rain(image_path, line_notify_token1, line_notify_token2):

    # อ่านภาพจากไฟล์
    img = cv2.imread(image_path)

    # ตรวจสอบว่าสามารถอ่านภาพได้หรือไม่
    if img is None:
        print("ไม่สามารถอ่านภาพไฟล์ได้")
        return

    # ครอปรูปก่อนจะทำการตรวจจับฝน
    cropped_img = img[:, 90:]

    # ตรวจจับฝนในระบบ HSV
    hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
    lower_red_hsv = np.array([0, 100, 100])  #  สีแดงเหลืองในรูปแบบ HSV
    upper_red_hsv = np.array([30, 255, 255])  # ปรับสเกลของสีในช่วงนี้ในช่องแรก ถ้ามากขึ้นยิ่งรับมีช่วงสีได้มากขึ้น แต่ตอนนี้ผมปรับให้พอดีอยู่แล้วครับ
    mask_red_hsv = cv2.inRange(hsv, lower_red_hsv, upper_red_hsv)

    # หา contour ของฝน
    contours_red, _ = cv2.findContours(mask_red_hsv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # คำนวณพื้นที่ของฝนสีแดง
    red_area = sum(cv2.contourArea(cnt) for cnt in contours_red)

    # แสดงข้อความพื้นที่ของฝนสีแดง
    print("พื้นที่ของฝนสีแดง:", red_area, "Pixel")

    # ถ้าพบฝนสีแดงให้ส่งข้อความไปที่ Line Notify
    if red_area > 20:
        message = f"พบฝนสีแดง-เหลือง ในระดับ 41.5 - 46.5 dBz!\nพื้นที่ของฝนสีแดง: {red_area} Pixel"
        #cropped_image = cv2.imencode('.jpg', cropped_img)[1].tostring()
        _, encoded_image = cv2.imencode('.jpg', cropped_img)
        cropped_image = encoded_image.tobytes()
        send_line_notify_with_cropped_image(message, line_notify_token1, cropped_image)  # ส่งภาพที่ถูกครอบ
        send_line_notify_with_cropped_image(message, line_notify_token2, cropped_image)  # ส่งภาพที่ถูกครอบ
        cv2.imwrite('rain_detected_red.jpg', cropped_img)  # บันทึกภาพที่ตรวจพบฝนสีแดงเพื่อใช้แสดงผล
    else:
        # บันทึกรูปที่ถูกครอบทุกครั้ง
        cv2.imwrite('cropped_image.jpg', cropped_img)

# ฟังก์ชันสำหรับดาวน์โหลดภาพและตรวจสอบฝนทุก 15 นาที
def download_and_detect():
    while True:
        # รอรับคำสั่งจากผู้ใช้เพื่อเริ่มต้นดาวน์โหลดและตรวจสอบ
        input("กด Enter เพื่อเริ่มต้นดาวน์โหลดและตรวจสอบฝนทุก 15 นาที:")
        
        # เริ่มต้นดาวน์โหลดภาพและตรวจสอบฝนทุก 15 นาที
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            if current_time.endswith(":05") or current_time.endswith(":20") or current_time.endswith(":35") or current_time.endswith(":50"):
                url = 'https://weather.tmd.go.th/kkn.php'
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                image_url = soup.find('img', id='radimg')['src']
                full_image_url = 'https://weather.tmd.go.th' + image_url.strip('.')
                response = requests.get(full_image_url)
                with open('rain_image.gif', 'wb') as f:
                    f.write(response.content)
                img_gif = Image.open("rain_image.gif")
                img_gif.convert("RGB").save("rain_image.jpg")
                image_path = 'rain_image.jpg'
                line_notify_token1 = "6KQyAe225DiMNmmKNaMH6LiwBAlPtSvfTnEwXBw4muY"
                line_notify_token2 = "sPYkN3rIRR2GxAMYGnWcQsVPVgxaC17qDLXQgk3tNdQ"
                detect_rain(image_path, line_notify_token1, line_notify_token2)
                time.sleep(900)  # รอ 15 นาที
            else:
                time.sleep(1)  # รอ 1 วินาที เพื่อป้องกันการใช้งาน CPU เกินไป

# เรียกใช้งานฟังก์ชัน download_and_detect
if __name__ == "__main__":
    download_and_detect()

