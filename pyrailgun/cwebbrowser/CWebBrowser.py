__author__ = 'haku'

import jswebkit
import threading
import CWebView, gtk

class Response:
    status_code = 500;
    text = None;

class CWebBrowser(threading.Thread):
    loaded = False;
    innerBody = None;
    innerHead = None;

    def __init__(self):
        threading.Thread.__init__(self);
        self.webview = CWebView.CWebView();

    def open(self, url):
        self.url = url;

    def run(self):
        self.webview.connect("load-finished", self.load_finished)
        self.webview.connect("load-error", self.load_error)
        self.webview.open(self.url)
        print self.url, " Now Loading "

    def getResponse(self):
        response = Response()
        if (self.innerBody != None):
            response.status_code = 200;

        response.text = self.innerBody;
        return response


    def load_error(self, view, frame, uri, userdata):
        print "Load Error ", uri
        self.loaded = True
        gtk.mainquit();


    def load_finished(self, view, frame):
        print "Done"
        js = jswebkit.JSContext(self.webview.get_main_frame().get_global_context())
        self.innerBody = str(js.EvaluateScript('document.body.innerHTML'))
        self.innerHead = str(js.EvaluateScript('document.head.innerHTML'))
        self.loaded = True
        gtk.mainquit();
