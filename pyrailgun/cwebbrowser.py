#    coding: UTF-8
#    User: haku
#    Date: 13-10-6
#    Time: 13:49
#

from logger import Logger
import time

from PyQt4.QtCore import QUrl, Qt
from PyQt4.QtGui import QApplication
from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtNetwork import QNetworkRequest
from PyQt4.QtWebKit import QWebPage, QWebView, QWebSettings

app = QApplication(['dummy'])


class Timeout(Exception):
    """A timeout (usually on page load) has been reached."""


class CWebBrowser():
    def _events_loop(self, wait=0.01):
        self.application.processEvents()
        time.sleep(wait)


    def __init__(self):

        self.application = app
        self.logger = Logger.getLogger()

        wp = QWebPage()
        wp.setForwardUnsupportedContent(True)
        wp.loadFinished.connect(self._on_load_finished)
        wp.loadStarted.connect(self._on_load_started)
        self.webpage = wp
        self.webframe = wp.mainFrame()
        self.headers = []
        self._load_timeout = -1
        self._load_success = False
        self.setSettings()

    def setSettings(self):
        page = self.webpage
        page.settings().setAttribute(QWebSettings.LocalStorageDatabaseEnabled, True)
        page.settings().setAttribute(QWebSettings.JavascriptCanOpenWindows, True)
        # auto disable image download
        page.settings().setAttribute(QWebSettings.AutoLoadImages, False)

    def _on_load_started(self):
        self._load_success = False
        self._load_last = 0
        self.logger.debug("Page Load Started")

    def _on_load_finished(self):
        self._load_success = True
        self.logger.debug("Page Load Finished " + unicode((self.webframe.url().toString())))

    def make_request(self, url):
        url = QUrl(url)
        req = QNetworkRequest(url)
        for header in self.headers:
            val = self.headers[header]
            req.setRawHeader(header, val)
        return req


    def setHeaders(self, headers):
        self.headers = headers

    def load(self, url, headers=None, body=None, load_timeout=-1, delay=None):
        if not headers:
            self.headers = []
        if not body:
            body = ""
            # ass headers
        req = self.make_request(url)
        self._load_success = False
        self._load_timeout = load_timeout

        self.webframe.load(req, QNetworkAccessManager.GetOperation, body)
        # wait to load finished
        self._wait_finish()
        # delay wait to render html
        if delay:
            self.wait_delays(delay)

    def _wait_finish(self):
        while not self._load_success:
            self._events_loop()
            self._load_last += 1
            if self._load_timeout > 0 and self._load_last >= self._load_timeout * 100:
                raise Timeout("Timeout reached: %d seconds" % self._load_timeout)

    def wait_delays(self, seconds):

        for j in range(1, seconds):
            for i in range(1, 100):
                # wait to load finished
                self._wait_finish()
                self._events_loop()

    def html(self):
        return unicode(self.webframe.toHtml())


    def show(self):
        self.webview = QWebView()
        self.webview.setPage(self.webpage)
        window = self.webview.window()
        window.setAttribute(Qt.WA_DeleteOnClose)
        self.application.syncX()
        self.webview.show()

    def close(self):
        pass
