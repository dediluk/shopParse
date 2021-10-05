import requests
from bs4 import BeautifulSoup

# URL = 'https://catalog.onliner.by/mobile?on_sale=1&page=1'
URL = 'https://by.wildberries.ru/catalog/elektronika/smartfony-i-telefony?sort=popular&bid=fd75b2c6-d30e-4cd0-9ba5-70849a942ab7'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'accept': '*/*'
}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def get_data(html):
    soap = BeautifulSoup(html, "html.parser")
    items = soap.find_all('div', class_='product-card__wrapper')


    res = [{'price': item.find(class_='lower-price').get_text().replace('\xa0', ' ')} for item in items]

    print(res)



def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_data(html.text)
    else:
        print('Ошибка доступа к сайту')


parse()
