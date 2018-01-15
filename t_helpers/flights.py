import json
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from .config import CHROMEDRIVER_PATH
from .push_bullet import send_push_notification


class Decolar(object):

    def __init__(self):
        self.results = []

    def __enter__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        self.browser = webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH,
            chrome_options=options
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

    def get_flights(self, from_, to_):
        self.browser.get('https://www.decolar.com/passagens-aereas')

        origin = (
            self.browser
            .find_element_by_class_name('searchbox-sbox-all-boxes')
            .find_element_by_css_selector('div[class*="sbox-origin-container"]')
            .find_element_by_css_selector('input[class*="origin-input"]')
        )
        origin.clear()
        origin.send_keys(from_)

        destination = (
            self.browser
            .find_element_by_class_name('searchbox-sbox-all-boxes')
            .find_element_by_css_selector('div[class*="sbox-destination-container"]')
            .find_element_by_css_selector('input[class*="destination-input"]')
        )
        destination.clear()
        destination.send_keys(to_)

        (self.browser
         .find_element_by_class_name('searchbox-sbox-all-boxes')
         .find_element_by_css_selector('input[class*="sbox-bind-checked-no-specified-date"]')
         .send_keys(Keys.SPACE))

        # Close elements that will fuck up
        time.sleep(1)
        (self.browser
         .find_element_by_css_selector('span[class*="as-login-close"]')
         .click())

        (self.browser
         .find_element_by_class_name('searchbox-sbox-all-boxes')
         .find_element_by_css_selector('div[class*="sbox-origin-container"]')
         .find_element_by_css_selector('ul[class="geo-autocomplete-list"]')
         .find_element_by_css_selector('a[href="#"]')
         .click())

        (self.browser
         .find_element_by_class_name('searchbox-sbox-all-boxes')
         .find_element_by_css_selector('div[class*="sbox-destination-container"]')
         .find_element_by_css_selector('ul[class="geo-autocomplete-list"]')
         .find_element_by_css_selector('a[href="#"]')
         .click())

        (self.browser
         .find_element_by_class_name('searchbox-sbox-all-boxes')
         .find_element_by_css_selector('a[class*="sbox-search')
         .click())

        assert self.browser.current_url != 'https://www.decolar.com/passagens-aereas'
        time.sleep(2)
        for cluster in self.browser.find_elements_by_css_selector('div[class*="flights-cluster"]'):
            currency = cluster.find_element_by_css_selector('span[class*="price-mask"]').text
            total_amount = (cluster.find_element_by_css_selector('span[class*="price-amount"]')
                            .text.replace(',', '').replace('.', ''))

            cluster_dict = {
                'currency': currency,
                'total_amount': '{:4.2f}'.format(float(total_amount))
            }

            for subcluster in cluster.find_elements_by_class_name('sub-cluster'):
                route_type = subcluster.find_element_by_css_selector('route-info-item[itemtype="type"]').text

                weekday, day = subcluster.find_element_by_class_name('day').text.split()
                month, year = subcluster.find_element_by_class_name('month-and-year').text.split()

                departure = subcluster.find_element_by_css_selector('span[class*="route-departure-location"]')
                departure_airport = departure.find_element_by_css_selector('span[class*="airport"]').text
                departure_city = departure.find_element_by_css_selector('span[class*="city-departure"]').text
                departure_time = subcluster.find_element_by_css_selector('itinerary-element[class="leave"]').text

                stops = subcluster.find_element_by_css_selector('itinerary-element[class="stops"]').text
                stops = int(stops.split(' ')[0]) if stops != 'Direto' else 0

                arrival = subcluster.find_element_by_css_selector('span[class*="route-arrival-location"]')
                arrival_airport = arrival.find_element_by_css_selector('span[class*="airport"]').text
                arrival_city = arrival.find_element_by_css_selector('span[class*="city-arrival"]').text

                arrive = subcluster.find_element_by_css_selector('itinerary-element[class="arrive"]')
                arrive_time = arrive.find_element_by_class_name('hour').text

                try:
                    days_difference = arrive.find_element_by_class_name('days-difference').text
                    days_difference = [int(s) for s in days_difference if s.isdigit()][0]
                except NoSuchElementException:
                    days_difference = 0

                total_time = subcluster.find_element_by_css_selector('itinerary-element[class="time"]').text

                cluster_dict[route_type.lower()] = {
                    'weekday': weekday,
                    'day': '{:02d}'.format(int(day)),
                    'month': month,
                    'year': year,
                    'departure': {
                        'airport': departure_airport,
                        'city': departure_city,
                        'time': departure_time,
                    },
                    'stops': stops,
                    'arrival': {
                        'airport': arrival_airport,
                        'city': arrival_city,
                        'time': arrive_time
                    },
                    'days_difference': days_difference,
                    'total_time': total_time
                }

            print(json.dumps(cluster_dict, indent=4))
            self.results.append(cluster_dict)

    def send_push(self):
        from_city = self.results[0]['ida']['departure']['city']
        to_city = self.results[0]['ida']['arrival']['city']
        output = [from_city + ' ' + to_city]

        for row in self.results:
            price = row['total_amount']
            from_ = row['ida']['day'] + ' ' + row['ida']['month']
            to_ = row['volta']['day'] + ' ' + row['volta']['month']

            print('R$ {}: {} - {}'.format(price, from_, to_))
            output.append('R$ {}: {} - {}'.format(price, from_, to_))

        send_push_notification('Decolar Flights', '\n'.join(output))
