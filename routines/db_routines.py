
import pandas as pd
import sqlite3
import io

def initialize_db():
    connection = sqlite3.connect('C://Users/Adminn/Documents/GitHub/talent_hub_hack_tg/napoleona-bot/database.db')
    cursor = connection.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT UNIQUE
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_name TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

    


    connection.commit()
    cursor.close()
    connection.close()


def add_user(chat_id):
    connection = sqlite3.connect('C://Users/Adminn/Documents/GitHub/talent_hub_hack_tg/napoleona-bot/database.db')
    cursor = connection.cursor()

    cursor.execute('INSERT OR IGNORE INTO users (chat_id) VALUES (?)', (chat_id,))

    connection.commit()
    cursor.close()
    connection.close()


def add_products(bot,chat_id, file_content,default=False):
    connection = sqlite3.connect('C://Users/Adminn/Documents/GitHub/talent_hub_hack_tg/napoleona-bot/database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM users WHERE chat_id = ?', (chat_id,))
    user_id = cursor.fetchone()[0]
    if default:
        df=pd.read_csv('C://Users/Adminn/Documents/GitHub/talent_hub_hack_tg/napoleona-bot/itmo_meta.csv')
    else:
        df = pd.read_csv(io.BytesIO(file_content))
    
    names=df['analogue_name']
    bot.send_message(chat_id,names.head().to_string(index=False))
    for name in names:
        cursor.execute('INSERT OR IGNORE INTO products (user_id, product_name) VALUES (?, ?)', (user_id, name))

    connection.commit()
    cursor.close()
    connection.close()


def delete_products(chat_id, products):
    connection = sqlite3.connect('C://Users/Adminn/Documents/GitHub/talent_hub_hack_tg/napoleona-bot/database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM users WHERE chat_id = ?', (chat_id,))
    user_id = cursor.fetchone()[0]

    cursor.execute('DELETE FROM products WHERE user_id = ? AND product_name = ?', (user_id, products))

    connection.commit()
    cursor.close()
    connection.close()





def get_saved_database(chat_id):
    connection = sqlite3.connect('C://Users/Adminn/Documents/GitHub/talent_hub_hack_tg/napoleona-bot/database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM users WHERE chat_id = ?', (chat_id,))
    user_id = cursor.fetchone()[0]

    cursor.execute('SELECT product_name FROM products WHERE user_id = ?', (user_id,))
    products = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return products



def is_table_empty(table_name):
    connection = sqlite3.connect('C://Users/Adminn/Documents/GitHub/ai_gp_hack_tg_bot4/napoleona-bot/database.db')
    cursor = connection.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0] == 0


