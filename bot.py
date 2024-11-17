import os
import time
import logging
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from pathlib import Path
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed

banner = """
==================================================================
 █████╗ ██╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗ 
██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
███████║██║██████╔╝██║  ██║██████╔╝██║   ██║██████╔╝
██╔══██║██║██╔══██╗██║  ██║██╔══██╗██║   ██║██╔═══╝ 
██║  ██║██║██║  ██║██████╔╝██║  ██║╚██████╔╝██║     
╚═╝  ╚═╝╚═╝╚═╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     
                                                    
██╗███╗   ██╗███████╗██╗██████╗ ███████╗██████╗     
██║████╗  ██║██╔════╝██║██╔══██╗██╔════╝██╔══██╗    
██║██╔██╗ ██║███████╗██║██║  ██║█████╗  ██████╔╝    
██║██║╚██╗██║╚════██║██║██║  ██║██╔══╝  ██╔══██╗    
██║██║ ╚████║███████║██║██████╔╝███████╗██║  ██║    
╚═╝╚═╝  ╚═══╝╚══════╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝    

Join our Telegram channel for the latest updates: t.me/airdropinsiderid

Airdrop Insider
==================================================================
"""
print(banner)
time.sleep(1)

# Load environment variables
load_dotenv()

# Logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

# Constants
EXTENSION_ID = "caacbgbklghmpodbdafajbgdnegacfmo"
CRX_URL = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=98.0.4758.102&acceptformat=crx2,crx3&x=id%3D{EXTENSION_ID}%26uc&nacl_arch=x86-64"
EXTENSION_FILENAME = "app.crx"
USER = os.getenv("APP_USER")
PASSWORD = os.getenv("APP_PASS")

# Validate credentials
if not USER or not PASSWORD:
    logger.error("Please set APP_USER and APP_PASS environment variables")
    exit(1)

# Load proxies from file
with open("active_proxies.txt", "r") as f:
    proxies = [line.strip() for line in f]

# Initialize Fake User-Agent generator
ua = UserAgent()

# Download Chrome extension
def download_extension():
    """Download Chrome extension."""
    logger.info(f"Downloading extension from: {CRX_URL}")
    ext_path = Path(EXTENSION_FILENAME)
    if ext_path.exists() and time.time() - ext_path.stat().st_mtime < 86400:
        logger.info("Extension already downloaded, skipping...")
        return
    response = requests.get(CRX_URL, headers={"User-Agent": ua.random})
    if response.status_code == 200:
        ext_path.write_bytes(response.content)
        logger.info("Extension downloaded successfully")
    else:
        logger.error(f"Failed to download extension: {response.status_code}")
        exit(1)

# Setup Chrome options for the WebDriver with random User-Agent and Proxy
def setup_chrome_options(proxy=None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument(f"user-agent={ua.random}")  # Random User-Agent
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-dev-shm-usage")  # To avoid crashes in headless mode

    if proxy:
        chrome_options.add_argument(f"--proxy-server={proxy}")
        logger.info(f"Using proxy: {proxy}")

    # Use extensions if necessary
    ext_path = Path(EXTENSION_FILENAME).resolve()
    chrome_options.add_extension(str(ext_path))
    
    # Mask the WebDriver (to avoid detection)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    return chrome_options

# Log in to the web application
def login_to_app(driver):
    """Log in to the web application."""
    driver.get("https://app.gradient.network/")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Enter Email"]'))
    )
    driver.find_element(By.CSS_SELECTOR, '[placeholder="Enter Email"]').send_keys(USER)
    driver.find_element(By.CSS_SELECTOR, '[type="password"]').send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button").click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/dashboard/setting"]'))
    )
    logger.info("Logged in successfully")

# Open the Chrome extension
def open_extension(driver):
    """Open the Chrome extension."""
    driver.get(f"chrome-extension://{EXTENSION_ID}/popup.html")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Status")]'))
    )
    logger.info("Extension loaded successfully")

# Attempt connection using a proxy
def attempt_connection(proxy):
    """Attempt to connect using a proxy."""
    chrome_options = setup_chrome_options(proxy)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        download_extension()
        login_to_app(driver)
        open_extension(driver)
        logger.info(f"Connection successful with proxy: {proxy}")
        return driver
    except Exception as e:
        logger.warning(f"Proxy failed: {proxy} - Error: {e}")
        driver.quit()
        return None

# Worker function to handle proxy testing with delay
def worker(proxy):
    driver = attempt_connection(proxy)
    if driver:
        logger.info(f"Proxy {proxy} is working. Running tasks...")
        try:
            while True:
                time.sleep(random.uniform(20, 40))  # Random delay between actions to look more natural
                logger.info(f"Running tasks on proxy {proxy}...")
        finally:
            driver.quit()
    else:
        logger.info(f"Proxy {proxy} failed. Moving to next.")

# Main function to run proxies in parallel with random delays
def main():
    """Main function to run proxies in parallel."""
    max_workers = len(proxies)  # Number of threads equals the number of proxies
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(worker, proxy) for proxy in proxies]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error in worker: {e}")

if __name__ == "__main__":
    main()

