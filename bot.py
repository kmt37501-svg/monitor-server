import telebot
import requests
import base64

# معلوماتك السرية
API_TOKEN = '8784944434:AAGe0YbqOludPp_65dQ81miLTfCnxXvChVg'
GH_TOKEN = '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'
REPO = 'kmt37501-svg/monitor-server'
CHAT_ID = '8343786519'

bot = telebot.TeleBot(API_TOKEN)

def update_github(status):
    url = f"https://api.github.com/repos/{REPO}/contents/control.txt"
    # نجيب الـ SHA للملف حتى نكدر نعدله
    r = requests.get(url, headers={"Authorization": f"token {GH_TOKEN}"})
    sha = r.json()['sha']
    
    payload = {
        "message": f"Command: {status}",
        "content": base64.b64encode(status.encode()).decode(),
        "sha": sha
    }
    requests.put(url, json=payload, headers={"Authorization": f"token {GH_TOKEN}"})

@bot.message_handler(commands=['start'])
def welcome(message):
    if str(message.chat.id) == CHAT_ID:
        bot.reply_to(message, "أهلاً عباس.. لوحة التحكم جاهزة.\nارسل 'تشغيل' للبدء أو 'إيقاف' للتعطيل.")

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    if str(message.chat.id) == CHAT_ID:
        if message.text == "تشغيل":
            update_github("START")
            bot.send_message(CHAT_ID, "🚀 تم! الملف صار START.. الأجهزة راح تبدأ الهجوم.")
        elif message.text == "إيقاف":
            update_github("OFF")
            bot.send_message(CHAT_ID, "🛑 تم الإيقاف.. السيرفر بوضع الاستعداد.")

bot.polling()
