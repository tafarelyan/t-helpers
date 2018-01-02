from setuptools import setup, find_packages


setup(name='t-helpers',
      version='0.1.2',
      description='Tafarel personal helper tools',
      author='Tafarel Yan',
      author_email='tafarel.yan@gmail.com',
      url='https://github.com/ArrowsX/t-helpers',
      packages=find_packages(exclude=['tests*']),
      scripts=['bin/tcli'],
      )
