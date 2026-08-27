import os
import time
from threading import Thread
import requests
from flask import Flask
import telebot
from telebot import types

TOKEN = '7685203704:AAHJvrtKNMMC3fMHImGdq6Xj2mdb5__912U'
bot = telebot.TeleBot(TOKEN)
CHANNEL_ID = '@titokvideodowloader'
CHANNEL_LINK = 'https://t.me/titokvideodowloader'

app = Flask('')


@app.route('/')
def home():
  return 'Bot is running!'


def run():
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


def check_sub(user_id):
  try:
    status = bot.get_chat_member(CHANNEL_ID, user_id).status
    return status in ['member', 'administrator', 'creator']
  except Exception as e:
    return False


@bot.message_handler(commands=['start'])
def start(message):
  start_text = (
      '👋 မင်္ဂလာပါ! TikTok Video Downloader Bot မှ ကြိုဆိုပါတယ်။\n\n'
      '📖 Channel Join ပြီးမှ သုံးလို့ရပါမယ်။'
  )
  if check_sub(message.from_user.id):
    bot.reply_to(message, '✅ Link ပို့နိုင်ပါပြီ။')
  else:
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('📢 Join Channel', url=CHANNEL_LINK)
    )
    bot.send_message(message.chat.id, start_text, reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_tiktok(message):
  if not check_sub(message.from_user.id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('📢 Join Channel', url=CHANNEL_LINK)
    )
    bot.send_message(
        message.chat.id, '⚠️ Channel အရင် Join ပေးပါ။', reply_markup=markup
    )
    return

  url = message.text.strip()
  if 'tiktok.com' in url or 'douyin.com' in url:
    sent = bot.reply_to(message, '⏳ ဗီဒီယိုကို ဆွဲထုတ်နေပါတယ် ခဏစောင့်ပါ...')
    try:
      api_url = f'https://www.tikwm.com/api/?url={url}&hd=1'
      headers = {'User-Agent': 'Mozilla/5.0'}
      res = requests.get(api_url, headers=headers).json()

      if res.get('code') == 0 and 'data' in res:
        video_url = res['data'].get('hd_play') or res['data'].get('play')
        if video_url:
          bot.send_video(
              message.chat.id,
              video_url,
              caption='✅ Done!\n@titokvideodowloader',
          )
          bot.delete_message(message.chat.id, sent.message_id)
        else:
          bot.edit_message_text(
              '❌ ဗီဒီယိုလင့်ခ် ရယူ၍ မရပါ။', message.chat.id, sent.message_id
          )
      else:
        bot.edit_message_text(
            '❌ ဗီဒီယို ရှာမတွေ့ပါ။', message.chat.id, sent.message_id
        )
    except Exception as e:
      bot.edit_message_text('❌ Error ဖြစ်သွားပါသည်။', message.chat.id, sent.message_id)
  else:
    bot.reply_to(message, '💡 ကျေးဇူးပြု၍ TikTok Link ပို့ပေးပါ။')


if __name__ == '__main__':
  t = Thread(target=run)
  t.start()

print('Bot စတင်အလုပ်လုပ်နေပါပြီ...')
bot.infinity_polling(skip_pending=True)

