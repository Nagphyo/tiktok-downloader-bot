import telebot
import requests
from telebot import types

# ၁။ Bot နှင့် Channel အချက်အလက်များ
TOKEN = "7685203704:AAEp_m-XOSi-SiRA0b9XrC-5HtGZZanLG0I" # Token အသစ်လဲထားလျှင် ဒီမှာ ပြန်ထည့်ပါ
bot = telebot.TeleBot(TOKEN)

CHANNEL_ID = "@Ytt_dowww_bot"  
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

# ၃။ /start Command (စာသားအသစ် ပြင်ဆင်ထားသည်)
@bot.message_handler(commands=['start'])
def start(message):
    start_text = (
        "👋 မင်္ဂလာပါခင်ဗျာ! TikTok Video Downloader Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "📖 **Bot အသုံးပြုနည်း**\n"
        "၁။ TikTok မှ မိမိဒေါင်းလုဒ်ဆွဲလိုသော ဗီဒီယို Link ကို Copy ယူပါ။\n"
        "၂။ ၎င်း Link ကို ဤ Bot ထံသို့ ပို့ပေးပါ။\n"
        "၃။ ခဏစောင့်ပြီးလျှင် Watermark မပါသော ဗီဒီယိုကို ရရှိပါမည်။\n\n"
        "📢 **မေတ္တာရပ်ခံချက်**\n"
        "ကျွန်ုပ်တို့၏ ဝန်ဆောင်မှုကို ဆက်လက်ထိန်းသိမ်းနိုင်ရန် အောက်ပါ Channel ကို အရင် Join ပေးဖို့ မေတ္တာရပ်ခံအပ်ပါသည်။\n\n"
        "⚠️ **သတိပေးချက်**\n"
        "Channel Join မထားပါက Bot ကို အသုံးပြု၍ ရမည်မဟုတ်ပါ။"
    )
    
    if check_sub(message.from_user.id):
        bot.reply_to(message, f"{start_text}\n\n✅ သင်သည် Channel Join ထားပြီးဖြစ်၍ Link ပို့နိုင်ပါပြီ။")
    else:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📢 Join Channel Here", url=CHANNEL_LINK)
        markup.add(btn)
        bot.send_message(message.chat.id, start_text, reply_markup=markup)

# ၄။ TikTok Video Download လုပ်သည့် အပိုင်း
@bot.message_handler(func=lambda message: True)
def handle_tiktok(message):
    if not check_sub(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)
        markup.add(btn)
        bot.send_message(
