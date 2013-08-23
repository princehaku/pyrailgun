__author__ = 'haku'

from cwebbrowser.CWebBrowser import CWebBrowser



def main():
    import gtk
    gtk.gdk.threads_init()
    web = CWebBrowser();
    web.open("http://www.baidu.com/zxc");
    web.start();
    gtk.threads_enter()
    gtk.main()

    print web.getResponse()

if __name__ == '__main__':
    main()