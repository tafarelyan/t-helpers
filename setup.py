from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [install.strip() for install in f]

setup(name='t-helpers',
      version='0.2.0',
      description='Tafarel personal helper tools',
      author='Tafarel Yan',
      author_email='tafarel.yan@gmail.com',
      url='https://github.com/ArrowsX/t-helpers',
      packages=find_packages(exclude=['tests*']),
      install_requires=requirements,
      scripts=['bin/tcli'],
      )
