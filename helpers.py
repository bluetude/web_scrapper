from bs4 import BeautifulSoup
from datetime import date
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('geardealz.db')
    conn.row_factory = sqlite3.Row
    return conn    

def scraper(html, site):
    if site == "reverb":
        return reverb_scraper(html)
    if site == "ebay":
        return ebay_scraper(html)

def reverb_scraper(html):
    print("Started scraping data from listing...")
    doc = BeautifulSoup(html, "html.parser")

    item_list = []

    ul = doc.find("ul", class_="tiles tiles--four-wide-max")
    if ul is None:
        return(item_list)
    li = ul.find_all("li", class_="tiles__tile")

    for item in li:
        if len(item) == 1:
            name = item.find("h4", class_="grid-card__title")
            price = item.find("meta", itemprop="price")["content"]
            currency = item.find("meta", itemprop="priceCurrency")["content"]
            link = item.find("meta", itemprop="url")["content"]
            img = item.find("img", loading="lazy")["src"]
            
            item_list.append((name.text, price, currency, link, img))

    print("Finished scraping.")

    return(item_list)

def ebay_scraper(html):
    print("Started scraping data from listing...")
    doc = BeautifulSoup(html, "html.parser")

    item_list = []

    ul = doc.find("ul", class_="srp-results srp-list clearfix")
    if ul is None:
        return(item_list)
    li = ul.find_all("li", class_="s-item")

    for item in li:
        name = item.find("span", role="heading")
        price = item.find("span", class_="s-item__price")
        link = item.find("a", class_="s-item__link")["href"]
        img = item.find("img")["src"]
        currency = "USD"
        
        price = price.text[1:]
        price = price.replace(",", "")

        name = name.text
        name = name.replace("New Listing", "")
        
        item_list.append((name, price, currency, link, img))

    print("Finished scraping.")

    return(item_list)

def olx_scraper(html):
    return

def save_to_db(item_list, name):
    print(f"Saving {name} listings to db...")
    with get_db_connection() as conn:
        for item in item_list:
            cursor = conn.cursor()
            link = item[3]
            cursor.execute('SELECT link FROM auctions WHERE link = ?', (link,))
            result = cursor.fetchone()
            if result is not None:
                continue

            data = (name, item[0], float(item[1]), item[2], item[3], item[4], date.today())
            
            print("Adding new listing.")
            cursor.execute("INSERT INTO auctions (item_name, title, price, currency, link, img_link, date) VALUES (?, ?, ?, ?, ?, ?, ?)", data)
            conn.commit()
    
    print("Saved succesfully.")
    print("")

def check_no_of_pages(html, site):
    if site == "reverb":
        return check_no_of_pages_reverb(html)
    if site == "ebay":
        return check_no_of_pages_ebay(html)

def check_no_of_pages_reverb(html):
    doc = BeautifulSoup(html, "html.parser")

    print("Checking number of pages...")

    links_list = []
    links = doc.find_all("a", class_="pagination__button--number")
    for link in links:
        link = link["href"]
        links_list.append(f"https://reverb.com/{link}")
    return links_list

def check_no_of_pages_ebay(html):
    doc = BeautifulSoup(html, "html.parser")

    print("Checking number of pages...")

    links_list = []
    links = doc.find_all("a", class_="pagination__item")
    for link in links:
        link = link["href"]
        links_list.append(link)
    return links_list


