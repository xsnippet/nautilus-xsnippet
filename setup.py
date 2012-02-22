#!/usr/bin/env python
# coding: utf-8
from os import getenv, path
from distutils.core import setup

USER_HOME = getenv('HOME')
PROJECT_DIR = path.dirname(__file__)

data = [
    (path.join(USER_HOME, '.local', 'share', 'nautilus-python', 'extensions'),
     [path.join(PROJECT_DIR, 'src', 'nautilus-xsnippet.py')]),

    ('/usr/share/pixmaps/',
     [path.join(PROJECT_DIR, 'src', 'pixmaps', 'nautilus-xsnippet.png')]),
]

setup(
    name='nautilus-xsnippet',
    version='0.2.2',
    description='Nautilus Xsnippet Extension',
    long_description=open('README.rst').read(),
    author='Igor Kalnitsky',
    author_email='igor@kalnitsky.org',
    url='http://www.kalnitsky.org/',
    license='GPL-3',
    keywords=['nautilus', 'xsnippet', 'extension'],
    data_files=data,
    install_requires=['poster>=0.8.1', ],
    platforms=['Linux'],
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Topic :: Desktop Environment :: File Managers",
        "Topic :: Desktop Environment :: Gnome",
        "Environment :: Plugins",
    ],
)
