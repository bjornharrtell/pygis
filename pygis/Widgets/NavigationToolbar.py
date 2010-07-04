import pygtk
pygtk.require('2.0')
import gtk

class NavigationToolbar(gtk.Toolbar):
    def __init__(self, map):
        gtk.Toolbar.__init__(self)
        
        self.map = map
        
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size("dummy.png", 24, 24)
        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        image.show()
        image2 = gtk.Image()
        image2.set_from_pixbuf(pixbuf)
        image2.show()
        
        zoomin = gtk.ToolButton()
        zoomin.set_label("Zoom in")
        zoomin.set_icon_widget(image)
        self.insert(zoomin, 0)
        
        zoomin.connect("clicked", self.clicked)

        zoomboxtool = gtk.ToggleToolButton()
        zoomboxtool.set_label("Zoombox")
        zoomboxtool.set_icon_widget(image2)
        #self.insert(zoomboxtool, 1)

    def clicked(self, toolbutton):
        self.map.zoomin()