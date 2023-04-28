from bs4 import BeautifulSoup
from datetime import date
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('geardealz.db')
    conn.row_factory = sqlite3.Row
    return conn    

def reverb_scrapper(doc):
    ul = doc.find("ul", class_="tiles tiles--four-wide-max")
    li = ul.find_all("li", class_="tiles__tile")

    item_list = []

    for item in li:
        if len(item) == 1:
            name = item.find("h4", class_="grid-card__title")
            price = item.find("meta", itemprop="price")["content"]
            currency = item.find("meta", itemprop="priceCurrency")["content"]
            link = item.find("meta", itemprop="url")["content"]
            img = item.find("img", loading="lazy")["src"]
            
            item_list.append((name.text, price, currency, link, img))

    return(item_list)

def save_to_db(item_list, name):
    with get_db_connection() as conn:
        for item in item_list:
            cursor = conn.cursor()
            link = item[3]
            cursor.execute('SELECT link FROM auctions WHERE link = ?', (link,))
            result = cursor.fetchone()
            if result is not None:
                continue

            data = (name, item[0], float(item[1]), item[2], item[3], item[4], date.today())
            
            cursor.execute("INSERT INTO auctions (item_name, title, price, currency, link, img_link, date) VALUES (?, ?, ?, ?, ?, ?, ?)", data)
            conn.commit()


