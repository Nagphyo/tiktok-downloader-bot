import telebot
from telebot import types

# ၁။ Token နှင့် Channel အချက်အလက် (မမှားပါစေနဲ့)
TOKEN = "7685203704:AAEp_m-XOSi-SiRA0b9XrC-5HtGZZanLG0I"
bot = telebot.TeleBot(TOKEN)
CHANNEL_ID = "@titokvideodowloader" 
CHANNEL_LINK = "https://t.me/titokvideodowloader"

# ၂။ Channel Join မ Join စစ်ဆေးသည့် Function
def check_sub(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        if status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return False

# ၃။ Start Command
@bot.message_handler(commands=['start'])
def start(message):
    if check_sub(message.from_user.id):
        bot.reply_to(message, "✅ Channel Join ထားပြီးသား ဖြစ်လို့ TikTok Link ပို့ပေးနိုင်ပါပြီ။")
    else:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)
        markup.add(btn)
        bot.send_message(message.chat.id, "⚠️ ရှေ့ဆက်ရန် ကျွန်ုပ်တို့၏ Channel ကို အရင် Join ပေးပါဦး။ Join ပြီးလျှင် /start ပြန်နှိပ်ပါ။", reply_markup=markup)

# ၄။ TikTok Link များ လက်ခံသည့်အပိုင်း (ဒီနေရာမှာ လူကြီးမင်းရဲ့ မူလ Downloader Code ရှိရပါမယ်)
@bot.message_handler(func=lambda message: True)
def handle_tiktok(message):
    # အမြဲတမ်း Join မ Join အရင်စစ်မည်
    if not check_sub(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)
        markup.add(btn)
        bot.send_message(message.chat.id, "⚠️ ဗီဒီယိုဒေါင်းရန် Channel ကို အရင် Join ရပါမည်။", reply_markup=markup)
        return

    # User က Join ထားရင် ဗီဒီယို စဒေါင်းမည်
    if "tiktok.com" in message.text:
        bot.reply_to(message, "⏳ ဗီဒီယိုကို စစ်ဆေးနေပါတယ်၊ ခဏစောင့်ပေးပါ...")
        # ဒီနေရာမှာ လူကြီးမင်းရဲ့ မူလ ဗီဒီယိုဒေါင်းတဲ့ (Requests/Download) Code တွေကို ဆက်ရေးပါ
    else:
        bot.reply_to(message, "❌ ကျေးဇူးပြု၍ TikTok Link အမှန်ကိုသာ ပို့ပေးပါ။")

bot.polling()
