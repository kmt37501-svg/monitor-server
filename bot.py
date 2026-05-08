import telebot, requests, base64

TOKEN = "8784944434:AAGe0YbqOludPp_65dQ81miLTfCnxXvChVg"
GH_TOKEN = "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"
REPO = "kmt37501-svg/monitor-server"

bot = telebot.TeleBot(TOKEN)

def update_status(new_content):
    url = f"https://api.github.com/repos/{REPO}/contents/control.txt"
    # جلب SHA الملف الحالي للتحديث
    r = requests.get(url, headers={"Authorization": f"token {GH_TOKEN}"}).json()
    sha = r['sha']
    
    payload = {
        "message": "Update status",
        "content": base64.b64encode(new_content.encode()).decode(),
        "sha": sha
    }
    requests.put(url, json=payload, headers={"Authorization": f"token {GH_TOKEN}"})

@bot.message_handler(func=lambda m: m.text == "تشغيل")
def start_cmd(message):
    update_status("START")
    bot.reply_to(message, "🚀 الأمر وصل! الملف صار START.. الأجهزة بدأت الهجوم.")

@bot.message_handler(func=lambda m: m.text == "إيقاف")
def stop_cmd(message):
    update_status("OFF")
    bot.reply_to(message, "🛑 تم الإيقاف.. الأجهزة بوضع السكون.")

bot.polling()
