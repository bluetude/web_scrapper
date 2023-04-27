from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time




driver_path = "/Library/chromedriver_mac_arm64/chromedriver"
chr_options = Options()
chr_options.add_experimental_option("detach", True)
chr_driver = webdriver.Chrome(driver_path, options=chr_options)
chr_driver.get("https://reverb.com/marketplace?query=akg%20c414&make=akg&product_type=pro-audio&condition=used")
time.sleep(10)
html = chr_driver.execute_script("return document.body.innerHTML;")
    
chr_driver.quit()

doc = BeautifulSoup(html, "html.parser")
with open ("index.html", "w") as file:
    file.write(str(doc))
print(doc.prettify())

