import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Tracker:
    def __init__(self):
        self.driver = None

    def start(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def check(self, name, url):
        try:
            print(f"Checking {name}")
            self.driver.get(url)
            time.sleep(3)

            title = self.driver.title
            print("Title:", title)

            if name.lower() in title.lower():
                print(f"✅ FOUND: {name}")
            else:
                print(f"❌ NOT FOUND: {name}")

        except Exception as e:
            print(f"⚠️ ERROR {name}: {e}")

    def stop(self):
        if self.driver:
            self.driver.quit()


def main():
    tracker = Tracker()
    tracker.start()

    items = [
        {
            "name": "HiBy FC5",
            "url": "https://example.com/fc5"
        },
        {
            "name": "Misheng Gemini",
            "url": "https://example.com/gemini"
        }
    ]

    for item in items:
        tracker.check(item["name"], item["url"])

    tracker.stop()


if __name__ == "__main__":
    main()
