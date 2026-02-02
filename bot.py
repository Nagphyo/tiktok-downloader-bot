import telebot
import requests
from telebot import types

# ၁။ Bot နှင့် Channel အချက်အလက်များ
TOKEN = "7685203704:AAEEwolEBkEN7t2nCPT6b2IGy9heASzlDy8" # Token အသစ်လဲထားလျှင် ဒီမှာ ပြန်ထည့်ပါ
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
        bot.send_message(message.chat.id, "⚠️ ဗီဒီယိုဒေါင်းယူရန် Channel ကို အရင် Join ပေးပါ။ Join ပြီးမှ /start ကို ပြန်နှိပ်ပါ။", reply_markup=markup)
        return

    url = message.text
    if "tiktok.com" in url:
        sent_msg = bot.reply_to(message, "⏳ ဗီဒီယိုကို စစ်ဆေးနေပါတယ်၊ ခဏစောင့်ပေးပါ...")
        try:
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

bot.polling(none_stop=True)
