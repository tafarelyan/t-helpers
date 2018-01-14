import os

from .misc import (create_credentials, credentials_to_environ,
                   install_chromedriver)
from .flights import Decolar
from .telegram import create_chatbot
from .youtube import download_from_youtube
from .push_bullet import send_push_notification
from .mailing import Mailing
from .sptrans import SPTrans

__all__ = ['send_push_notification', 'create_chatbot', 'download_from_youtube',
           'install_chromedriver', 'Decolar', 'Mailing', 'SPTrans']

CONFIG = os.path.join(os.path.expanduser('~'), '.tconfig')
if not os.path.exists(CONFIG):
    os.makedirs(CONFIG)

CREDENTIALS_PATH = os.path.join(CONFIG, 'credentials')
if not os.path.exists(CREDENTIALS_PATH):
    create_credentials(CREDENTIALS_PATH)

credentials_to_environ(CREDENTIALS_PATH)
