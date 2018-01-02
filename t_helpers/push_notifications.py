import os
import json
import urllib.request


def send_push(title, body):
    url = 'https://api.pushbullet.com/v2/pushes'

    headers = {
        'Access-Token': os.environ['PUSH_BULLET_API_TOKEN'],
        'Content-Type': 'application/json',
    }

    payload = {
        'type': 'note',
        'title': 'Hello World',
        'body': 'No content',
    }
    data = json.dumps(payload).encode('utf8')

    req = urllib.request.Request(url, headers=headers, data=data)
    response = urllib.request.urlopen(req)

    return json.loads(response.read().decode('utf8'))
