from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from helpers import reverb_scrapper, get_db_connection, save_to_db



driver_path = "/Library/chromedriver_mac_arm64/chromedriver"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_driver = webdriver.Chrome(driver_path, options=chrome_options)
chrome_driver.get("https://reverb.com/marketplace?query=AKG%20C414&make=akg&product_type=pro-audio&condition=used&sort=published_at%7Cdesc")
time.sleep(10)
html = chrome_driver.execute_script("return document.body.innerHTML;")
    
chrome_driver.quit()

doc = BeautifulSoup(html, "html.parser")
with open ("index.html", "w") as file:
    file.write(str(doc))
name = "AKG C414"
item_list = reverb_scrapper(doc)
save_to_db(item_list, name)


