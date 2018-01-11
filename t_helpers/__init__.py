import os

from .misc import (create_credentials, credentials_to_environ,
                   install_chromedriver)
from .push_bullet import send_push_notifications
from .telegram import create_chatbot
from .sptrans import SPTrans

__all__ = ['send_push', 'create_chatbot']

CONFIG = os.path.join(os.path.expanduser('~'), '.tconfig')
if not os.path.exists(CONFIG):
    os.makedirs(CONFIG)

CREDENTIALS_PATH = os.path.join(CONFIG, 'credentials')
if not os.path.exists(CREDENTIALS_PATH):
    create_credentials(CREDENTIALS_PATH)

credentials_to_environ(CREDENTIALS_PATH)

CHROMEDRIVER_PATH = os.path.join(CONFIG, 'chromedriver')
if not os.path.exists(CHROMEDRIVER_PATH):
    install_chromedriver(path=CONFIG)
