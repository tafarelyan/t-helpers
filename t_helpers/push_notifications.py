import os

import requests


def send_push(title, body):
    url = 'https://api.pushbullet.com/v2/pushes'

    headers = {
        'Access-Token': os.environ['PUSH_BULLET_API_TOKEN'],
    }

    payload = {
        'type': 'note',
        'title': 'Hello World',
        'body': 'No content',
    }

    r = requests.post(url, headers=headers, json=payload)

    return r.json()
