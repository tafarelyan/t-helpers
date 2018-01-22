import os
import pprint

import requests


class SPTrans(object):

    VERSION = 2.1
    BASE_URL = 'http://api.olhovivo.sptrans.com.br/v{0}'.format(VERSION)

    def __init__(self):
        self._authenticate()

    def _authenticate(self):
        self.session = requests.Session()

        r = self.session.post('{0}/Login/Autenticar?token={1}'.format(
            self.BASE_URL, os.environ['SPTRANS_API_TOKEN']
        ))

        if r.json():
            print('Authentication success')
        else:
            raise ValueError('Wrong API TOKEN')

    def bus_position(self, line, sentido=1):
        url = '{0}/Linha/Buscar?termosBusca={1}'.format(self.BASE_URL, line)
        for row in self.session.get(url).json():
            if row['sl'] == sentido:
                url = '{0}/Posicao/Linha?codigoLinha={1}'.format(self.BASE_URL, row['cl'])
                r = self.session.get(url)

                pp = pprint.PrettyPrinter(indent=2)
                pp.pprint(row)
                pp.pprint(r.json())

                return r.json()

    def bus_estimate_time(self, line, parada_id=None, sentido=1):
        url = '{0}/Linha/Buscar?termosBusca={1}'.format(self.BASE_URL, line)
        for row in self.session.get(url).json():
            if row['sl'] == sentido:
                payload = {
                    'codigoLinha': row['cl'],
                }

                if parada_id:
                    payload['codigoParada'] = parada_id

                r = self.session.get(self.BASE_URL + '/Previsao', params=payload)
                print(r.url)

                pp = pprint.PrettyPrinter(indent=2)
                pp.pprint(r.json())
