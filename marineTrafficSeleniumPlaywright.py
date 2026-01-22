from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import undetected_chromedriver as uc

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
driver = uc.Chrome(desired_capabilities=capabilities)


requests = driver.get_log("performance")
for request in requests:
      message = json.loads(request.get("message", {}))
      url = message.get("message", {}).get("params", {}).get("documentURL")
      if "text" in url:
          #Intercept this request
