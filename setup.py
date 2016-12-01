try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'launchpad-presence-tracker',
    'description': 'The client for a presence tracker system. The client processes device activities, encodes the information and pushes it to the server.',
    'author': 'Jonas Spinner',
    'url': 'https://github.com/pioniergarage/launchpad-presence-tracker',
    'download_url': 'https://github.com/pioniergarage/launchpad-presence-tracker.git',
    'version': '0.1',
    'packages': ['apscheduler>=3.3.0'],
    'scripts': []
}

setup(**config)
