import requests


def tomo_chan_tracker():
    url = 'https://dropoutmanga.wordpress.com/category/tomo-chan-wa-onna-no-ko/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    chapter = (soup.find('div', {'class': 'entry-content'})
               .find('h2').text)
    return chapter
