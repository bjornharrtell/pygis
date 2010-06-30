import mapnik

import pygtk
pygtk.require('2.0')
import gtk

from PyGIS.Widgets.Mapnik import Mapnik

class Client(object):

    def __init__(self):
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.show()
        
        self.mapnik = Mapnik()
        self.window.add(self.mapnik)
        self.mapnik.show()

    def main(self):
        gtk.main()
        
if __name__ == "__main__":
    client = Client()
    client.main()
