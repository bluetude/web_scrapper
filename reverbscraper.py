from bs4 import BeautifulSoup

with open("index.html", "r") as file:
    doc = BeautifulSoup(file, "html.parser")

ul = doc.find("ul", class_="sortable-tiles")
li = ul.find_all("li", class_="sortable-tile")
mic_list = []
for mic in li:
    name = mic.find("h4", class_="grid-card__title")
    price = mic.find("span", class_="price-display")
    link = mic.find("a", class_="grid-card__inner")
    link = link["href"]
    link = f"https://reverb.com{link}"
    img = mic.find("img", loading="lazy")
    img = img["src"]
    mic_list.append((name.text, price.text, link, img))

print(mic_list)