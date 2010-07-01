import pygtk
pygtk.require('2.0')
import gtk

class NavigationToolbar(gtk.Toolbar):
    def __init__(self):
        gtk.Toolbar.__init__(self)
        
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size("dummy.png", 24, 24)
        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        image.show()

        zoomboxtool = gtk.ToggleToolButton()
        zoomboxtool.set_label("Zoombox")
        zoomboxtool.set_icon_widget(image)
        self.insert(zoomboxtool, 0)
