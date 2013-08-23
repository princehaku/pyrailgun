__author__ = 'haku'

import webkit


class CWebView(webkit.WebView):
    def __init__(self):
        webkit.WebView.__init__(self);
        self.set_settings();
        self.init_signals();

    def init_signals(self):
        self.connect("console-message", self._javascript_console_message)

    def _javascript_console_message(self, view, page, msg, udata):
        return True

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

