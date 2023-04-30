from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from helpers import reverb_scrapper, get_db_connection, save_to_db, check_no_of_pages_reverb


# Initializing chromedriver with Selenium
driver_path = "/Library/chromedriver_mac_arm64/chromedriver"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_driver = webdriver.Chrome(driver_path, options=chrome_options)

# Getting a list of links to scrap data from a db
links_list = []
with get_db_connection() as conn:
    print("Getting list of links from db...")
    links = conn.execute("SELECT link, name FROM reverb_links").fetchall()
    for row in links:
        links_list.append((row["link"], row["name"]))
    print("")

# Scraping data from every link
for link in links_list:
    chrome_driver.get(link[0])
    time.sleep(10)
    html = chrome_driver.execute_script("return document.body.innerHTML;")
    name = link[1]

    print(f"Started scraping listings for {name}")

    # Checking if listing have multiple pages
    pages = check_no_of_pages_reverb(html)
    if len(pages) > 0:
        print(f"Number of pages: {len(pages)}")
        for page in pages:
            print(f"Scraping page {page}")
            chrome_driver.get(page)
            time.sleep(10)
            html = chrome_driver.execute_script("return document.body.innerHTML;")
            item_list = reverb_scrapper(html)
            save_to_db(item_list, name)
    else:
        print(f"Scraping page {link[0]}")
        item_list = reverb_scrapper(html)
        save_to_db(item_list, name)

chrome_driver.quit()

print("Closing program.")


# chrome_driver.get("https://reverb.com/marketplace?query=AKG%20C414&make=akg&product_type=pro-audio&condition=used&sort=published_at%7Cdesc")
# time.sleep(10)
# html = chrome_driver.execute_script("return document.body.innerHTML;")

# chrome_driver.quit()

# doc = BeautifulSoup(html, "html.parser")
# with open ("index.html", "w") as file:
#     file.write(str(doc))
# name = "AKG C414"
# item_list = reverb_scrapper(doc)
# save_to_db(item_list, name)


