import telebot
import requests
from telebot import types
import os
from flask import Flask
from threading import Thread

# ၁။ Bot Token နှင့် Channel အချက်အလက်
TOKEN = "7685203704:AAEEwolEBkEN7t2nCPT6b2IGy9heASzlDy8" 
bot = telebot.TeleBot(TOKEN)
CHANNEL_ID = "@titokvideodowloader"  
CHANNEL_LINK = "https://t.me/titokvideodowloader"

# ၂။ Render Port Error ကျော်ရန် Flask Server တည်ဆောက်ခြင်း
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# ၃။ Channel Join စစ်ဆေးသည့် Function
def check_sub(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# ၄။ /start Command
@bot.message_handler(commands=['start'])
def start(message):
    start_text = (
        "👋 မင်္ဂလာပါ! TikTok Video Downloader Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "📖 **Bot အသုံးပြုနည်း**\n"
        "၁။ TikTok ဗီဒီယို Link ကို Copy ယူပါ။\n"
        "၂။ ၎င်း Link ကို ဤ Bot ထံသို့ ပို့ပေးပါ။\n\n"
        "📢 **မေတ္တာရပ်ခံချက်**\n"
        "ဝန်ဆောင်မှုကို ဆက်လက်ပေးနိုင်ရန် Channel ကို အရင် Join ပေးပါ။\n\n"
        "⚠️ Channel Join မထားပါက သုံး၍မရပါ။"
    )
    if check_sub(message.from_user.id):
        bot.reply_to(message, f"{start_text}\n\n✅ Link ပို့နိုင်ပါပြီ။")
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
        bot.send_message(message.chat.id, start_text, reply_markup=markup)

# ၅။ Video Download လုပ်သည့်အပိုင်း
@bot.message_handler(func=lambda message: True)
def handle_tiktok(message):
    if not check_sub(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
        bot.send_message(message.chat.id, "⚠️ Channel အရင် Join ပေးပါ။", reply_markup=markup)
        return

    url = message.text
    if "tiktok.com" in url:
        sent = bot.reply_to(message, "⏳ စစ်ဆေးနေပါတယ်...")
        try:
            res = requests.get(f"https://tikwm.com/api/?url={url}").json()
            if res.get("code") == 0:
                bot.send_video(message.chat.id, res['data']['play'], caption="✅ Done!\n@titokvideodowloader")
                bot.delete_message(message.chat.id, sent.message_id)
            else:
                bot.edit_message_text("❌ ဗီဒီယို ရှာမတွေ့ပါ။", message.chat.id, sent.message_id)
        except:
            bot.edit_message_text("❌ အမှားအယွင်း ဖြစ်သွားပါသည်။", message.chat.id, sent.message_id)
    else:
        bot.reply_to(message, "💡 TikTok Link ပို့ပေးပါ။")

# ၆။ Bot နှင့် Server ကို တစ်ပြိုင်နက်နှိုးခြင်း
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
