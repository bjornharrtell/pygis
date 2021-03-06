import pygtk
pygtk.require('2.0')
import gtk

from pygis.Widgets.Map import Map
from pygis.Widgets.NavigationToolbar import NavigationToolbar

"""
Client application implemented upon a gtk.Window
"""
class Client(gtk.Window):

    def __init__(self, windowtype):
        gtk.Window.__init__(self, windowtype)
        
        # needed to make it possible to resize to smaller size
        self.set_geometry_hints(min_width=400, min_height=300)
        
        self.connect("destroy", self.destroy)
        
        self.map = Map()
        
        vbox = gtk.VBox()
        self.add(vbox)

        menubar = gtk.MenuBar()
        vbox.pack_start(menubar, False, False, 0)
        
        handlebox = gtk.HandleBox()
        navbar = NavigationToolbar(self.map)
        handlebox.add(navbar)
        vbox.pack_start(handlebox, False, False, 0)
        
        menuitemfile = gtk.MenuItem(label="File")
        menubar.add(menuitemfile)
        
        menu = gtk.Menu()
        menuitemfile.set_submenu(menu)
        
        menuitemquit = gtk.MenuItem(label="Quit")
        menu.attach(menuitemquit, 0, 1, 0, 1)
        menuitemquit.connect("activate", self.destroy)
        
        self.hbox = gtk.HBox()
        vbox.pack_start(self.hbox, True, True, 0)
        
        self.hbox.add(self.map)
        self.hbox.connect("size-allocate", self.onsizeallocate)
        
        self.statusbar = gtk.Statusbar()
        vbox.pack_end(self.statusbar, False, False, 0)

        self.show_all()

    def onsizeallocate(self, widget, event):
        #print "size-allocate: ", widget.allocation
        self.statusbar.push(0, "Map image dimension: " + str(widget.allocation))
                
    def destroy(self, widget):
        gtk.main_quit()

    def main(self):
        gtk.main()
        
if __name__ == "__main__":
    client = Client(gtk.WINDOW_TOPLEVEL)
    client.main()
