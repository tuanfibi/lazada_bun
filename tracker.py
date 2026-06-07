import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TrackerPro:
    def __init__(self):
        self.driver = None

    # =========================
    # INIT BROWSER (STABLE)
    # =========================
    def start_browser(self):
        print("[INIT] Starting Chrome...")

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        self.driver.set_page_load_timeout(20)
        print("[OK] Browser started")

    # =========================
    # SAFE GET WITH RETRY
    # =========================
    def safe_get(self, url, retries=3):
        for i in range(retries):
            try:
                print(f"[LOAD] Attempt {i+1}: {url}")
                self.driver.get(url)
                return True
            except Exception as e:
                print(f"[WARN] Load failed: {e}")
                time.sleep(2)

        print("[FAIL] Giving up URL:", url)
        return False

    # =========================
    # CHECK ITEM
    # =========================
    def check_item(self, name, url):
        try:
            print(f"\n==============================")
            print(f"[CHECK] {name}")

            if not self.safe_get(url):
                return

            time.sleep(3)

            title = self.driver.title
            print("[TITLE]", title)

            if name.lower() in title.lower():
                print(f"[FOUND] {name}")
            else:
                print(f"[NOT FOUND] {name}")

        except Exception as e:
            print("[ERROR]", name)
            traceback.print_exc()

    # =========================
    # CLOSE
    # =========================
    def stop(self):
        if self.driver:
            self.driver.quit()
            print("[CLOSE] Browser closed")


def main():
    tracker = TrackerPro()

    tracker.start_browser()

    items = [
        {"name": "HiBy FC5", "url": "https://example.com/fc5"},
        {"name": "Misheng Gemini", "url": "https://example.com/gemini"},
    ]

    for item in items:
        tracker.check_item(item["name"], item["url"])

    tracker.stop()


if __name__ == "__main__":
    main()
