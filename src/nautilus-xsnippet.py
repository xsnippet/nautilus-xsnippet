# coding: utf-8

"""
    AUTHOR: Igor Kalnitsky <igor.kalnitsky@gmail.com>
    URL: http://www.kalnitsky.org.ua/
"""

import nautilus
import pynotify
import urllib
import urllib2
import gtk
import os

class XsnippetExtension(nautilus.MenuProvider):
    """
        Nautilus extension to send files to xsnippet.tk

        Add 'Send to xsnippet.tk' item to nautilus context menu.
        Link to the snippet is copied to the clipboard and displays
        by notification.
    """

    API_URL = "http://www.xsnippet.tk/new"
    ICON = "/usr/share/pixmaps/nautilus-xsnippet.png"

    languages = {
            ".c": "C",
            ".cpp": "C++", "cxx": "C++",
            ".h": "C++", ".hpp": "C++", ".hxx": "C++",
            ".cs": "C#",
            ".java": "Java",
            ".py": "Python",
            ".sh": "Bash",
            ".html": "HTML", ".htm": "HTML",
            ".xml": "XML",
            ".css": "CSS",
            ".js": "JavaScript",
            ".php": "PHP",
            ".sql": "SQL",
            ".rb": "Ruby",
            ".conf": "Apache",
            ".cmake": "CMake",
            ".pas": "Delphi",
            ".diff": "diff",
            ".bat": "DOS",
            ".erl": "Erlang",
            ".go": "Go",
            ".hs": "Haskell",
            ".ini": "ini",
            ".lisp": "Lisp",
            ".lua": "Lua",
            ".conf": "Nginx",
            ".m": "Objective-C",
            ".pl": "Perl",
            ".scale": "Scala",
            ".sm": "Smalltalk",
            ".tex": "TeX",
            ".vbs": "VBScript",
            ".vhdl": "VHDL",
            ".txt": "Text",
    }

    def __init__(self):
        pynotify.init("nautilus-xsnippet")
        self.clipboard = gtk.clipboard_get()

    def sendFile(self, filename):
        """
            Send file to xsnippet.tk and return link to last one.
            Return 'None' if error occured.
        """

        language = "Autodetection"
        title = os.path.basename(filename)
        extension = os.path.splitext(filename)[1]
        if extension in XsnippetExtension.languages:
            language = XsnippetExtension.languages[extension]

        data = {
            "title": title,
            "content": open(filename).read(),
            "language": language,
            "author": os.environ.get("USER"),
        }

        request = urllib2.Request(url=XsnippetExtension.API_URL,
                                  data=urllib.urlencode(data))
        response = urllib2.urlopen(request)

        if response.getcode() == 200:
            return response.geturl()
        return None

    def menu_click(self, menu, sourcefile):
        """
            'Send to xsnippet.tk' item handler.

            Send file to xsnippet and show notification.
        """
        title = ''
        message = ''
        snippeturl = self.sendFile(sourcefile.get_uri()[7:])

        if snippeturl is None:
            title = "Error"
            message = "Can't post file"
        else:
            title = "Posted to"
            message = snippeturl

            self.clipboard.set_text(message)
            self.clipboard.store()

        notification = pynotify.Notification(title, message,
                                             XsnippetExtension.ICON)
        notification.show()

    def get_file_items(self, window, files):
        """
            Show 'Send to xsnippet.tk' item only for 1 selected file.
        """

        if len(files) != 1 or files[0].is_directory():
            return

        item = nautilus.MenuItem(
                "XsnippetExtension::send_to_xsnippet",
                "Send to xsnippet.tk",
                "Send the current file to xsnippet.tk",
        )

        item.set_property("icon", "nautilus-xsnippet")
        item.connect("activate", self.menu_click, files[0])
        return [item]
