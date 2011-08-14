import pygtk
pygtk.require('2.0')
import gtk
import glib
import webkit
import Queue
import threading

import captchatrader
HTMLLOADINGPAGE = """<html><body>Loading: <span id=\"loading\">%s</span><script>setInterval(function() {var nume = document.getElementById('loading'); nume.innerHTML = ( parseInt(nume.innerHTML) != 0 ? parseInt(nume.innerHTML) - 1 : 0);}, 1000);</script></body></html>
"""
class GtkRunner(threading.Thread):
    '''run *func* in a thread with *args* and *kwargs* as arguments, when
    finished call callback with a two item tuple containing a boolean as first
    item informing if the function returned correctly and the returned value or
    the exception thrown as second item
    '''

    def __init__(self, callback, func, *args, **kwargs):
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.callback = callback
        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.result = Queue.Queue()

        self.start()
        glib.timeout_add_seconds(1, self.check)

    def run(self):
        '''
        main function of the thread, run func with args and kwargs
        and get the result, call callback with the (True, result)

        if an exception is thrown call callback with (False, exception)
        '''
        try:
            result = (True, self.func(*self.args, **self.kwargs))
        except Exception, ex:
            result = (False, ex)

        self.result.put(result)

    def check(self):
        '''
        check if func finished
        '''
        try:
            result = self.result.get(False, 0.1)
        except Queue.Empty:
            return True

        self.callback(result)
        return False

class window(gtk.Window):
    def __init__(self, ct):
        self.ct = ct
        gtk.Window.__init__(self)
        self.set_default_size(400, 100)
        self.set_keep_above(True)
        self.stick()
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_skip_taskbar_hint(True)

        box = gtk.VBox()
        self.add(box)

        self.webview = webkit.WebView()
        box.pack_start(self.webview)
        self.webview.load_string('<html><body></body></html>', 'text/html', 'UTF-8','/')

        label = gtk.Label('Enter captcha (leave blank to skip)')
        box.pack_start(label)

        self.entry = gtk.Entry()
        self.entry.set_text('Loading')
        self.entry.connect('activate', self.onSubmit)
        box.pack_start(self.entry)

        hbox = gtk.HBox()
        box.pack_start(hbox)

        hbox.pack_start(gtk.Label('Wait/timeout:'))
        self.label = gtk.Label('')
        hbox.pack_start(self.label)

        exitbutton = gtk.Button('Exit')
        exitbutton.connect('clicked', self.onExit)
        box.pack_start(exitbutton)

#        GtkRunner(lambda *x: x, self.loadImage)
        GtkRunner(lambda x: self.webview.load_string('<html><body><img src="%s"/></body></html>' % x[1][1], 'text/html', 'UTF-8','/'), self.ct.enqueue)
        GtkRunner(lambda x: self.webview.load_string(HTMLLOADINGPAGE % x[1][2], 'text/html', 'UTF-8','/'), self.ct.getWaitTime )
        glib.timeout_add_seconds(2, lambda *x: GtkRunner(lambda x: self.label.set_text(str(x[1][2])), self.ct.getWaitTime ) )

    def loadImage(self):
        self.__loadImage(self.ct.enqueue()[1])

    def __loadImage(self, imagedata):
        print imagedata
        self.webView.load_string('<html><body><img src="%s"/></body></html>' % imagedata, 'text/html', 'UTF-8','/')
        self.entry.set_text('')
        self.execute_script('oldtitle=document.title;document.title=document.documentElement.innerHTML;')
        html = self.get_main_frame().get_title()
        print html

    def onSubmit(self, entry, *args):
        text = entry.get_text()
        if text == '':
            GtkRunner(lambda *x: x, self.ct.dequeue)
        else:
            GtkRunner(lambda *x: x, self.ct.answer, text)
        entry.set_text()
        GtkRunner(lambda x: self.webview.load_string(HTMLLOADINGPAGE % x[1][2], 'text/html', 'UTF-8','/'), self.ct.getWaitTime )
        GtkRunner(lambda x: self.webview.load_string('<html><body><img src="%s"/></body></html>' % x[1][1], 'text/html', 'UTF-8','/'), self.ct.enqueue)

    def onExit(self, button, *args):
        self.hide()
        self.ct.dequeue()
        gtk.main_quit()
        exit()


if __name__ == "__main__":
    user = raw_input('User:')
    passw = raw_input('Password:')
    ct = captchatrader.captchatrader()
    ct.login(user, passw)
#    gtk.gdk.threads_init()
    win = window(ct)
    win.show_all()
    gtk.main()
