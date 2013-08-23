#    coding: UTF-8
#    User: haku
#    Date: 13-8-24
#    Time: 上午1:52
#
__author__ = 'haku'

import webkit, ctypes

try:
    libwebkit = ctypes.CDLL('libwebkitgtk-1.0.so.0')
except:
    try:
        libwebkit = ctypes.CDLL('libwebkit-1.0.so.2')
    except:
        libwebkit = ctypes.CDLL('libwebkitgtk-1.0.so')

libgobject = ctypes.CDLL('libgobject-2.0.so.0')
libsoup = ctypes.CDLL('libsoup-2.4.so.1')


class CWebView(webkit.WebView):
    def __init__(self):
        webkit.WebView.__init__(self);
        self.set_settings();
        self.init_signals();
        self.init_cookie();

    def add_cookie(self, name, value, domain):
        soup_cookie = libsoup.soup_cookie_new(name.encode("ascii"), value.encode("utf-8"), domain.encode("utf-8"), "/")
        libsoup.soup_cookie_jar_add_cookie(self.soup_cookie, soup_cookie)

    def init_cookie(self):
        session = libwebkit.webkit_get_default_session()
        #soup_cookie = libsoup.soup_cookie_jar_new()
        soup_cookie = libsoup.soup_cookie_jar_text_new("./cookie.txt", False)
        libgobject.g_object_set(session, 'add-feature', soup_cookie, None)
        self.soup_cookie = soup_cookie

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

