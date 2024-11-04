import sqlite3
from decouple import config
from pyrogram import Client


# Создание базы данных и таблицы
def create_database():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            message_id INTEGER,
            sender_id INTEGER,
            date TEXT,
            text TEXT,
            media_type TEXT,
            media_url TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Сохранение сообщения в базу данных
def save_message(chat_id, message_id, sender_id, date, text, media_type, media_url):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (chat_id, message_id, sender_id, date, text, media_type, media_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (chat_id, message_id, sender_id, date, text, media_type, media_url))
    conn.commit()
    conn.close()


# Получение истории сообщений
def save_chat_history(client, chat_username):
    for message in client.get_chat_history(chat_username):
        chat_id = message.chat.id
        message_id = message.id  # Используем message.id вместо message.message_id
        sender_id = message.from_user.id if message.from_user else None
        date = message.date.isoformat()  # Преобразуем дату в строку
        text = message.text or ''  # Текст сообщения, если он есть

        media_type = None
        media_url = None

        # Проверка на наличие медиа
        if message.photo:
            media_type = 'photo'
            media_url = message.photo.file_id
        elif message.video:
            media_type = 'video'
            media_url = message.video.file_id
        elif message.document:
            media_type = 'document'
            media_url = message.document.file_id
        elif message.audio:
            media_type = 'audio'
            media_url = message.audio.file_id

        # Сохранение сообщения в базу данных
        save_message(chat_id, message_id, sender_id, date, text, media_type, media_url)


# Чтение конфигурации
api_id = config('API_ID')  # ID приложения
api_hash = config('API_HASH')  # Хэш приложения
phone = config('PHONE')  # Номер телефона
login = config('LOGIN')  # Логин (username)

# Создание клиента
app = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)

if __name__ == "__main__":
    create_database()  # Создание базы данных и таблицы
    with app:
        save_chat_history(app, "@ampilog")  # запускаем
