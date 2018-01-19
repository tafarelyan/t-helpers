import os

import requests


def send_push_notification(title, body, link=None):
    url = 'https://api.pushbullet.com/v2/pushes'

    headers = {
        'Access-Token': os.environ['PUSH_BULLET_API_TOKEN'],
    }

    if link:
        payload = {
            'type': 'link',
            'title': title,
            'body': body,
            'url': link
        }
    else:
        payload = {
            'type': 'note',
            'title': title,
            'body': body,
        }

    r = requests.post(url, headers=headers, data=payload)

    return r.json()
