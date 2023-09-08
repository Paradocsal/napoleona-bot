import telebot
import re

from db_routines import initialize_db, add_user, add_products, \
     get_saved_database
from reports_routines import send_analogs,scrape_text,scrape_text_old

initialize_db()


def get_bot_token():
    token_file = open('C://Users/Adminn/Documents/GitHub/talent_hub_hack_tg/napoleona-bot/tokens/mch_bot_token', 'r')
    token = token_file.read()
    token_file.close()
    return token


bot = telebot.TeleBot(get_bot_token())



def create_keyboard_with_command_test_database():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    
    keyboard.add(telebot.types.KeyboardButton('У меня нет базы данных'))

    return keyboard


def create_keyboard_with_commands():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    keyboard.add(telebot.types.KeyboardButton('/get_text_from_image'))
    keyboard.add(telebot.types.KeyboardButton('/add_database'))
    keyboard.add(telebot.types.KeyboardButton('/show_analogs'))

    return keyboard



# noinspection SpellCheckingInspection
@bot.message_handler(commands=['start'])
def handle_start(message):
    add_user(message.chat.id)
    description = "Привет! Этот бот поможет вам работать с фотографиями ценников. ID вашего чата был записан для дальнейшей синхронизации с вашей базой наименований. Вам доступны следующие команды для взаимодействия с ботом:\n\n"
    description += "/get_text_from_image - Получить текстовое представление полезной информации с фотографии ценника.\n"
    description += "/add_database - Загрузить свою базу данных или выбрать тестовую. Это даст вам возможность сравнивать ценники с аналогами.\n"
    description += "/show_analogs - Получить информацию об аналогах товара на ценнике в базе наименований.\n\n"
    
    description += "Мы работаем над увеличением нашего функционала!"
    bot.reply_to(message, description, reply_markup=create_keyboard_with_commands())


# noinspection SpellCheckingInspection
@bot.message_handler(commands=['get_text_from_image'])
def handle_get_text_from_image(message):
    bot.reply_to(message, 'Пожалуйста, загрузите в бот фото вашего ценника.', reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_text_from_image_step)


# noinspection SpellCheckingInspection
def get_text_from_image_step(message):
    if message.content_type == 'photo':
        largest_photo = message.photo[-1]
        file_info = bot.get_file(largest_photo.file_id)
        file_content = bot.download_file(file_info.file_path)
        text = scrape_text(file_content)
        if text:
            bot.reply_to(message,text,reply_markup=create_keyboard_with_commands())
        else:
            bot.reply_to(message, 'На данном изображении текст не был обнаружен, попробуйте сфотографировать ценник более чётко.', reply_markup=create_keyboard_with_commands())
    else:
        bot.reply_to(message, 'Кажется, ваше сообщение не является фотографией. ', reply_markup=create_keyboard_with_commands())
    


# noinspection SpellCheckingInspection
@bot.message_handler(commands=['add_database'])
def handle_add_database(message):
    bot.reply_to(message, 'Пожалуйста, загрузите в бот вашу базу данных в формате csv. Если вы хотите просто протестировать работу бота на тестовой базе, выберете соответствующую команду', reply_markup=create_keyboard_with_command_test_database())
    
    
    bot.register_next_step_handler(message, add_database_step)


# noinspection SpellCheckingInspection
def add_database_step(message):
    if message.content_type == 'document':
        
        file_info = bot.get_file(message.document.file_id)
        file_content = bot.download_file(file_info.file_path)

        add_products(bot, message.chat.id, file_content)
        
        bot.reply_to(message, 'Ваша база наименований была успешно сохранена',reply_markup=create_keyboard_with_commands())
    if message.content_type == 'text' and message.text == 'У меня нет базы данных':

        add_products(bot, message.chat.id, None, default=True)
        bot.reply_to(message, "Теперь ваши фотографии будут сравниваться с тестовой базой данных. Вы может в любой момент добавить свою, просто вызвав функцию ещё раз.", reply_markup=create_keyboard_with_commands())
    


# noinspection SpellCheckingInspection
@bot.message_handler(commands=['show_analogs'])
def handle_show_analogs(message):
    database = get_saved_database(message.chat.id) 
    
    if not database:
        bot.reply_to(message, 'Кажется, вы не задали базу наименований. Воспользуйтесь функцией /add_database.', reply_markup=create_keyboard_with_commands())
    else:
        bot.reply_to(message, 'Пожалуйста, загрузите фото ценника, аналоги которого вы хотите найти.')
        bot.register_next_step_handler(message, show_analogs_step,database)
        


def show_analogs_step(message,database):
    
        
        if message.content_type == 'photo':
            largest_photo = message.photo[-1]
            file_info = bot.get_file(largest_photo.file_id)
            file_content = bot.download_file(file_info.file_path)
            text = scrape_text(file_content)

            if text:
                analogs = send_analogs(database, text)
            else:
                bot.reply_to(message, 'На данном изображении текст не был обнаружен, попробуйте сфотографировать ценник более чётко.', reply_markup=create_keyboard_with_commands())
            print(analogs)
            if analogs!=[]:
                bot.reply_to(message, analogs, reply_markup=create_keyboard_with_commands())
            else:
                bot.reply_to(message, 'Для данной изображения аналоги не были найдены.', reply_markup=create_keyboard_with_commands())
        else:
            bot.reply_to(message, 'Кажется, ваше сообщение не является фотографией. ', reply_markup=create_keyboard_with_commands())
        
        
        
        # products_text = "\n".join(database)
        # bot.send_message(message.chat.id, products_text)
        # # for item in database:
        # #     bot.send_message(message.chat.id, item)
        
        # send_analogs(bot, message.chat.id, database)
        
    


# noinspection SpellCheckingInspection
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, 'Извините, я могу отвечать только на представленные команды.', reply_markup=create_keyboard_with_commands())


bot.polling(none_stop=True)
