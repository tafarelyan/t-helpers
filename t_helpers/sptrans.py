import os
import pprint

import requests


VERSION = 2.1
BASE_URL = 'http://api.olhovivo.sptrans.com.br/v{0}'.format(VERSION)


def authenticate():
    url = BASE_URL + '/Login/Autenticar'

    payload = {
        'token': os.environ['SPTRANS_API_TOKEN'],
    }

    r = requests.post(url, params=payload)

    if r.json():
        print('Authentication success')
        return r.cookies
    else:
        raise ValueError('Wrong API TOKEN')


def line_search(line):
    url = BASE_URL + '/Linha/Buscar'

    payload = {
        'termosBusca': line
    }

    cookies = authenticate()

    r = requests.get(url, params=payload, cookies=cookies)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(r.json())


def bus_position(line_code):
    url = BASE_URL + '/Posicao/Linha'
    
    payload = {
        'codigoLinha': line_code,
    }

    cookies = authenticate()

    r = requests.get(url, params=payload, cookies=cookies)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(r.json())
