import undetected_chromedriver as uc
import time

# 1. Setup Options
options = uc.ChromeOptions()
options.add_argument("--start-maximized")

# Optional: If you are on Linux/Chromium, uncomment the line below to point to your binary
# options.binary_location = "/usr/sbin/chromium" 

# 2. Launch the "Undetected" browser
print("Launching stealth browser...")
driver = uc.Chrome(options=options)

try:
    url = "https://www.marinetraffic.com/"
    print(f"Navigating to {url}...")
    
    # 3. Load the page
    driver.get(url)
    
    # Wait to see if the block page appears
    print("Waiting 15 seconds... Check the window to see if it loaded!")
    time.sleep(15)

finally:
    driver.quit()
