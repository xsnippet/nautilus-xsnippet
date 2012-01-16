Nautilus Xsnippet Extension
---------------------------

xsnippet_ is a simple Pastebin service written in Python.

This is an extension for **Nautilus file manager**, which allows to send
files to xsnippet service via context menu.

A link to the snippet is copied to the clipboard and displays
by notification.

Version 0.2 and above works only with Nautilus 3.

Installation
------------

There are two installation ways:

1. Using 'pip' utility:

       $ sudo pip install nautilus-xsnippet

2. Download and uncompress tarball. For installation use a setup.py script:

       $ sudo ./setup.py install

Restart Nautilus for applying extension:

    $ nautilus -q


Dependencies
------------

Dependencies that must be meet:

- poster

      $ sudo pip install poster

- python-nautilus and libnautilus-extension1

      $ sudo aptitude install python-nautilus libnautilus-extension1


Changes
-------

**0.2.0**

- Moving to GTK3. So the project works with Nautilus 3.
  *Note: Earlier versions of Nautilus were errors, so the extension 
  may not work.*

**0.1.5**

- Use new domain.
- Upload file system instead sending plain text.
- New logotype.

**0.1.4**

- Add '[the link is copied to clipboard]' to notification.

**0.1.3**

- Remove getpass module from import section.
- Pep8 verified code.


**0.1.2**

- Use filename as snippet title.
- Fix paths in setup.py.


.. _xsnippet: http://www.xsnippet.org/
