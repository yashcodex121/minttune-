#!/usr/bin/env python3
"""
Auto YouTube Cookie Renewal Script
Runs headless Chromium, logs into YouTube, exports cookies.txt
Usage: python3 renew_cookies.py
Cron: 0 */12 * * * /root/yash/minttune-/renew_cookies.py >> /tmp/cookie_renewal.log 2>&1
"""
import os
import sys
import time
import json

COOKIES_PATH = "/root/yash/minttune-/SHUKLAMUSIC/assets/cookies.txt"
# Set these as environment variables or hardcode (keep private)
YT_EMAIL = os.environ.get("YT_EMAIL", "")
YT_PASS  = os.environ.get("YT_PASS", "")

def renew_with_yt_dlp():
    """Use yt-dlp OAuth2 plugin — no browser needed."""
    try:
        import subprocess
        result = subprocess.run(
            ["yt-dlp", "--username", "oauth2", "--password", "", 
             "--cookies", COOKIES_PATH,
             "--skip-download", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
            capture_output=True, text=True, timeout=60
        )
        if os.path.exists(COOKIES_PATH) and os.path.getsize(COOKIES_PATH) > 100:
            print(f"[OK] Cookies renewed via yt-dlp oauth2")
            return True
    except Exception as e:
        print(f"[WARN] yt-dlp oauth2 failed: {e}")
    return False

def renew_with_selenium():
    """Headless Chromium login + cookie export."""
    if not YT_EMAIL or not YT_PASS:
        print("[ERROR] YT_EMAIL and YT_PASS env vars not set")
        return False
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,720")
        options.binary_location = "/usr/bin/chromium-browser"

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)

        # Go to YouTube login
        driver.get("https://accounts.google.com/signin/v2/identifier?service=youtube")
        time.sleep(2)

        # Enter email
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "identifier")))
        email_field.send_keys(YT_EMAIL)
        driver.find_element(By.ID, "identifierNext").click()
        time.sleep(2)

        # Enter password
        pass_field = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
        pass_field.send_keys(YT_PASS)
        driver.find_element(By.ID, "passwordNext").click()
        time.sleep(4)

        # Navigate to YouTube
        driver.get("https://www.youtube.com")
        time.sleep(3)

        # Export cookies in Netscape format
        cookies = driver.get_cookies()
        driver.quit()

        with open(COOKIES_PATH, "w") as f:
            f.write("# Netscape HTTP Cookie File\n")
            for c in cookies:
                domain = c.get("domain", "")
                flag = "TRUE" if domain.startswith(".") else "FALSE"
                path = c.get("path", "/")
                secure = "TRUE" if c.get("secure") else "FALSE"
                expiry = str(int(c.get("expiry", 0))) if c.get("expiry") else "0"
                name = c.get("name", "")
                value = c.get("value", "")
                f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")

        print(f"[OK] Cookies exported: {len(cookies)} cookies -> {COOKIES_PATH}")
        return True

    except Exception as e:
        print(f"[ERROR] Selenium failed: {e}")
        return False

if __name__ == "__main__":
    print(f"[START] Cookie renewal at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Try yt-dlp oauth2 first (no credentials needed)
    if renew_with_yt_dlp():
        sys.exit(0)
    
    # Fallback: Selenium with credentials
    if renew_with_selenium():
        sys.exit(0)
    
    print("[FAILED] All renewal methods failed")
    sys.exit(1)