from pyrogram import Client
from decouple import config


api_id = config('API_ID')
api_hash = config('API_HASH')
phone = config('PHONE')
login = config('LOGIN')


bot = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)


bot.start()
bot.send_message(chat_id='me', text='Тестируем отправку сообщения себе')
bot.stop()
