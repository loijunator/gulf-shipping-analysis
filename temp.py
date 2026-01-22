from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import undetected_chromedriver as uc

import json
import time 
import os
import pandas as pd

options = uc.ChromeOptions()
options.add_argument("start-maximized")
options.binary_location = "/usr/sbin/chromium"

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
driver = uc.Chrome(options=options, desired_capabilities=capabilities, enable_cdp_events=True)
# url = "https://www.marinetraffic.com/"
url_custom = "https://www.marinetraffic.com/en/ais/home/centerx:61.8/centery:28.8/zoom:6"
driver.add_cdp_listener("Network.responseReceived", network_event_handler)
driver.get(url_custom)  
time.sleep(15)

requests = driver.get_log("performance")
for request in requests:
      message = json.loads(request.get("message", {}))
      url = message.get("message", {}).get("params", {}).get("documentURL")
      if "station:0" in url:
            response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
            # 'response_body' is a dict containing 'body' (the data) and 'base64Encoded' (bool)
            captured_data = response_body['body']
            print("--- Captured Data Preview ---")
            print(captured_data[:500]) # Print first 500 characters
driver.quit()
