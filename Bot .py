import telebot
import requests
from telebot import types

TOKEN = '7685203704:AAEU1nEHTwZiQwzz6xm5ao2G9QdGm7zMEDE'
GPLINK_URL = 'https://gplinks.co/EQpKYQH' 

bot = telebot.TeleBot(TOKEN)
user_usage = {}

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "👋 **TikTok Downloader Bot မှ ကြိုဆိုပါတယ်!**\n\n"
        "🛠 **အသုံးပြုနည်း (User Guide)**\n"
        "၁။ TikTok Link ကို Copy ယူပါ။\n"
        "၂။ ဤ Bot ထံသို့ Link ပို့ပေးပါ။\n\n"
        "🎁 **အခမဲ့ အသုံးပြုနိုင်မှု**\n"
        "• ပထမဆုံး **၂ ကြိမ်** အခမဲ့ စမ်းသုံးနိုင်ပါတယ်။\n"
        "• အကြိမ်ရေကုန်ပါက ကြော်ငြာကြည့်ပြီး **၅ ကြိမ်စီ** ထပ်တိုးရယူနိုင်ပါတယ်ဗျ။\n\n"
        "🙏 **မေတ္တာရပ်ခံစာ**\n"
        "Bot လေး ၂၄ နာရီ အမြဲရှင်သန်နိုင်ဖို့ Server ဖိုးများအတွက် ကြော်ငြာကြည့်ရှုပေးဖို့ အနူးအညွတ် မေတ္တာရပ်ခံပါတယ်ဗျ။ 😊"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_tt(message):
    user_id = message.from_user.id
    url = message.text
    if "tiktok.com" not in url: return

    if user_id not in user_usage:
        user_usage[user_id] = 2

    if user_usage[user_id] <= 0:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("🔓 VPN ဖွင့်ပြီး ကြော်ငြာကြည့်ရန်", url=GPLINK_URL)
        markup.add(btn)
        
        ad_msg = (
            "⚠️ **အကြိမ်ရေ ကုန်ဆုံးသွားပါပြီ**\n\n"
            "✅ **အဆင့် (၁):** အောက်ကခလုတ်ကိုနှိပ်ပြီး ကြော်ငြာကြည့်ပေးပါ။\n"
            "✅ **အဆင့် (၂):** ပြီးလျှင် **Telegram ထဲသို့ ပြန်ဝင်ပါ**။\n"
            "✅ **အဆင့် (၃):** Link ပြန်ပို့ပေးပါ။ ၅ ကြိမ် ထပ်ရပါပြီ။\n\n"
            "🌐 **မှတ်ချက်:** လင့်မပွင့်ပါက **VPN (Singapore)** ဖွင့်ပေးပါရန် မေတ္တာရပ်ခံပါသည်။"
        )
        bot.send_message(message.chat.id, ad_msg, reply_markup=markup, parse_mode="Markdown")
        user_usage[user_id] = 5
        return

    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        res = requests.get(api_url).json()
        video_url = res['data']['play']
        user_usage[user_id] -= 1
        caption = f"✅ ဒေါင်းလုဒ် အောင်မြင်ပါတယ်ဗျ။\n📊 လက်ကျန်: {user_usage[user_id]} ကြိမ်"
        bot.send_video(message.chat.id, video_url, caption=caption)
    except:
        bot.send_message(message.chat.id, "❌ လိုင်းမတည်ငြိမ်သဖြင့် ခဏနေမှ ပြန်စမ်းပေးပါဗျ။")

bot.polling(none_stop=True)
