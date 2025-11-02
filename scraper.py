import os
import csv
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


EBAY_URL = "https://www.ebay.com/globaldeals/tech"
CSV_PATH = "ebay_tech_deals.csv"



def create_driver():
    options = Options()
    for arg in [
        "--headless=new",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--window-size=1920,1080",
    ]:
        options.add_argument(arg)
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)



def load_all_products(driver):
    driver.get(EBAY_URL)
    time.sleep(5)
    prev_height = 0
    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)
        height = driver.execute_script("return document.body.scrollHeight")
        if height == prev_height:
            break
        prev_height = height



def collect_products(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, "div.dne-itemtile")
    extracted = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for el in elements:
        def safe_get(selector, attr=None):
            try:
                item = el.find_element(By.CSS_SELECTOR, selector)
                return item.get_attribute(attr) if attr else item.text.strip()
            except:
                return "N/A"

        extracted.append({
            "timestamp": now,
            "title": safe_get(".dne-itemtile-title span"),
            "price": safe_get(".dne-itemtile-price"),
            "original_price": safe_get(".itemtile-price-strikethrough"),
            "item_url": safe_get(".dne-itemtile-detail a", "href"),
        })
    return extracted



def fetch_shipping(link):
    if not link.startswith("http"):
        return "Shipping info unavailable"

    try:
        driver = create_driver()
        driver.get(link)
        time.sleep(3)
        try:
            node = driver.find_element(
                By.XPATH,
                "//div[contains(@class,'ux-labels-values__values')]"
                "//span[not(contains(@class,'clipped')) and "
                "(contains(text(),'Shipping') or contains(text(),'shipping') or contains(text(),'International'))]"
            )
            result = node.text.strip()
        except:
            try:
                node = driver.find_element(
                    By.XPATH,
                    "//span[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'shipping')]"
                )
                result = node.text.strip()
            except:
                result = "Shipping info unavailable"

        driver.quit()
        if not result or result.lower() in ["see details", "for shipping", ""]:
            return "Shipping info unavailable"
        return " ".join(result.split())

    except Exception:
        try:
            driver.quit()
        except:
            pass
        return "Shipping info unavailable"


def main():
    browser = create_driver()
    load_all_products(browser)
    records = collect_products(browser)
    browser.quit()

    with ThreadPoolExecutor(max_workers=8) as pool:
        future_map = {pool.submit(fetch_shipping, r["item_url"]): r for r in records}
        for task in as_completed(future_map):
            rec = future_map[task]
            rec["shipping"] = task.result() or "Shipping info unavailable"

    fields = ["timestamp", "title", "price", "original_price", "shipping", "item_url"]
    exists = os.path.isfile(CSV_PATH)

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerows(records)

    print(f"Saved {len(records)} products to {CSV_PATH}")



if __name__ == "__main__":
    main()
