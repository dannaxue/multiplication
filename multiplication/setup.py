#!/usr/bin/env python
"""Setup script for installing multiplication."""

from setuptools import setup 

config = {
    'name': 'multiplication',
    'version': '0.0.1',
    'description': 'GUI',
    'author': 'Danna Xue',
    'author email': 'dannaxue@stanford.edu',
    'url': 'https://github.com/dannaxue/multiplication.git',
    'download_url': 'https://github.com/dannaxue/multiplication',
    'license': 'MIT',
    'packages': ['multiplication'],
    'scripts': ['bin/multiplication'],
    'include_package_data': True,
    # 'package_data': {'multiplication': ['icons/*.png', 'icons/*.gif', 'stylesheet.css']}
}

setup(**config)
