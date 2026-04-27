import requests
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TARGET_CODES = ["16", "18"] # Algiers and Jijel

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def check_quotas():
    api_url = "https://adhahi.dz/api/v1/public/wilaya-quotas"
    response = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()
    
    found = [item['wilayaNameAr'] for item in data if item['wilayaCode'] in TARGET_CODES and item['available']]
    if found:
        send_telegram_msg(f"🚨 *تنبيه أضاحي*\nمتوفر حجز في: *{' و '.join(found)}*\nhttps://adhahi.dz/register/")

if __name__ == "__main__":
    check_quotas()