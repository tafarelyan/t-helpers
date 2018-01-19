import requests
from bs4 import BeautifulSoup


def tomo_chan_tracker():
    url = 'https://dropoutmanga.wordpress.com/category/tomo-chan-wa-onna-no-ko/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    title = (soup.find('h1', {'class': 'entry-title'})
             .text.replace('\xa0', ' ').capitalize())
    chapter = (soup.find('div', {'class': 'entry-content'})
               .find('h2').text)
    url = (soup.find('h1', {'class': 'entry-title'})
           .find('a')['href'])

    return title + ' ' + chapter, url


def shokugeki_no_soma_tracker():
    r = requests.get('http://ww1.readshokugeki.com')
    soup = BeautifulSoup(r.content, 'html.parser')

    first_from_list = (
        soup.find('ul', {'class': 'chapters-list'})
        .find('li')
    )

    url = first_from_list.find('a')['href']
    chapter = list(first_from_list.strings)[1].split()

    return ' '.join(chapter[:-2]) + ' ' + chapter[-1], url
