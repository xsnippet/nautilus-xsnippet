# coding: utf-8

"""
    AUTHOR: Igor Kalnitsky <igor@kalnitsky.org>
    URL: http://www.kalnitsky.org/
"""

import os
import urllib2

from gi.repository import Nautilus, GObject, Gtk, Gdk, GdkPixbuf, Notify

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


class XsnippetExtension(GObject.GObject, Nautilus.MenuProvider):
    """
        Nautilus extension to send files to xsnippet.org

        Add 'Send to xsnippet.org' item to nautilus context menu.
        Link to the snippet is copied to the clipboard and displays
        by notification.
    """

    API_URL = "http://www.xsnippet.org/new"
    ICON = "/usr/share/pixmaps/nautilus-xsnippet.png"

    def __init__(self):
        try:
            factory = Gtk.IconFactory()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(XsnippetExtension.ICON)
            iconset = Gtk.IconSet.new_from_pixbuf(pixbuf)
            factory.add("xsnippet", iconset)
            factory.add_default()
        except:
            pass

        Notify.init("nautilus-xsnippet")
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    def sendFile(self, filename):
        """
            Send file to xsnippet.org and return link to last one.
            Return 'None' if error occured.
        """

        register_openers()
        data, headers = multipart_encode({
            "file": open(filename, "rb"),
            "author": os.environ.get("USER"),
        })

        request = urllib2.Request(XsnippetExtension.API_URL, data, headers)
        response = urllib2.urlopen(request)

        if response.getcode() == 200:
            return response.geturl()
        return None

    def menu_click(self, menu, sourcefile):
        """
            'Send to xsnippet.org' item handler.

            Send file to xsnippet and show notification.
        """
        snippeturl = self.sendFile(sourcefile.get_uri()[7:])

        if snippeturl is None:
            title = "Error"
            message = "Can't post file"
        else:
            title = "Posted to"
            message = snippeturl + '\n[the link is copied to clipboard]'

            self.clipboard.set_text(message, -1)
            self.clipboard.store()

        notification = Notify.Notification.new(title, message,
            XsnippetExtension.ICON)
        notification.show()

    def get_file_items(self, window, files):
        """
            Show 'Send to xsnippet.org' item only for 1 selected file.
        """

        if len(files) != 1 or files[0].is_directory():
            return

        item = Nautilus.MenuItem(
                name="XsnippetExtension::send_to_xsnippet",
                label="Send to xsnippet.org",
                tip="Send the current file to xsnippet.org",
                icon="xsnippet"
        )

        item.connect("activate", self.menu_click, files[0])
        return [item]

    def __del__(self):
        Notify.uninit()
