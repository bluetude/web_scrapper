from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from helpers import scraper, get_db_connection, save_to_db, check_no_of_pages


# Initializing chromedriver with Selenium
driver_path = "/Library/chromedriver_mac_arm64/chromedriver"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_driver = webdriver.Chrome(driver_path, options=chrome_options)

# Getting a list of links to scrap data from a db
links_list = []
with get_db_connection() as conn:
    print("Getting list of links from db...")
    links = conn.execute("SELECT link, name, site FROM links").fetchall()
    for row in links:
        links_list.append((row["link"], row["name"], row["site"]))
    print("")

# Scraping data from every link
for link in links_list:
    name = link[1]
    site = link[2]
    chrome_driver.get(link[0])
    time.sleep(10)
    html = chrome_driver.execute_script("return document.body.innerHTML;")
    
    print(f"Started scraping listings for {name}")

    # Checking if listing have multiple pages
    pages = check_no_of_pages(html, site)
    if len(pages) > 0:
        print(f"Number of pages: {len(pages)}")
        for page in pages:
            print(f"Scraping page {page}")
            chrome_driver.get(page)
            time.sleep(10)
            html = chrome_driver.execute_script("return document.body.innerHTML;")
            item_list = scraper(html, site)
            save_to_db(item_list, name, site)
    else:
        print(f"Scraping page {link[0]}")
        item_list = scraper(html, site)
        save_to_db(item_list, name, site)

chrome_driver.quit()

print("Closing program.")



