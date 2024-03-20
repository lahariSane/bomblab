import asyncio
from pyrogram import Client,filters
from pyrogram.handlers import MessageHandler
from config import api_hash, api_id,bot_token
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton,CallbackQuery
import zipfile
import re
from bomblab import extract_bomb
# import logging
# logging.basicConfig(
#     level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#     format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log message format
#     datefmt='%Y-%m-%d %H:%M:%S'  # Define the date-time format
# )
# logger = logging.getLogger(__name__)
app = Client("my_account", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

START_MESSAGE ='\nI am a bomblab bot. I will help you solving your labs.'
START_BUTTONS = [
        [
            InlineKeyboardButton('Help',callback_data="help"),
            InlineKeyboardButton('Close',callback_data='close')
            ]
        ]

@app.on_message(filters.command('start'))
async def start(client, message):
    # await app.send_message(message.chat.id,text="hello")
    await message.reply_text(
            f'Hello {message.chat.first_name}' + START_MESSAGE,
            reply_markup = InlineKeyboardMarkup(START_BUTTONS), 
            quote = True
            )

@app.on_callback_query()
def callbackQuery(client, CallbackQuery):
    if CallbackQuery.data == 'help':
        HELP_MESSAGE = '__Enter instructions__'
        HELP_BUTTONS = [
            [
                InlineKeyboardButton('Back to Menu', callback_data='backToMenu')
            ]
        ]
        CallbackQuery.edit_message_text(
            HELP_MESSAGE,
            reply_markup = InlineKeyboardMarkup(HELP_BUTTONS)
        )
    elif CallbackQuery.data == 'backToMenu':
        CallbackQuery.edit_message_text(
            START_MESSAGE,
            reply_markup = InlineKeyboardMarkup(START_BUTTONS)
        )
    elif CallbackQuery.data == 'close':
        app.delete_messages(CallbackQuery.message.chat.id,[CallbackQuery.message.id,CallbackQuery.message.reply_to_message.id])
        
    
@app.on_message(filters.command('upload'))
async def upload(client, message):
    await message.reply_text(
        f'{message.chat.first_name},Please upload the zip file of the bomblab.',
            reply_markup = InlineKeyboardMarkup(START_BUTTONS), 
            quote = True
    )
    
async def zip_filter(_, __, message):
    if message.document:
        file_name = message.document.file_name
        return file_name.endswith('.zip')
    return False

@app.on_message(filters.create(zip_filter))
async def download_zip(client, message):
    async def progress(current, total):
        print(f"{current * 100 / total:.1f}%")
    zip_file_path = await message.download(file_name=message.document.file_name,progress=progress)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        pattern = re.compile(r'^.*bomb$')
        for file_name in file_list:
            if pattern.match(file_name):
                file_location = zip_ref.extract(file_name)
                await client.send_message(message.chat.id, "Bomb file extracted!")
                extract_bomb(file_location)
                app.send_document(message.chat_id,'answers.txt')
                break
            else:
                await client.send_message(message.chat.id, "No bomb file found in the zip.")

    
async def main():
    print("start")
    # app.log_level = logging.DEBUG
    print('connection bulit')
    async with app:
        print('started')
        await app.send_message(1767934002, "Hi!")
        print("done")
        
# app.add_handler(MessageHandler(start))

app.run()