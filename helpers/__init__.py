import os

from .constants import HOME
from .push_notifications import send_push
from .telegram_chabot_from_template import create_basic_chatbot

__all__ = ['send_push', 'HOME', 'create_basic_chatbot']

credentials = os.path.join(HOME, '.tcredentials')
if not os.path.exists(credentials):
    print('You don\'t have a credentials file yet')
    print('Creating {}...'.format(credentials))

    with open(credentials, 'w') as f:
        pb_key = input('Insert PushBullet API KEY: ')
        if pb_key:
            f.write('PUSH_BULLET_API_TOKEN = {}\n'.format(pb_key))

with open(credentials, 'r') as f:
    for x in f.read().strip().split('\n'):
        key, value = x.split(' = ')
        os.environ[key] = value
