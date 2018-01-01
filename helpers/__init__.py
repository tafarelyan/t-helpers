import os

from .constants import HOME
from .push_notifications import send_push

__all__ = ['send_push', 'HOME']

credentials = os.path.join(HOME, '.tcredentials')
if not os.path.exists(credentials):
    print('You don\'t have a credentials file yet')
    print(f'Creating {credentials}...')

    with open(credentials, 'w') as f:
        pb_key = input('Insert PushBullet API KEY: ')
        if pb_key:
            f.write(f'PUSH_BULLET_API_TOKEN = {pb_key}\n')

with open(credentials, 'r') as f:
    for x in f.read().strip().split('\n'):
        key, value = x.split(' = ')
        os.environ[key] = value
