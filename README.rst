Nautilus Xsnippet Extension
===========================

xsnippet_ is a simple Pastebin service written in Python.

This is an extension for **Nautilus file manager**, which allows to send
files to xsnippet service via context menu.

A link to the snippet is copied to the clipboard and displays
by notification.

    **NOTE:** Version 0.2 and above works only with Nautilus 3.

Installation
------------

There are two installation ways:

1. Using ``pip``/``easy_install`` utility::

       $ sudo pip install nautilus-xsnippet

   or ::

       $ sudo easy_install nautilus-xsnippet

2. Download and uncompress tarball. For installation use a setup.py script::

       $ sudo ./setup.py install

Restart Nautilus for applying extension::

    $ nautilus -q


Dependencies
------------

Dependencies that must be meet:

- ``Pygments``::

      $ sudo pip install Pygments

- ``python-nautilus`` and ``libnautilus-extension1``::

      $ sudo aptitude install python-nautilus libnautilus-extension1


Meta
----

- Author: Igor Kalnitsky <igor@kalnitsky.org>
- License: GNU GPL v3
- Version: 0.2.3

.. _xsnippet: http://xsnippet.org/
