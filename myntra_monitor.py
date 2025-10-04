import time
import requests
import undetected_chromedriver as uc
import os
from dotenv import load_dotenv

# Load .env variables (optional locally)
load_dotenv()

# === CONFIG from Environment Variables ===
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
CHECK_URL = os.environ.get("CHECK_URL", "https://www.myntra.com/14773806")
CHECK_KEYWORD = os.environ.get("CHECK_KEYWORD", "BFFNEW15")
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", 60))
ALERT_COOLDOWN = int(os.environ.get("ALERT_COOLDOWN", 300))

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Telegram alert sent.")
        else:
            print(f"⚠️ Telegram failed: {response.text}")
    except Exception as e:
        print("⚠️ Telegram error:", e)

def check_myntra():
    try:
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")

        with uc.Chrome(options=options) as driver:
            driver.get(CHECK_URL)
            time.sleep(7)
            page_text = driver.page_source

        if CHECK_KEYWORD.lower() in page_text.lower():
            send_telegram_message(f"⚡ Coupon {CHECK_KEYWORD} is LIVE on Myntra!")
            return True
        return False

    except Exception as e:
        print("⚠️ Error checking Myntra:", e)
        return False

if __name__ == "__main__":
    print("🔍 Starting Myntra Coupon Monitor...")
    while True:
        found = check_myntra()
        if found:
            print(f"🎉 Coupon found! Waiting {ALERT_COOLDOWN} seconds...")
            time.sleep(ALERT_COOLDOWN)
        else:
            print(f"⏱ Not found, checking again in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)
