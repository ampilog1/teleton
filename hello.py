from telethon import TelegramClient
import asyncio
from telethon import TelegramClient

# Use your own values from my.telegram.org
api_id = 28965915
api_hash = '91f4882c59cc1dcce04893f9d6367762'

with TelegramClient('anon', api_id, api_hash, device_model="iPhone 12 Pro", system_version="4.16.30-CUSTOM") as client:
    me = client.loop.run_until_complete(client.get_me())
    print(me)
