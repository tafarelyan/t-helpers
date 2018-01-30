import requests
from bs4 import BeautifulSoup


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
        'search_words': query,
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


def fuzzy_card_to_exact_match(card_name):
    pass


def search_duel_shop(query):
    url = 'https://www.duelshop.com.br/procurar'

    payload = {
        'controller': 'search',
        'orderby': 'price',
        'orderway': 'asc',
        'search_query': query,
    }

    r = requests.get(url, params=payload)
    soup = BeautifulSoup(r.content, 'html.parser')

    if soup.find('p', {'class': 'alert'}):
        return 'No results in Duel Shop'

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

    return price_list


def search_epic_game(query):
    url = 'https://www.epicgame.com.br/'

    payload = {
        'view': 'ecom/itens',
        'busca': query,
        'fOrder': 3,
        'fShow': 160,
        'txt_estoque':  1,
    }

    r = requests.get(url, params=payload)
    soup = BeautifulSoup(r.content, 'html.parser')

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

    return price_list
