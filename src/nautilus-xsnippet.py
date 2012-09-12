# coding: utf-8
#
# Copyright 2012 Igor Kalnitsky
#
# This file is part of Nautilus-Xsnippet.
#
# Nautilus-Xsnippet is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Nautilus-Xsnippet is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Nautilus-Xsnippet.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import json
import urllib
import urllib2

from pygments.lexers import get_lexer_for_filename
from gi.repository import Nautilus, GObject, Gtk, Gdk, GdkPixbuf, Notify


class Xsnippet(GObject.GObject, Nautilus.MenuProvider):
    """
        Nautilus extension to send files to xsnippet.org

        Add 'Send to xsnippet.org' item to nautilus context menu.
        Link to the snippet is copied to the clipboard and displays
        by notification.
    """

    DOMAIN = "http://xsnippet.org"
    API_URL = "{domain}/api/v1/snippets/".format(domain=DOMAIN)
    ICON = "/usr/share/pixmaps/nautilus-xsnippet.png"

    def __init__(self):
        try:
            factory = Gtk.IconFactory()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(Xsnippet.ICON)
            iconset = Gtk.IconSet.new_from_pixbuf(pixbuf)
            factory.add("xsnippet", iconset)
            factory.add_default()
        except:
            pass

        Notify.init("nautilus-xsnippet")
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    @staticmethod
    def get_lang_by_filename(filename):
        try:
            aliases = get_lexer_for_filename(filename).aliases
            sname = aliases[0] if aliases else "text"
        except:
            sname = "text"
        return sname

    def send_file(self, filename):
        """
            Send file to xsnippet.org and return link to last one.
            Return 'None' if error occured.
        """
        data = {
            "title": os.path.basename(filename),
            "language": Xsnippet.get_lang_by_filename(filename),
            "content": open(filename, "rt").read(),
        }

        data = urllib.urlencode(data)
        request = urllib2.Request(Xsnippet.API_URL, data)
        response = urllib2.urlopen(request)

        if response.getcode() == 201:
            id = json.loads(response.read()).get('id')
            if id is not None:
                return '{domain}/{id}/'.format(domain=Xsnippet.DOMAIN, id=id)
        return None

    def menu_click(self, menu, sourcefile):
        """
            'Send to xsnippet.org' item handler.

            Send file to xsnippet and show notification.
        """
        snippeturl = self.send_file(sourcefile.get_uri()[7:])

        if snippeturl is None:
            title = "Error"
            message = "Can't post file"
        else:
            title = "Posted to"
            message = snippeturl + '\n[the link is copied to clipboard]'

            self.clipboard.set_text(snippeturl, -1)
            self.clipboard.store()

        notification = Notify.Notification.new(title, message, Xsnippet.ICON)
        notification.show()

    def get_file_items(self, window, files):
        """
            Show 'Send to xsnippet.org' item only for 1 selected file.
        """

        if len(files) != 1 or files[0].is_directory():
            return

        if files[0].is_mime_type('text/plain') is False:
            return

        item = Nautilus.MenuItem(
            name="Xsnippet::send_to_xsnippet",
            label="Send to xsnippet.org",
            tip="Send the current file to xsnippet.org",
            icon="nautilus-xsnippet"
        )

        item.connect("activate", self.menu_click, files[0])
        return [item]

    def __del__(self):
        Notify.uninit()
