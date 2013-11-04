try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'Data Exchange file API',
	'author': 'David J. Vine',
	'url': 'https://github.org/djvine/data_exchange',
	'author_email': 'djvine@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['data_exchange'],
	'scripts': [],
	'name': 'data_exchange'
}

setup(**config)