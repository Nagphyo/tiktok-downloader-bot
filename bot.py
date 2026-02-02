import telebot
import requests
from telebot import types

# ၁။ Bot နှင့် Channel အချက်အလက်များ
TOKEN = "7685203704:AAEp_m-XOSi-SiRA0b9XrC-5HtGZZanLG0I"
bot = telebot.TeleBot(TOKEN)

CHANNEL_ID = "@Ytt_dowww_bot"  # လူကြီးမင်းရဲ့ Channel Username
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

# ၃။ /start Command
@bot.message_handler(commands=['start'])
def start(message):
    if check_sub(message.from_user.id):
        bot.reply_to(message, "✅ Channel Join ထားပြီးသား ဖြစ်လို့ TikTok Link ပို့ပေးနိုင်ပါပြီ။")
    else:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)
        markup.add(btn)
        bot.send_message(message.chat.id, "⚠️ ရှေ့ဆက်ရန် ကျွန်ုပ်တို့၏ Channel ကို အရင် Join ပေးပါဦး။ \n\nJoin ပြီးလျှင် /start ကို ပြန်နှိပ်ပါ။", reply_markup=markup)

# ၄။ TikTok Video Download လုပ်သည့် အပိုင်း
@bot.message_handler(func=lambda message: True)
def handle_tiktok(message):
    # အမြဲတမ်း Join မ Join အရင်စစ်မည်
    if not check_sub(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)
        markup.add(btn)
        bot.send_message(message.chat.id, "⚠️ ဗီဒီယိုဒေါင်းရန် Channel ကို အရင် Join ရပါမည်။", reply_markup=markup)
        return

    # User က Join ထားရင် Link စစ်မည်
    url = message.text
    if "tiktok.com" in url:
        sent_msg = bot.reply_to(message, "⏳ ဗီဒီယိုကို စစ်ဆေးနေပါတယ်၊ ခဏစောင့်ပေးပါ...")
        
        try:
            # TikTok API သို့ ချိတ်ဆက်ခြင်း (မူလအတိုင်း)
            api_url = f"https://tikwm.com/api/?url={url}"
            response = requests.get(api_url).json()
            
            if response.get("code") == 0:
                video_url = response['data']['play']
                bot.send_video(message.chat.id, video_url, caption="✅ ဒေါင်းလုဒ်ဆွဲမှု အောင်မြင်ပါသည်။ \n\n@titokvideodowloader")
                bot.delete_message(message.chat.id, sent_msg.message_id)
            else:
                bot.edit_message_text("❌ ဗီဒီယို ရှာမတွေ့ပါ။ Link မှန်မမှန် ပြန်စစ်ပေးပါ။", message.chat.id, sent_msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ အမှားအယွင်းတစ်ခု ဖြစ်ပေါ်ခဲ့ပါသည်- {str(e)}", message.chat.id, sent_msg.message_id)
    else:
        bot.reply_to(message, "💡 ကျေးဇူးပြု၍ TikTok Link တစ်ခု ပို့ပေးပါ။")

# ၅။ Bot ကို စတင်နှိုးခြင်း
print("Bot is running...")
bot.polling(none_stop=True)
