import telebot
import requests
from telebot import types
import time
import os
from flask import Flask
from threading import Thread

# --- Render အတွက် Flask Server ---
app = Flask('')

@bot_app.route('/')
def home():
    return "Bot is alive and running!"

# --- အချက်အလက်များ (လူကြီးမင်းအတွက် အကုန်ဖြည့်ပြီးသား) ---
TOKEN = '7685203704:AAEU1nEHTwZiQwzz6xm5ao2G9QdGm7zMEDE'
GPLINK_URL = 'https://gplinks.co/EQpKYQH' 
ADMIN_ID = 7878088171  # လူကြီးမင်းရဲ့ ID အမှန်

bot = telebot.TeleBot(TOKEN)
user_usage = {}
user_list = set()

# --- Admin Stats Command ---
@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id == ADMIN_ID:
        total_users = len(user_list)
        bot.reply_to(message, f"📊 **Admin Panel**\n\n👥 စုစုပေါင်းအသုံးပြုသူ: {total_users} ယောက်", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ သင်သည် Admin မဟုတ်ပါ။")

# --- TikTok Link Handling ---
@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_tt(message):
    user_id = message.from_user.id
    url = message.text
    user_list.add(user_id)
    
    if user_id not in user_usage:
        user_usage[user_id] = 2

    if user_usage[user_id] <= 0:
        markup = types.InlineKeyboardMarkup()
        btn_ad = types.InlineKeyboardButton("🔓 ကြော်ငြာကြည့်ရန်", url=GPLINK_URL)
        btn_check = types.InlineKeyboardButton("✅ Check", callback_data="check_ad")
        markup.add(btn_ad, btn_check)
        bot.send_message(message.chat.id, "⚠️ အကြိမ်ရေ ကုန်ဆုံးသွားပါပြီ။", reply_markup=markup, parse_mode="Markdown")
        return

    status_msg = bot.reply_to(message, "⏳ ဗီဒီယိုကို ရှာဖွေနေပါသည်...")
    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        res = requests.get(api_url, timeout=15).json()
        if res.get('data') and res['data'].get('play'):
            video_url = res['data']['play']
            user_usage[user_id] -= 1
            bot.send_video(message.chat.id, video_url, caption=f"✅ ဒေါင်းလုဒ် အောင်မြင်ပါသည်!\n📊 လက်ကျန်: {user_usage[user_id]} ကြိမ်")
            bot.delete_message(message.chat.id, status_msg.message_id)
        else:
            bot.edit_message_text("❌ ဗီဒီယို ရှာမတွေ့ပါ။", message.chat.id, status_msg.message_id)
    except:
        bot.edit_message_text("❌ Server မအားသေးပါ။", message.chat.id, status_msg.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "check_ad")
def callback_check(call):
    user_usage[call.from_user.id] = 5
    bot.answer_callback_query(call.id, "🎉 ၅ ကြိမ် ထပ်တိုးပေးလိုက်ပါပြီ!")
    bot.edit_message_text("✅ အကြိမ်ရေ တိုးပြီးပါပြီ။", call.message.chat.id, call.message.message_id)

# --- Bot Polling ---
def run_bot():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except:
            time.sleep(15)

if __name__ == "__main__":
    # Flask ကို Background မှာ run ခြင်း
    t = Thread(target=run_bot)
    t.start()
    
    # Render Port အတွက် Flask ကို Port 8080 မှာ run ခြင်း
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
