import telebot
import requests
from telebot import types
import time
import os
from flask import Flask
from threading import Thread

# --- Render Web Server ---
bot_app = Flask('')

@bot_app.route('/')
def home():
    return "✅ Bot is Online and Ready!"

# လူကြီးမင်း၏ Bot အချက်အလက်များ
TOKEN = '7685203704:AAEU1nEHTwZiQwzz6xm5ao2G9QdGm7zMEDE'
GPLINK_URL = 'https://gplinks.co/EQpKYQH' 
ADMIN_ID = 7878088171 

bot = telebot.TeleBot(TOKEN)
user_usage = {}
user_list = set()

# --- Start Command ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_list.add(user_id)
    welcome_msg = (
        "🌟 **TikTok Video Downloader မှ ကြိုဆိုပါတယ်!** 🌟\n\n"
        "Link ပေးပို့ရုံဖြင့် Watermark မပါသော ဗီဒီယိုများကို ရယူနိုင်ပါပြီ။\n\n"
        "🎁 **လက်ဆောင်:** အခမဲ့ (၂) ကြိမ် ဒေါင်းလုဒ်ဆွဲနိုင်ပါသည်။"
    )
    bot.send_message(message.chat.id, welcome_msg, parse_mode="Markdown")

# --- TikTok Video Handling ---
@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_tt(message):
    user_id = message.from_user.id
    user_list.add(user_id)
    
    if user_id not in user_usage:
        user_usage[user_id] = 2 

    if user_usage[user_id] <= 0:
        request_text = (
            "⚠️ **ဒေါင်းလုဒ်လုပ်ခွင့် အကြိမ်ရေ ကုန်ဆုံးသွားပါပြီ**\n\n"
            "Bot ကို ဆက်လက်အသုံးပြုနိုင်ရန် အောက်ပါအတိုင်း ကူညီပေးပါခင်ဗျာ -\n\n"
            "၁။ ကျေးဇူးပြု၍ **VPN (USA သို့မဟုတ် UK)** လေး ခံပေးပါ 🙏\n\n"
            "၂။ အောက်က **'🔓 အကြိမ်ရေတိုးရန်'** ခလုတ်ကို နှိပ်ပြီး ကြော်ညာကို အဆုံးထိ ကြည့်ပေးပါ။\n\n"
            "၃။ ကြော်ညာကြည့်ပြီးသွားလျှင် **'✅ Check အတည်ပြုမည်'** ဆိုသည့် ခလုတ်ကို မဖြစ်မနေ နှိပ်ပေးပါခင်ဗျာ။\n\n"
            "ကျေးဇူးတင်ရှိပါတယ်! ❤️"
        )
        markup = types.InlineKeyboardMarkup()
        btn_ad = types.InlineKeyboardButton("🔓 အကြိမ်ရေတိုးရန် နှိပ်ပါ", url=GPLINK_URL)
        btn_check = types.InlineKeyboardButton("✅ Check အတည်ပြုမည်", callback_data="check_ad")
        markup.add(btn_ad, btn_check)
        bot.send_message(message.chat.id, request_text, reply_markup=markup, parse_mode="Markdown")
        return

    status = bot.reply_to(message, "⏳ ဗီဒီယိုကို ရှာဖွေနေပါသည်...")
    try:
        api_url = f"https://www.tikwm.com/api/?url={message.text}"
        res = requests.get(api_url, timeout=15).json()
        if res.get('data') and res['data'].get('play'):
            video_url = res['data']['play']
            user_usage[user_id] -= 1
            bot.send_video(message.chat.id, video_url, caption=f"✅ ဒေါင်းလုဒ် အောင်မြင်ပါသည်!\n📊 လက်ကျန်: {user_usage[user_id]} ကြိမ်")
            bot.delete_message(message.chat.id, status.message_id)
        else:
            bot.edit_message_text("❌ ဗီဒီယို ရှာမတွေ့ပါ။", message.chat.id, status.message_id)
    except:
        bot.edit_message_text("❌ စနစ်ချို့ယွင်းနေပါသည်။", message.chat.id, status.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "check_ad")
def callback_check(call):
    user_usage[call.from_user.id] = 5
    bot.answer_callback_query(call.id, "🎉 ၅ ကြိမ် ထပ်တိုးပေးလိုက်ပါပြီ!")
    bot.edit_message_text("✅ အကြိမ်ရေ (၅) ကြိမ် တိုးပြီးပါပြီ။ Link ပြန်ပို့နိုင်ပါပြီ ခင်ဗျာ။", call.message.chat.id, call.message.message_id)

def run_bot():
    while True:
        try: 
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            time.sleep(10)

if __name__ == "__main__":
    t = Thread(target=run_bot)
    t.daemon = True
    t.start()
    # Render အတွက် Port 10000 ကို အဓိကထား သုံးခိုင်းခြင်း
    port = int(os.environ.get('PORT', 10000))
    bot_app.run(host='0.0.0.0', port=port)
