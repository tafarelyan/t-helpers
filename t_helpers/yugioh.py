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

        return 'R${:.2f}'.format(avg_price * 3.2)

    url = 'https://www.trollandtoad.com/products/search.php'

    payload = {
        'search_words': query,
        'search_category': 4736,  # Yugioh
        'search_order': 'relevant_desc',
    }

    r = requests.get(url, params=payload)
    soup = BeautifulSoup(r.content, 'html.parser')

    results = (
        [x.text.replace('\xa0', '') for x in row.contents][:-1]
        for row in (soup.find('div', {'class': 'searchResults'})
                    .find_all('div', {'class': 'search_result_text'}))
    )

    price_list = []

    for row in results:
        if row[2] != 'Currently Out of Stock':
            avg_price = find_calculate_convert_currency(row[2])
            price_list.append({
                'card_name': row[0],
                'collection': row[1],
                'avg_price': avg_price,
            })

    return price_list
