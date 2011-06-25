#!/usr/bin/env python
# coding: utf-8

import os
from distutils.core import setup

root = os.path.dirname(__file__)

data = [
    ('/usr/lib/nautilus/extensions-2.0/python',
     [os.path.join(root, 'src/nautilus-xsnippet.py')]),

    ('/usr/share/pixmaps/',
     [os.path.join(root, 'src/pixmaps/nautilus-xsnippet.png')]),
]

setup(
    name='nautilus-xsnippet',
    description='Nautilus Xsnippet Extension',
    long_description=open('README').read(),
    version='0.1.3',
    author='Igor Kalnitsky',
    author_email='igor.kalnitsky@gmail.com',
    url='http://www.kalnitsky.org.ua/',
    license='GPL-3',
    platforms=['Linux'],
    keywords=['nautilus', 'xsnippet', 'extension'],
    requires=['pynotify', 'nautilus', 'gtk'],
    data_files=data,
)
