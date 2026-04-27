import requests
import os
import time  # Import time for the delay
from datetime import datetime

# --- CONFIGURATION ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8512915922:AAGhZQW5ehBONNZeI-zTafUlgUA2uD1cWFc")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "1056958029")

# Target Wilaya Codes: 16 = Algiers, 18 = Jijel, 54 = In Guezzam (for testing)
TARGET_CODES = ["16", "18", "54"]

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Telegram notification sent!")
        else:
            print(f"❌ Failed to send Telegram: {response.text}")
    except Exception as e:
        print(f"❌ Error sending to Telegram: {e}")

def check_quotas():
    api_url = "https://adhahi.dz/api/v1/public/wilaya-quotas"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        found_matches = []
        for item in data:
            if item['wilayaCode'] in TARGET_CODES and item['available'] is True:
                found_matches.append(item['wilayaNameAr'])

        if found_matches:
            wilayas = " و ".join(found_matches)
            alert_text = f"🚨 *تنبيه أضاحي*\n\nالآن متوفر حجز في ولاية: *{wilayas}*\n\nسجل هنا: https://adhahi.dz/register/"
            send_telegram_msg(alert_text)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] No quota for Jijel/Algiers.")

    except Exception as e:
        print(f"❌ API Error: {e}")

if __name__ == "__main__":
    print("🚀 Script started. Press Ctrl+C to stop.")
    while True:
        check_quotas()
        # 300 seconds = 5 minutes
        time.sleep(20)