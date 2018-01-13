import os

import requests


def send_push_notification(title, body):
    url = 'https://api.pushbullet.com/v2/pushes'

    headers = {
        'Access-Token': os.environ['PUSH_BULLET_API_TOKEN'],
    }

    payload = {
        'type': 'note',
        'title': title,
        'body': body,
    }

    r = requests.post(url, headers=headers, data=payload)

    return r.json()
