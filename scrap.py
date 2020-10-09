import requests
from bs4 import BeautifulSoup
import re
import random

MAIN_URL = "https://world.openfoodfacts.org"
URL = "https://es.openfoodfacts.org/tienda/mercadona"
LIMIT = 162
products = {}
def get_html(url, n=None):
    page = None
    if n:
        page = requests.get(url + "/" + str(n))
    else:
        page = requests.get(url)
    assert page is not None
    return page.text

def get_products():
    ul = soup.find("ul", "products")
    for a in ul.findChildren("a", recursive=True):
        title = a.get("title", None)
        link = re.sub(r"producto", "product", MAIN_URL + a.get("href", None))
        products[title] = {
            "link": link 
        }
        get_product(title, link)

        
def get_product(title, link):
    product_page_html = get_html(link)
    product_soup = BeautifulSoup(product_page_html, 'html.parser')
    get_weight(title, product_soup)
    get_origin(title, product_soup)
    get_brand(title, product_soup)
    get_categories(title, product_soup)
    get_nutrients(title, product_soup)
    get_image(title, product_soup)
    get_barcode(title, product_soup)
    get_price(title)
    get_stock(title)
    get_edible(title)
    get_times_sold(title)


def get_edible(title):
    products[title]["edible"] = True

def get_barcode(title, product_soup):
    barcode_span = product_soup.find("span", id="barcode")
    if barcode_span is not None:
        barcode = int(barcode_span.text)
    else:
        barcode = None
    products[title]["image"] = barcode

def get_image(title, product_soup):
    image_link = product_soup.find("img", id="og_image")
    if image_link is not None:
        products[title]["image"] = image_link["src"]
    else:
        products[title]["image"] = None

def get_stock(title):
    stock = random.randint(0, 50)
    products[title]["stock"] = stock

def get_times_sold(title):
    times_sold = random.randint(0, 50)
    products[title]["times_sold"] = times_sold

def get_price(title):
    price = round(random.uniform(0, 4), 2)
    products[title]["price"] = price

def get_nutrients(title, product_soup):
    nutrients = {}
    tbody = product_soup.find("tbody")
    for tr in tbody.findAll("tr"):
        tds = tr.findAll("td")
        nutrient_label = tds[0].text.strip()
        if len(tds) > 1:
            nutrient_value = tds[1].text.strip()
            nutrients[nutrient_label] = nutrient_value
        else:
            nutrients[nutrient_label] = None
    products[title]["nutrients"] = nutrients

        
def get_brand(title, product_soup):
    brand_span = product_soup.find("span", text="Brands:")
    if brand_span is not None:
        brand = re.sub(r"Brands:", "", brand_span.parent.text).strip()
        products[title]["brand"] = brand

def get_categories(title, product_soup):
    categories_span = product_soup.find("span", text="Categories:")
    if categories_span is not None:
        categories = re.sub(r"Categories:", "", categories_span.parent.text).strip().split(", ")
        products[title]["categories"] = categories

def get_origin(title, product_soup):
    origin_span = product_soup.find("span", text="Origin of ingredients:")
    if origin_span is not None:
        origin = re.sub(r"Origin of ingredients:", "", origin_span.parent.text).strip()
        products[title]["origin"] = origin

def get_weight(title, product_soup):
    quantity_span = product_soup.find("span", text="Quantity:")
    if quantity_span is not None:
        quantity = re.sub(r"Quantity:", "", quantity_span.parent.text).strip()
        products[title]["weight"] = quantity
    

def save():
    import json
    with open("products.json", "w") as f:
        json.dump(products, f)
n = 0
while n < LIMIT:
    html = get_html(URL, n)
    soup = BeautifulSoup(html, 'html.parser')
    get_products()
    save()
    n += 1
