import requests
from bs4 import BeautifulSoup
import re

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
    get_nutrients(title, product_soup)
    get_image(title, product_soup)

def get_image(title, product_soup):
    image_link = product_soup.find("img", id="og_image")
    products[title]["image"] = image_link["src"]

def get_nutrients(title, product_soup):
    nutrients = {}
    tbody = product_soup.find("tbody")
    for tr in tbody.findAll("tr"):
        tds = tr.findAll("td")
        nutrient_label = tds[0].text.strip()
        nutrient_value = tds[1].text.strip()
        nutrients[nutrient_label] = nutrient_value
    products[title]["nutrients"] = nutrients


            
        
def get_weight(title, product_soup):
    quantity_span = product_soup.find("span", text="Quantity:")
    if quantity_span is not None:
        quantity = re.sub(r"Quantity:", "", quantity_span.parent.text)
        products[title]["weight"] = quantity
    

n = 0
while n < LIMIT:
    html = get_html(URL, n)
    soup = BeautifulSoup(html, 'html.parser')
    get_products()
    n += 1
