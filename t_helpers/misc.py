import os
import io
import stat
import zipfile

import requests


def create_credentials(credentials_path):
    print('You don\'t have a credentials file yet')
    print('Creating {}...'.format(credentials_path))

    with open(credentials_path, 'w') as f:
        os = input('Which OS (Windows/MacOS/Linux)? ')
        if os:
            f.write('OS = {}\n'.format(os.lower()))
        else:
            f.write('OS = linux\n')

        pb_key = input('Insert PushBullet API KEY: ')
        if pb_key:
            f.write('PUSH_BULLET_API_TOKEN = {}\n'.format(pb_key))

        spt_key = input('Insert SPTrans API KEY: ')
        if spt_key:
            f.write('SPTRANS_API_TOKEN = {}\n'.format(spt_key))

def credentials_to_environ(credentials_path):
    with open(credentials_path, 'r') as f:
        for x in f.read().strip().split('\n'):
            key, value = x.split(' = ')
            os.environ[key] = value

def install_chromedriver(path=None):
    base_url = 'https://chromedriver.storage.googleapis.com'

    version = requests.get(base_url + '/LATEST_RELEASE').json()

    output = {
        'windows': 'win32',
        'macos': 'mac64',
        'linux': 'linux64'
    }[os.environ['OS']]

    file_url = '{0}/{1}/chromedriver_{2}.zip'.format(base_url, version, output)

    z = zipfile.ZipFile(io.BytesIO(requests.get(file_url).content))
    z.extractall(path=path)

    chromepath = os.path.join(path, 'chromedriver')
    st = os.stat(chromepath)
    os.chmod(chromepath, st.st_mode | 0o111)
