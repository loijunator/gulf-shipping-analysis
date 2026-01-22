from seleniumwire import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc 

import time 
import pandas as pd 
import os

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google.Inc",
        platform="Win32",
        webgl_vendor="Intel.Inc",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
# url below centered on persian gulf, strait of hormuz and northern arabian sea 
driver.get("https://www.marinetraffic.com/en/ais/home/centerx:61.8/centery:28.8/zoom:6")

for request in driver.requests:
    if request.response:
        print(f"URL: {request.url}")
        print(f"Method: {request.method}")
        print(f"Response Status Code: {request.response.status_code}")
time.sleep(30)
driver.close()
