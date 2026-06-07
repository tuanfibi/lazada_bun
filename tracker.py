import os
import re
import time
import requests
import pandas as pd

from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram chưa cấu hình")
        return

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg
        },
        timeout=30
    )

def extract_price(text):
    matches = re.findall(r'([\d\.]+)\s*₫', text)

    prices = []

    for m in matches:
        try:
            prices.append(int(m.replace(".", "")))
        except:
            pass

    if prices:
        return min(prices)

    return None

def get_price(url):
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            url,
            wait_until="networkidle",
            timeout=60000
        )

        time.sleep(5)

        text = page.locator("body").inner_text()

        browser.close()

        return extract_price(text)

def main():

    df = pd.read_csv("products.csv")

    for _, row in df.iterrows():

        name = row["name"]
        url = row["url"]
        target = int(row["target_price"])

        print(f"Checking {name}")

        try:

            price = get_price(url)

            print(price)

            if price:

                message = (
                    f"📦 {name}\n"
                    f"Giá hiện tại: {price:,}đ\n"
                    f"Mục tiêu: {target:,}đ"
                )

                send_telegram(message)

                if price <= target:

                    send_telegram(
                        f"🔥 DEAL!\n{name}\n"
                        f"Giá chỉ còn {price:,}đ"
                    )

        except Exception as e:

            send_telegram(
                f"Lỗi kiểm tra {name}\n{e}"
            )

if __name__ == "__main__":
    main()
