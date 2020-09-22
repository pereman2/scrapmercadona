import requests
from bs4 import BeautifulSoup

URL = "https://es.openfoodfacts.org/tienda/mercadona"
LIMIT = 162
def get_html(url, n):
    page = None
    if n:
        page = requests.get(url + "/" + str(n))
    else:
        page = requests.get(url)
    assert page is not None
    return page.content

def get_products():
    assert soup is not None
    ul = soup.find("ul", "products")
    for a in ul.findChildren("a", recursive=True):
        print(a.get("title", "No title attribute"))
        

n = 0
while n < LIMIT:
    html = get_html(URL, n)
    soup = BeautifulSoup(html, 'html.parser')
    get_products()
    n += 1
