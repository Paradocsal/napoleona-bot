from io import BytesIO
import pandas as pd





def scrape_text(image):#Скрапинг текста с фото, возможно не всего, а как-то отфильтрованный, пока просто отсылает фотку обратно
    image_stream = BytesIO(image)
    #bot.send_photo(chat_id,photo=image_stream)
    
    return ('Текст для данной картинки:')
    

def send_analogs(database,text):
    return('Аналоги')







class Reporter:
    def __init__(self):
       ...






    def generate_report_text(self):  
        


        return 0
    
def send_report(bot, chat_id, validation=False):
    reporter = Reporter()
    
    
    bot.send_message(chat_id, reporter.generate_report_text())




        

    
