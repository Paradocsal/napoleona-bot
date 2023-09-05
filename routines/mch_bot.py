import telebot
import re

# from db_routines import initialize_db, add_user, add_timeseries_source_table, delete_timeseries_source_table, \
#     get_saved_databases
from reports_routines import send_report,scrape_text

#initialize_db()


def get_bot_token():
    token_file = open('C://Users/Adminn/Documents/GitHub/talent_hub_hack_tg/tokens/mch_bot_token', 'r')
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
    #add_user(message.chat.id)
    description = "Привет! Этот бот поможет вам работать с фотографиями ценников. ID вашего чата был записан для дальнейшей синхронизации с вашей базой наименований. Вам доступны следующие команды для взаимодействия с ботом:\n\n"
    description += "/get_text_from_image - Получить текстовое представление полезной информации с фотографии ценника.\n"
    description += "/add_database - Загрузить свою базу данных или выбрать тестовую. Это даст вам возможность сравнивать ценники с аналогами.\n\n"
    description += "/show_analogs - Получить информацию об аналогах товара на ценнике в базе наименований.\n"
    
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
        scrape_text(bot, message.chat.id,message.document)
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
        # TO DO Реализовать запись csv в базу данных с id этого пользователя
        bot.reply_to(message, 'Ваша база наименований была успешно сохранена',reply_markup=create_keyboard_with_commands())
    if message.content_type == 'text' and message.text == 'У меня нет базы данных':
        bot.reply_to(message, "Теперь ваши фотографии будут сравниваться с тестовой базой данных. Вы может в любой момент добавить свою, просто вызвав функцию ещё раз.", reply_markup=create_keyboard_with_commands())
    


# noinspection SpellCheckingInspection
@bot.message_handler(commands=['show_analogs'])
def handle_show_analogs(message):
    #database = get_saved_databases(message.chat.id) # TO DO реализовать геттер для базы данных
    #if not database:
    #    bot.reply_to(message, 'У вас нет собственной базы наименований. Поиск аналогов будет происходить в  тестовой.', reply_markup=create_keyboard_with_commands())
    # else:
    #    send_analogs(bot, message.chat.id, database)
    #
    bot.reply_to(message, 'Аналог', reply_markup=create_keyboard_with_commands())         
    


# noinspection SpellCheckingInspection
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, 'Извините, я могу отвечать только на представленные команды.', reply_markup=create_keyboard_with_commands())


bot.polling(none_stop=True)
