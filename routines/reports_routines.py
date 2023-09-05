from io import BytesIO
import pandas as pd





def scrape_text(bot,chat_id,image):#Скрапинг текста с фото, возможно не всего, а как-то отфильтрованный, пока просто отсылает фотку обратно

    bot.send_message(chat_id, 'Текст для данной картинки:')
    bot.send_photo(chat_id,image)

def send_analogs(bot,chat_id,database):
    bot.send_message(chat_id, 'Аналоги')






class Reporter:
    def __init__(self):
       ...






    def generate_report_text(self):  
        


        return 0
    
def send_report(bot, chat_id, validation=False):
    reporter = Reporter()
    
    
    bot.send_message(chat_id, reporter.generate_report_text())




        

    
