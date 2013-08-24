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

import threading, re
from cwebview import CWebView
from __logging import Logger


class CWebBrowser(threading.Thread):
    loaded = False
    innerBody = None
    innerHead = None

    def __init__(self, url):
        threading.Thread.__init__(self)
        self.logger = Logger.getLogger()
        self.url = url
        pattern = re.compile(r"://(.*?)/")
        matched = pattern.findall(url)
        assert matched, url + " Contains No Validated Domain"

        domain = matched[0].split(":")
        self.domain = domain[0]
        self.webview = CWebView()

    # not implements
    def set_timeout(self, timeout):
        pass

    def add_cookie(self, name, value):
        self.logger.debug("Cookie Add TO " + self.domain + " " + name + " " + value)
        self.webview.add_cookie(name, value, self.domain)
        pass

    def run(self):
        self.webview.connect("load-finished", self.load_finished)
        self.webview.connect("load-error", self.load_error)
        self.webview.open(self.url)
        self.logger.debug(self.url + " Now Loading ")

    def getResponse(self):
        class Response:
            status_code = 500
            text = None
        response = Response()
        if (self.innerBody != None):
            response.status_code = 200
        response.text = self.innerBody
        return response


    def load_error(self, view, frame, uri, userdata):
        self.logger.error("Load Error " + uri)
        self.loaded = True
        #Gtk.main_quit()();

    def load_finished(self, view, frame):
        self.logger.debug(self.url + " Load Finished ")
        self.innerHead = self.webview.get_dom_document().get_head().get_inner_html().encode("utf-8")
        self.innerBody = self.webview.get_dom_document().get_body().get_inner_html().encode("utf-8")
        self.loaded = True
        Gtk.main_quit()
