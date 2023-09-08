from io import BytesIO
import pandas as pd
import requests
import json
import cv2
from PIL import Image
from textblob import TextBlob
import easyocr
import numpy as np
import os
import time
import re
import torch
from torchvision import transforms as T

def send_analogs(database,text):
    
    headers = {
        'accept': 'text/plain',
        'Content-Type': 'application/json',
    }
    for i in range(len(database)):
        database[i] = database[i].lower()
    
    text = text.lower()
    print(text)
    encoded_text = requests.utils.quote(text.encode('utf-8'), safe='')
    url = f"http://localhost:5035/TfIdfSearch?query={encoded_text}"
    
    response = requests.post(url, headers=headers,  json=database)
    
    response_data = response.text
    # if response.status_code == 200:
    #     response_data = response.text
    #     # Process the response data as needed
    # else:
    #     return(f"Request failed with status code {response.status_code}")
    return response_data


def scrape_text(image):
    image_stream = BytesIO(image)
    
    
    timestamp = int(time.time())
    unique_filename = f"{timestamp}.jpg"
    image_save = cv2.imdecode(np.frombuffer(image_stream.read(), np.uint8), cv2.IMREAD_COLOR)
    print(unique_filename)
    output_image_path = os.path.join('C://Users/Adminn/Documents/GitHub/talent_hub_hack_tg/napoleona-bot/images', unique_filename)

    model = torch.hub.load('C://Users/Adminn/Documents/GitHub/talent_hub_hack_tg/yolov5', 'custom', path='C://Users/Adminn/Documents/GitHub/talent_hub_hack_tg/napoleona-bot/best.pt', force_reload=True, source = 'local') 
    model.eval()
    model.conf = 0.2
    cv2.imwrite(output_image_path, image_save)
    print(output_image_path)
    image = Image.open(output_image_path)

    with torch.no_grad():
        results = model(image)
    predictions = results.pred[0]
    boxes = predictions[:, :4]
    scores = predictions[:, 4]
    conf_threshold = 0.3
    filtered_boxes = boxes[scores >= conf_threshold]
    filtered_scores = scores[scores >= conf_threshold]
    margin = 100

    
    cropped_images = []
    for box in filtered_boxes.tolist():
        x1, y1, x2, y2 = box
        x1 -= margin
        y1 -= margin
        x2 += margin
        y2 += margin

        cropped_image = image.crop((x1, y1, x2, y2))
        cropped_images.append(cropped_image)
    
    detected_texts=[]
    for idx, cropped_image in enumerate(cropped_images):
        cropped_image.save(f'{output_image_path}_{idx}.jpg')  # Сохраните обрезанные изображения
        text = text_recog(f'{output_image_path}_{idx}.jpg') 
        
        if text:
            detected_texts.append(' '.join(text))
    
    return ' '.join(detected_texts)


def scrape_text_old(image):#Скрапинг текста с фото, возможно не всего, а как-то отфильтрованный, пока просто отсылает фотку обратно
    image_stream = BytesIO(image)
    
    timestamp = int(time.time())
    unique_filename = f"{timestamp}.jpg"
    
    image = cv2.imdecode(np.frombuffer(image_stream.read(), np.uint8), cv2.IMREAD_COLOR)
    output_image_path = os.path.join('C://Users/Adminn/Documents/GitHub/talent_hub_hack_tg/napoleona-bot/images', unique_filename)
    
    # Эквализация гистограммы с использованием CLAHE
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized = clahe.apply(gray)

    # Улучшение резкости изображения
    sharpened = cv2.filter2D(equalized, -1, kernel=np.array([[-1, -1, -1],
                                                            [-1, 9, -1],
                                                            [-1, -1, -1]]))

    # Фильтр Лапласа для выделения границ
    laplacian = cv2.Laplacian(sharpened, cv2.CV_64F)

    # Оценка смазанности на основе градиента
    laplacian_var = laplacian.var()

    # Порог для определения смазанных изображений
    threshold_var = 300
    cv2.imwrite(output_image_path, sharpened)

    if laplacian_var >= threshold_var:
        # Если градиент изображения выше порога, то изображение не считается смазанным
        # и его можно сохранить
        
        # Распознавание текста на изображении
        text = text_recog(output_image_path)

        # Предобработка текста
        preprocessed_text = preprocess_text(text)

        # Вывод результата
        #corrected_text=corrected_text.lower()
        return preprocessed_text
    else:
        return ('Изображение слишком смазанное для обработки. Пожалуйста, отправьте более чёткое изображение.')



# Функция для распознавания текста на изображении
def text_recog(path):
    reader = easyocr.Reader(['ru', 'en'])
    result = reader.readtext(path, detail=0)
    return result

def preprocess_text(text):
    # Объединить строки в одну
    combined_text = ' '.join(text)

    # Преобразовать текст в нижний регистр
    lower_text = combined_text.lower()

    # Удалить все символы, кроме букв и цифр
    cleaned_text = re.sub(r'[^a-zA-Z0-9а-яА-Я ]', '', lower_text)

    # Удалить лишние пробелы и пробелы в начале и конце строки
    final_text = ' '.join(cleaned_text.split())

    return final_text

# Функция для исправления опечаток в тексте
def correct_spelling(text):
    blob = TextBlob(text)
    return str(blob.correct())



    

# def send_analogs(database,text):
#     return('Аналоги')







class Reporter:
    def __init__(self):
       ...






    def generate_report_text(self):  
        


        return 0
    
def send_report(bot, chat_id, validation=False):
    reporter = Reporter()
    
    
    bot.send_message(chat_id, reporter.generate_report_text())




        

    
