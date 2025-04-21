import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

banner = """
==================================================================
Join our Telegram channel for the latest updates: t.me/airdropscriptfa 

GRADIENT ACTIVE PROXY CHECKER - Airdrop Insider - RESHARED BY AIRDROPSCRIPTFA 
==================================================================
"""
print(banner)
time.sleep(1)

# Logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

# Load proxies from file
PROXY_FILE = "proxies.txt"
ACTIVE_PROXY_FILE = "checked_proxies.txt"

def load_proxies(file_path):
    """Load proxies from a file."""
    with open(file_path, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]
    return proxies

def save_active_proxies(proxies):
    """Save active proxies to a file."""
    with open(ACTIVE_PROXY_FILE, "w") as f:
        f.writelines(f"{proxy}\n" for proxy in proxies)

def check_proxy(proxy):
    """Check if a proxy can connect to a target URL."""
    target_url = "https://app.gradient.network/"  
    try:
        response = requests.get(
            target_url,
            proxies={"http": proxy, "https": proxy},
            timeout=10
        )
        if response.status_code == 200:
            logger.info(f"Proxy {proxy} is active")
            return proxy
    except Exception as e:
        logger.warning(f"Proxy {proxy} failed: {e}")
    return None

def run_proxy_checker(proxies):
    """Run proxy checker for a list of proxies."""
    logger.info("Starting proxy checker...")
    active_proxies = []
    with ThreadPoolExecutor(max_workers=10) as executor:  # Atur jumlah thread sesuai kebutuhan
        futures = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
        for future in as_completed(futures):
            result = future.result()
            if result:
                active_proxies.append(result)
    logger.info(f"Active proxies found: {len(active_proxies)}")
    return active_proxies

def main():
    """Main function to run proxy checker and execute bot tasks."""
    # Load proxies
    proxies = load_proxies(PROXY_FILE)
    if not proxies:
        logger.error(f"No proxies found in {PROXY_FILE}")
        return

    # Check proxies
    active_proxies = run_proxy_checker(proxies)
    if not active_proxies:
        logger.error("No active proxies found. Exiting...")
        return

    # Save active proxies
    save_active_proxies(active_proxies)
    logger.info(f"Active proxies saved to {ACTIVE_PROXY_FILE}")

    # Run main bot with active proxies
    logger.info("Starting bot execution with active proxies...")

if __name__ == "__main__":
    main()
