from setuptools import setup, find_packages


def requirements():
    with open('requirements.txt', 'r') as requirements:
        return [install.strip() for install in requirements]

setup(name='t-helpers',
      version='0.0.7',
      description='Tafarel personal helper tools',
      author='Tafarel Yan',
      author_email='tafarel.yan@gmail.com',
      url='https://github.com/ArrowsX/t-helpers',
      packages=find_packages(exclude=['tests*']),
      install_requires=requirements(),
      scripts=['bin/tcli'],
      )
