      # API အသစ်တစ်ခုနဲ့ စမ်းသပ်ခြင်း
      api_url = f'https://www.tikwm.com/api/?url={url}&hd=1'
      headers = {
          'User-Agent': (
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
              ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
          )
      }
      res = requests.get(api_url, headers=headers).json()

      if res.get('code') == 0 and 'data' in res:
        # Watermark မပါတဲ့ HD ဗီဒီယိုလင့်ခ်ကို ယူခြင်း
        video_url = res['data'].get('hd_play') or res['data'].get('play')
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

