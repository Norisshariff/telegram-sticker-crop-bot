# Telegram sticker crop bot
https://t.me/stickercropbot 

A bot that remove the image background and changes the resolution of an image for adding to a sticker pack.

## Install
python3-full and python3-pip required:
```bash
sudo apt update && sudo apt install git screen python3-full python3-pip -y
```

Clone repo and install dependencies:
```bash
git clone https://github.com/imhassla/telegram-sticker-crop-bot
cd telegram-sticker-crop-bot
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Usage

Create a file called .env  and add your TOKEN variable to this file:
```bash
echo 'TOKEN=bot_token' > .env
```
run:
```bash
screen python3 crop-bot.py
```
## License
This script is distributed under the MIT license. 
