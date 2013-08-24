#    coding: UTF-8
#    User: haku
#    Date: 13-8-24
#    Time: 上午1:52
#
__author__ = 'haku'

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import WebKit
from gi.repository import Soup

import sys

class CWebView(WebKit.WebView):
    def __init__(self):
        WebKit.WebView.__init__(self);
        self.set_settings();
        self.init_signals();
        self.init_cookie();

    def add_cookie(self, name, value, domain):

        n_cookie = Soup.Cookie.new(name.encode("utf-8"), value.encode("utf-8"), domain.encode("utf-8"), "/", sys.maxint - 100)
        self.soup_cookie.add_cookie(n_cookie)


    def init_cookie(self):
        self.soup_cookie = Soup.CookieJar.new()
        self.soup_cookie.set_accept_policy(Soup.CookieJarAcceptPolicy.ALWAYS)
        session = WebKit.get_default_session()
        session.add_feature(self.soup_cookie)


    def init_signals(self):
        self.connect("console-message", self._javascript_console_message)

    # ignore console js message
    def _javascript_console_message(self, view, page, msg, udata):
        return True

    # some basic settings
    def set_settings(self):
        settings = self.get_settings()
        settings.set_property("auto-resize-window", False)
        settings.set_property("auto-load-images", False)
        settings.set_property("enable-developer-extras", True)
        settings.set_property('enable-universal-access-from-file-uris', True)
        settings.set_property('enable-file-access-from-file-uris', True)
        settings.set_property('enable-page-cache', True)
        settings.set_property('javascript-can-open-windows-automatically', True)
        settings.set_property('enable-spatial-navigation', True)
        settings.set_property('javascript-can-access-clipboard', True)
        settings.set_property('enable-site-specific-quirks', True)
        settings.set_property('user-agent',
                              'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:17.0) Gecko/20100101 Firefox/17.0')

