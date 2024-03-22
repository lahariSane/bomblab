import asyncio
from pyrogram import Client,filters
from config import api_hash, api_id,bot_token,connection_string
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import zipfile
import re
from bomblab import extract_bomb
from database import user_database
# import logging
# logging.basicConfig(
#     level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#     format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log message format
#     datefmt='%Y-%m-%d %H:%M:%S'  # Define the date-time format
# )
# logger = logging.getLogger(__name__)
app = Client("my_account", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
connection = connection_string
database_name = 'telidu'
collection = 'users'
db = user_database(connection,database_name,collection)

START_MESSAGE ='\nI am a bomblab bot. I will help you solving your labs.'
START_BUTTONS = [
        [
            InlineKeyboardButton('Help',callback_data="help"),
            InlineKeyboardButton('Close',callback_data='close')
            ]
        ]
PRO_BUTTONS = [
        [
            InlineKeyboardButton('Upload Payment Screenshot',callback_data="uploadFile")
            ],
        [
            InlineKeyboardButton('Go Back',callback_data='backToPlan')
            ]
        ]



@app.on_message(filters.command('start'))
async def start(client, message):
    await message.reply_text(
            f'Hello {message.chat.first_name}' + START_MESSAGE,
            reply_markup = InlineKeyboardMarkup(START_BUTTONS), 
            quote = True
            )
    user = await db.find_user(message.from_user.id)
    if(not user):
        await db.new_user(message.from_user.id,0)

@app.on_callback_query()
async def callbackQuery(client, CallbackQuery):
    if CallbackQuery.data == 'help':
        HELP_MESSAGE = '**You need help??**\n\n✵/upload Upload bomblab zip\n   Allows only zip files containing file \nnamed bomb without any extension\n\n ✵/plan Check plans'
        HELP_BUTTONS = [
            [
                InlineKeyboardButton('Back to Menu', callback_data='backToMenu')
            ]
        ]
        await CallbackQuery.edit_message_text(
            HELP_MESSAGE,
            reply_markup = InlineKeyboardMarkup(HELP_BUTTONS)
        )
    elif CallbackQuery.data == 'backToMenu':
        await CallbackQuery.edit_message_text(
            START_MESSAGE,
            reply_markup = InlineKeyboardMarkup(START_BUTTONS)
        )
    elif CallbackQuery.data == 'close':
        await app.delete_messages(CallbackQuery.message.chat.id,[CallbackQuery.message.id,CallbackQuery.message.reply_to_message.id])
    elif CallbackQuery.data == 'Pro':
        await CallbackQuery.edit_message_text(
            'Pay **₹89/-** and get **4** bomblabs solved\n\n__payment upi__\n\nPay to the above upi link and please upload the screenshot to get remaining bomblabs to be solved increased by 4.',
            reply_markup = InlineKeyboardMarkup(PRO_BUTTONS) 
        )
    elif CallbackQuery.data == 'Platinum':
        await CallbackQuery.edit_message_text(
            'Pay **₹69/-** and get **3** bomblabs solved\n\n__payment upi__\n\nPay to the above upi link and please upload the screenshot to get remaining bomblabs to be solved increased by 3.',
            reply_markup = InlineKeyboardMarkup(PRO_BUTTONS) 
        )
    elif CallbackQuery.data == 'Gold':
        await CallbackQuery.edit_message_text(
            'Pay **₹49/-** and get **2** bomblabs solved\n\n__payment upi__\n\nPay to the above upi link and please upload the screenshot to get remaining bomblabs to be solved increased by 2.',
            reply_markup = InlineKeyboardMarkup(PRO_BUTTONS) 
        )
    elif CallbackQuery.data == 'Sliver':
        await CallbackQuery.edit_message_text(
            'Pay **₹25/-** and get **1** bomblabs solved\n\n__payment upi__\n\nPay to the above upi link and please upload the screenshot to get remaining bomblabs to be solved increased by 1.',
            reply_markup = InlineKeyboardMarkup(PRO_BUTTONS) 
        )
    elif CallbackQuery.data == 'backToPlan':
        user = await db.find_user(CallbackQuery.from_user.id)
        await CallbackQuery.edit_message_text(
            f"**User ID:**{CallbackQuery.message.chat.id}\n**Username:**{CallbackQuery.message.chat.first_name}\n\nBomblabs that are remained which can be solved by the bot as per your plan are **{user['remaining']}**",
            reply_markup = InlineKeyboardMarkup(PLAN_BUTTONS)
        )
    elif CallbackQuery.data == 'uploadFile':
        await CallbackQuery.message.reply_text("Please upload the file.")
    elif CallbackQuery.data.split(' ')[0] == 'no':
        await app.send_message(CallbackQuery.data.split(' ')[1],'Some issue with transaction.')
    elif CallbackQuery.data == 'updated':
        await CallbackQuery.answer('Already updated',True)
    else:
        await db.update_plan(CallbackQuery.data.split(' ')[1],int(CallbackQuery.data.split(' ')[0]))
        await app.send_message(CallbackQuery.data.split(' ')[1],'Updated')
        await app.edit_message_reply_markup(
            CallbackQuery.message.chat.id, CallbackQuery.message.id,
            InlineKeyboardMarkup([[InlineKeyboardButton("Updated", callback_data="updated")]]
        ))
    
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
        user = await db.find_user(message.from_user.id)
        for file_name in file_list:
            if pattern.match(file_name and user['remaining'] > 0):
                file_location = zip_ref.extract(file_name)
                await client.send_message(message.chat.id, "Bomb file extracted!")
                extract_bomb(file_location)
                app.send_document(message.chat_id,'answers.txt')
                await db.update_plan(user['userID'],-1)
                break
            else:
                await client.send_message(message.chat.id, "No bomb file found in the zip.")
                

PLAN_BUTTONS = [
        [
            InlineKeyboardButton('Pro',callback_data='Pro'),
            InlineKeyboardButton('Platinum',callback_data='Platinum')
            ],
        [
            InlineKeyboardButton('Gold',callback_data='Gold'),
            InlineKeyboardButton('Sliver',callback_data="Sliver")
        ]
        ]

@app.on_message(filters.command('plan'))
async def plan(client, message):
    user = await db.find_user(message.from_user.id)
    await message.reply_text(
            f"**User ID:**{message.chat.id}\n**Username:**{message.chat.first_name}\n\nBomblabs that are remained which can be solved by the bot as per your plan are **{user['remaining']}**",
            reply_markup = InlineKeyboardMarkup(PLAN_BUTTONS), 
            quote = True
            )

@app.on_message(filters.photo)
async def forwardPhoto(client,message):
    user_id = message.from_user.id
    PHOTO_BUTTONS = [
        [InlineKeyboardButton('89',callback_data=f'4 {user_id}'),InlineKeyboardButton('69',callback_data=f'3 {user_id}')],
        [InlineKeyboardButton('49',callback_data=f'2 {user_id}'),InlineKeyboardButton('25',callback_data=f'1 {user_id}')],
        [InlineKeyboardButton('NO', callback_data=f"no {user_id}")]
    ]
    await app.copy_message(-1002107584717,message.from_user.id,message.id,
                           reply_markup=InlineKeyboardMarkup(PHOTO_BUTTONS))
    await message.reply_text('Forwarded to admin. Waiting for response.',quote=True)
    
# app.log_level = logging.DEBUG
        
# app.add_handler(MessageHandler(start))

app.run()


# payment id
# bomblab optimized code