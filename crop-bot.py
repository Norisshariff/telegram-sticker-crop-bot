import telebot
from PIL import Image
import io
import os, time
import threading
import uuid
from rembg import remove
from telebot import types

token = 'TOKEN'
bot = telebot.TeleBot(token)
mode = 'crop' 

def remove_bg_and_resize_image(image_path):
    with open(image_path, 'rb') as img_file:
        input_img = img_file.read()
    output_img = remove(input_img)
    with open(image_path, 'wb') as img_file:
        img_file.write(output_img)
    resize_image(image_path)

def resize_image(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        max_size = 512
        if width > height:
            new_height = int(max_size * height / width)
            new_width = max_size
        else:
            new_width = int(max_size * width / height)
            new_height = max_size
        img = img.resize((new_width, new_height), Image.LANCZOS)
        new_img = Image.new("RGBA", (max_size, max_size), (0, 0, 0, 0))
        new_img.paste(img, ((max_size - new_width) // 2, (max_size - new_height) // 2))
        new_img.save(image_path, "PNG")

commands = [
    types.BotCommand('crop', 'remove image background & adjust image size to Telegram sticker format'),
    types.BotCommand('size', 'adjust image size to Telegram sticker format'),
]
bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! \nSend me an image and Ill turn it into a sticker. \nYou can use the /crop command to remove the image background. \nOr /size to adjust the image size to the Telegram sticker format.")

@bot.message_handler(commands=['crop', 'size'])
def set_mode(message):
    global mode
    mode = message.text[1:]

@bot.message_handler(content_types=['photo', 'sticker', 'document'])
def handle_image(message):
    threading.Thread(target=process_image, args=(message,)).start()

def process_image(message):
    try:
        if message.document:
            if message.document.mime_type.startswith('image'):
                file_id = message.document.file_id
            else:
                bot.reply_to(message, 'Submit an image to create a sticker.')
                return
        elif message.photo:
            file_id = message.photo[-1].file_id
        elif message.sticker:
            file_id = message.sticker.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        unique_filename = str(uuid.uuid4()) + '.webp'
        with open(unique_filename, 'wb') as new_file:
            new_file.write(downloaded_file)
        if mode == 'crop':
            remove_bg_and_resize_image(unique_filename)
        elif mode == 'size':
            resize_image(unique_filename)
        with open(unique_filename, 'rb') as img:
            bot.send_document(message.chat.id, document=img)
        os.remove(unique_filename)
    except Exception:
        bot.reply_to(message, 'An error occurred while processing your image, try again')

@bot.message_handler(func=lambda message: True)
def handle_other(message):
    bot.reply_to(message, 'Submit an image to create a sticker.')

while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        print('Connection error, reconnect after 15 seconds...')
        time.sleep(15)
