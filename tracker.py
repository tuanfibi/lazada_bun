import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Tracker:
    def __init__(self):
        self.driver = None

    def start_browser(self):
        options = Options()
        options.add_argument("--headless")  # chạy nền
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)

    def check_item(self, url, name):
        try:
            self.driver.get(url)
            time.sleep(3)

            title = self.driver.title
            print(f"Checking {name}")

            if name.lower() in title.lower():
                print(f"[FOUND] {name}")
            else:
                print(f"[NOT FOUND] {name}")

        except Exception as e:
            print(f"[ERROR] {name}: {e}")

    def close(self):
        if self.driver:
            self.driver.quit()


def main():
    tracker = Tracker()
    tracker.start_browser()

    items = [
        {"name": "HiBy FC5", "url": "https://example.com/fc5"},
        {"name": "Misheng Gemini", "url": "https://example.com/gemini"},
    ]

    for item in items:
        tracker.check_item(item["url"], item["name"])

    tracker.close()


if __name__ == "__main__":
    main()
