from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema


def fuzzy_query_to_exact_match(card_name):
    url = 'https://www.google.com.br/search'

    payload = {
        'q': 'yugioh ' + card_name,
    }

    r = requests.get(url, params=payload)
    soup = BeautifulSoup(r.content, 'html.parser')

    for tag in soup.find_all('h3', {'class': 'r'}):
        url_wikia = parse_qs(
            urlparse(
                tag.find('a')['href']
            ).query
        )['q'][0]

        try:
            r = requests.get(url_wikia)
            soup = BeautifulSoup(r.content, 'html.parser')
            return soup.find('h1').text

        except MissingSchema:
            pass


def search_troll_and_toad(query):

    def find_calculate_convert_currency(string):
        first_index = string.find('$') + 1
        second_index = string.find('$', first_index) + 1

        if second_index:
            end = first_index + string[first_index:].find(' ')
            first_price = float(string[first_index:end])
            second_price = float(string[second_index:])
            avg_price = (first_price + second_price) / 2
        else:
            avg_price = float(string[first_index:])

        return 'R$ {:.2f}'.format(avg_price * 3.2).replace('.', ',')

    url = 'https://www.trollandtoad.com/products/search.php'

    payload = {
        'search_words': fuzzy_query_to_exact_match(query),
        'search_category': 4736,  # Yugioh
        'search_order': 'relevant_desc',
    }

    r = requests.get(url, params=payload)
    soup = BeautifulSoup(r.content, 'html.parser')

    results = (
        [x.text.replace('\xa0', '') for x in row.contents]
        for row in (soup.find('div', {'class': 'searchResults'})
                    .find_all('div', {'class': 'search_result_text'}))
    )

    price_list = []

    for row in results:
        if row[2] != 'Currently Out of Stock':
            avg_price = find_calculate_convert_currency(row[2])
            price_list.append({
                'card_name': row[0],
                #  'collection': row[1],
                'avg_price': avg_price,
            })

    return price_list


def search_duel_shop(query):
    card_query = fuzzy_query_to_exact_match(query)

    url = 'https://www.duelshop.com.br/procurar'

    payload = {
        'controller': 'search',
        'orderby': 'price',
        'orderway': 'asc',
        'search_query': card_query,
    }

    r = requests.get(url, params=payload)
    soup = BeautifulSoup(r.content, 'html.parser')

    if soup.find('p', {'class': 'alert'}):
        return 'No results for %s in Duel Shop' % card_query

    results = (
        row for row in soup.find_all('div', {'class': 'product-container'})
        if not row.find('div', {'class': 'product-disable-box'})
    )

    price_list = []

    for row in results:
        card_name = row.find('a', {'class': 'product-name'}).text
        avg_price = row.find('span', {'class': 'product-price'}).text

        price_list.append({
            'card_name': card_name.strip(),
            'avg_price': avg_price.strip()
        })

    if price_list:
        return price_list
    else:
        return card_query + ' out of stock in Duel Shop'


def search_epic_game(query):
    card_query = fuzzy_query_to_exact_match(query)

    url = 'https://www.epicgame.com.br/'

    payload = {
        'view': 'ecom/itens',
        'busca': card_query,
        'fOrder': 3,
        'fShow': 160,
        'txt_estoque':  1,
    }

    r = requests.get(url, params=payload)
    soup = BeautifulSoup(r.content, 'html.parser')

    if soup.find('div', {'class': 'alertaErro'}):
        return 'No results for %s in Epic Game' % card_query

    card_name = (
        soup.find('div', {'class': 'itemMain'})
        .find_all('td')[2].text.strip()
    )

    results = (
        [x.text.strip() for x in row.find_all('td', {'class': 'hmin30'})]
        for row in (soup.find('div', {'class': 'itemMain'})
                    .find_all('table')[-1]
                    .find_all('tr')[1:])
    )

    price_list = []

    for row in results:
        if row[3] == '-':
            row[3] = '...'

        price_list.append({
            'card_name': ' - '.join([card_name, row[0], row[3]]),
            'avg_price': row[5],
        })

    if price_list:
        return price_list
    else:
        return card_query + ' out of stock in Epic'
