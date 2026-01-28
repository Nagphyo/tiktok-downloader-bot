import telebot
import requests
from telebot import types
import time
from flask import Flask
from threading import Thread

# --- Render Port Error မတက်အောင် Flask Server တည်ဆောက်ခြင်း ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- ပြင်ဆင်ရန် အပိုင်း (လူကြီးမင်းရဲ့ ID နဲ့ Token အမှန်များ) ---
TOKEN = '7685203704:AAEU1nEHTwZiQwzz6xm5ao2G9QdGm7zMEDE'
GPLINK_URL = 'https://gplinks.co/EQpKYQH' 
ADMIN_ID = 7878088171  # လူကြီးမင်းရဲ့ ID အမှန်ကို ထည့်ပေးထားပါတယ်

bot = telebot.TeleBot(TOKEN)
user_usage = {}
user_list = set()

# --- Start Command ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_list.add(user_id)
    welcome_text = (
        "👋 **TikTok Downloader Bot မှ ကြိုဆိုပါတယ်!**\n\n"
        "🛠 **အသုံးပြုနည်း**\n"
        "၁။ TikTok Link ကို Copy ယူပါ။\n"
        "၂။ ဤ Bot ထံသို့ Link ပို့ပေးပါ။\n\n"
        "🎁 **အခမဲ့ အသုံးပြုနိုင်မှု**\n"
        "• ပထမဆုံး **၂ ကြိမ်** အခမဲ့ စမ်းသုံးနိုင်ပါတယ်။\n"
        "• အကြိမ်ရေကုန်ပါက ကြော်ညာကြည့်ပြီး **၅ ကြိမ်စီ** ထပ်တိုးရယူနိုင်ပါတယ်ဗျ။"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# --- Admin Stats Command ---
@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id == ADMIN_ID:
        total_users = len(user_list)
        bot.reply_to(message, f"📊 **Admin Panel**\n\n👥 စုစုပေါင်းအသုံးပြုသူ: {total_users} ယောက်", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ သင်သည် Admin မဟုတ်သဖြင့် ဤ Command ကို သုံးခွင့်မရှိပါ။")

# --- TikTok Link Handling ---
@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def handle_tt(message):
    user_id = message.from_user.id
    url = message.text
    user_list.add(user_id)
    
    # Usage logic
    if user_id not in user_usage:
        user_usage[user_id] = 2

    if user_usage[user_id] <= 0:
        markup = types.InlineKeyboardMarkup()
        btn_ad = types.InlineKeyboardButton("🔓 VPN ဖွင့်ပြီး ကြော်ငြာကြည့်ရန်", url=GPLINK_URL)
        btn_check = types.InlineKeyboardButton("✅ Check အကြိမ်ရေတိုးမည်", callback_data="check_ad")
        markup.add(btn_ad)
        markup.add(btn_check)
        bot.send_message(message.chat.id, "⚠️ **အကြိမ်ရေ ကုန်ဆုံးသွားပါပြီ**\n\nအပေါ်ကလင့်ခ်မှာ ကြော်ညာကြည့်ပြီး Check ကိုနှိပ်ပါဗျ။", reply_markup=markup, parse_mode="Markdown")
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
            bot.edit_message_text("❌ ဗီဒီယို ရှာမတွေ့ပါ။ Link ပြန်စစ်ပေးပါဗျ။", message.chat.id, status_msg.message_id)
    except Exception:
        bot.edit_message_text("❌ Server မအားသေးလို့ ခဏနေမှ ပြန်စမ်းပေးပါဗျ။", message.chat.id, status_msg.message_id)

# --- Ad Check Callback ---
@bot.callback_query_handler(func=lambda call: call.data == "check_ad")
def callback_check(call):
    user_id = call.from_user.id
    user_usage[user_id] = 5
    bot.answer_callback_query(call.id, "🎉 ၅ ကြိမ် ထပ်တိုးပေးလိုက်ပါပြီ!", show_alert=True)
    bot.edit_message_text("✅ အကြိမ်ရေ တိုးပြီးပါပြီ။ Link ပြန်ပို့နိုင်ပါပြီဗျ။", call.message.chat.id, call.message.message_id)

# --- Bot အမြဲနိုးကြားစေရန် Loop ပတ်ခြင်း ---
if __name__ == "__main__":
    keep_alive()  # Render Port Error မတက်အောင် Server စတင်ခြင်း
    print("Bot is starting...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            time.sleep(15)
