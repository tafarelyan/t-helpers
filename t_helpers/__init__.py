import os

from .push_bullet import send_push_notifications
from .telegram import create_chatbot
from .sptrans import *

__all__ = ['send_push', 'create_chatbot']

home = os.path.expanduser('~')

config = os.path.join(home, '.tconfig')
if not os.path.exists(config):
    os.makedirs(config)

credentials = os.path.join(config, 'credentials')
if not os.path.exists(credentials):
    print('You don\'t have a credentials file yet')
    print('Creating {}...'.format(credentials))

    with open(credentials, 'w') as f:
        pb_key = input('Insert PushBullet API KEY: ')
        if pb_key:
            f.write('PUSH_BULLET_API_TOKEN = {}\n'.format(pb_key))

        spt_key = input('Insert SPTrans API KEY: ')
        if spt_key:
            f.write('SPTRANS_API_TOKEN = {}\n'.format(spt_key))

with open(credentials, 'r') as f:
    for x in f.read().strip().split('\n'):
        key, value = x.split(' = ')
        os.environ[key] = value
