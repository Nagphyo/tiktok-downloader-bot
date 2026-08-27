import os
import time
from threading import Thread
import requests
from flask import Flask
import telebot
from telebot import types

# ၁။ Bot Token နှင့် Channel အချက်အလက်
TOKEN = '7685203704:AAEEwolEBkEN7t2nCPT6b2IGy9heASzlDy8'
bot = telebot.TeleBot(TOKEN)
CHANNEL_ID = '@titokvideodowloader'
CHANNEL_LINK = 'https://t.me/titokvideodowloader'

# ၂။ Render Port Error ကျော်ရန် Flask Server တည်ဆောက်ခြင်း
app = Flask('')


@app.route('/')
def home():
  return 'Bot is running!'


def run():
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


# ၃။ Channel Join စစ်ဆေးသည့် Function
def check_sub(user_id):
  try:
    status = bot.get_chat_member(CHANNEL_ID, user_id).status
    return status in ['member', 'administrator', 'creator']
  except Exception as e:
    print(f'Channel check error: {e}')
    return False


# ၄။ /start Command
@bot.message_handler(commands=['start'])
def start(message):
  start_text = (
      '👋 မင်္ဂလာပါ! TikTok Video Downloader Bot မှ ကြိုဆိုပါတယ်။\n\n'
      '📖 **Bot အသုံးပြုနည်း**\n'
      '၁။ TikTok ဗီဒီယို Link ကို Copy ယူပါ။\n'
      '၂။ ၎င်း Link ကို ဤ Bot ထံသို့ ပို့ပေးပါ။\n\n'
      '📢 **မေတ္တာရပ်ခံချက်**\n'
      'ဝန်ဆောင်မှုကို ဆက်လက်ပေးနိုင်ရန် Channel ကို အရင် Join ပေးပါ။\n\n'
      '⚠️ Channel Join မထားပါက သုံး၍မရပါ။'
  )
  if check_sub(message.from_user.id):
    bot.reply_to(message, f'{start_text}\n\n✅ Link ပို့နိုင်ပါပြီ။')
  else:
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('📢 Join Channel', url=CHANNEL_LINK)
    )
    bot.send_message(message.chat.id, start_text, reply_markup=markup)


# ၅။ Video Download လုပ်သည့်အပိုင်း
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
      api_url = f'https://tikwm.com/api/?url={url}'
      res = requests.get(api_url).json()

      if res.get('code') == 0 and 'data' in res:
        video_url = res['data'].get('play')
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
            '❌ ဗီဒီယို ရှာမတွေ့ပါ (သို့) လင့်ခ် မှားယွင်းနေပါသည်။',
            message.chat.id,
            sent.message_id,
        )
    except Exception as e:
      print(f'Download Error: {e}')
      bot.edit_message_text(
          '❌ စနစ်အမှားအယွင်း ဖြစ်သွားပါသည်။ နောက်တစ်ကြိမ် ထပ်ကြိုးစားပါ။',
          message.chat.id,
          sent.message_id,
      )
  else:
    bot.reply_to(message, '💡 ကျေးဇူးပြု၍ မှန်ကန်သော TikTok Link ပို့ပေးပါ။')


if __name__ == '__main__':
  t = Thread(target=run)
  t.start()

# Bot ကို loop တစ်ခုထဲမှာ ဆက်တိုက် Run ထားခြင်း
while True:
  try:
    print('Bot စတင်အလုပ်လုပ်နေပါပြီ...')
    bot.polling(none_stop=True, timeout=60)
  except Exception as e:
    print(f'Bot Crash ဖြစ်သွားလို့ ၅ စက္ကန့်နေရင် ပြန်စပါမယ်: {e}')
    time.sleep(5)
