import pygtk
pygtk.require('2.0')
import gtk

from PyGIS.Widgets.Map import Map

"""
Client application implemented upon a gtk.Window
"""
class Client(gtk.Window):

    def __init__(self, windowtype):
        gtk.Window.__init__(self, windowtype)
        
        # needed to make it possible to resize to smaller size
        self.set_geometry_hints(min_width=1, min_height=1)
        
        self.connect("destroy", self.destroy)

        mapnik = Map()
        self.add(mapnik)

        self.show_all()
        
    def destroy(self, widget):
        gtk.main_quit()

    def main(self):
        gtk.main()
        
if __name__ == "__main__":
    client = Client(gtk.WINDOW_TOPLEVEL)
    client.main()
