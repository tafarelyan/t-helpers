import os
import io
import zipfile

import requests


def create_credentials(credentials_path):
    print('You don\'t have a credentials file yet')
    print('Creating {}...'.format(credentials_path))

    with open(credentials_path, 'w') as f:
        os = input('Which OS (Windows/MacOS/Linux)? ')
        if os:
            f.write('OS = {}\n'.format(os.lower()))

        pb_key = input('Insert PushBullet API KEY: ')
        if pb_key:
            f.write('PUSH_BULLET_API_TOKEN = {}\n'.format(pb_key))

        spt_key = input('Insert SPTrans API KEY: ')
        if spt_key:
            f.write('SPTRANS_API_TOKEN = {}\n'.format(spt_key))


def credentials_to_environ(credentials_path):
    with open(credentials_path, 'r') as f:
        for x in f.read().strip().split('\n'):
            try:
                key, value = x.split(' = ')
                os.environ[key] = value
            except ValueError:
                pass


def install_chromedriver(path):
    base_url = 'https://chromedriver.storage.googleapis.com'

    version = requests.get(base_url + '/LATEST_RELEASE').json()

    operation_systems = {
        'windows': 'win32',
        'macos': 'mac64',
        'linux': 'linux64'
    }

    chromedriver_path = os.path.join(path, 'chromedriver')
    if os.environ.get('OS') and not os.path.exists(chromedriver_path):
        output = operation_systems[os.environ.get('OS')]

        file_url = '{0}/{1}/chromedriver_{2}.zip'.format(
            base_url, version, output
        )

        z = zipfile.ZipFile(io.BytesIO(requests.get(file_url).content))
        z.extractall(path=path)

        st = os.stat(chromedriver_path)
        os.chmod(chromedriver_path, st.st_mode | 0o111)

        return chromedriver_path

    elif not os.environ.get('OS'):
        raise ValueError(
            'No OS config found in your credentials file. '
            'Please write a new line in your credentials: '
            'OS = your_operational_system'
        )

    elif os.path.exists(chromedriver_path):
        return chromedriver_path


CONFIG = os.path.join(os.path.expanduser('~'), '.tconfig')
if not os.path.exists(CONFIG):
    os.makedirs(CONFIG)

credentials = os.path.join(CONFIG, 'credentials')
if not os.path.exists(credentials):
    create_credentials(credentials)

credentials_to_environ(credentials)

CHROMEDRIVER_PATH = install_chromedriver(CONFIG)
