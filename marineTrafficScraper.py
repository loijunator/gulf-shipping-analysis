from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import undetected_chromedriver as uc

import json
import time 
import os
import pandas as pd

#options section
options = uc.ChromeOptions()
options.add_argument("start-maximized")
options.binary_location = "/usr/sbin/chromium"
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = uc.Chrome(options=options, enable_cdp_events=True)
url_custom = "https://www.marinetraffic.com/en/ais/home/centerx:61.8/centery:28.8/zoom:6"
# driver.add_cdp_listener("Network.responseReceived", network_event_handler)
driver.get(url_custom)  
time.sleep(30)

requests = driver.get_log("performance")
vessels = []
for entry in requests:
    message = json.loads(entry["message"])["message"]

    if message["method"] == "Network.responseReceived":
        #found_count += 1
        params = message.get("params", {})
        url = response.get("response", {}).get("url", "")
        if "get_data_json" in url: #station:0 requests all have this
            request_id = params.get("requestId")
            body_data = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
            raw_json = json.loads(body_data.get('body', '[]'))
            #save to file
            # with open(f"marinetraffic_data_{found_count}.json", "w") as f:
            #     f.write(raw_json)
            if isinstance(raw_json, list):
                vessels.extend(raw_json)
            elif 'data' in raw_json:
                vessels.extend(raw_json['data'])

if vessels:
    df = pd.DataFrame(vessels)
    print(df.head(20))
driver.quit()
