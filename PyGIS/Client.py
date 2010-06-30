import pygtk
pygtk.require('2.0')
import gtk

from PyGIS.Widgets.Mapnik import Mapnik

class Client(object):

    def __init__(self):
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        
        self.layout = gtk.Layout()
        self.window.add(self.layout)
        
        self.mapnik = Mapnik()
        self.layout.add(self.mapnik)

        self.window.show_all()
        
        self.window.connect("size-allocate", self.onsizeallocate)

    def onsizeallocate(self, widget, allocation):
        self.mapnik.resize(allocation)

    def destroy(self, widget):
        gtk.main_quit()

    def main(self):
        gtk.main()
        
if __name__ == "__main__":
    client = Client()
    client.main()
