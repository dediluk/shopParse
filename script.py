import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup

FILENAME = 'pzz.csv'
URL = 'https://dominos.by/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'accept': '*/*'
}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def save_data_in_csv(data: list) -> None:
    with open(FILENAME, 'w', newline='') as file:
        columns = ['Название', 'Вес', 'Цена']
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def save_data_in_xlsx(data: list) -> None:
    df = pd.DataFrame(data)
    df.to_excel('pzz.xlsx', index=False)


def get_data(html) -> list:
    soap = BeautifulSoup(html, "html.parser")
    items = soap.find_all('div', class_='product-card product-card--vertical')

    data = [
        {
            'Название': item.find(class_='product-card__title').get_text(),
            'Вес': item.find(class_='product-card__modification-info-weight').get_text(),
            'Цена': item.find(class_='product-card__modification-info-price').get_text(),
        }

        for item in items
    ]

    return sorted(data, key=lambda data: data['Цена'])


def parse():
    html = get_html(URL)
    print(type(html))
    if html.status_code == 200:
        data = get_data(html.text)
        save_data_in_xlsx(data)
        save_data_in_csv(data)
    else:
        print('Ошибка доступа к сайту')


parse()
