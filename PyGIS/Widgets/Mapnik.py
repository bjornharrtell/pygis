import pygtk
pygtk.require('2.0')
import gtk
import mapnik

class Mapnik(gtk.Image):

    def __init__(self):
        gtk.Image.__init__(self)
        
        self.connect("show", self.onshow)

    def onshow(self, widget):
        self.parent.connect("configure-event", self.onconfigure)
        self.update()
        
    def onconfigure(self, widget, allocation):
        self.update()
        
    def update(self):
        width = self.parent.allocation.width
        height = self.parent.allocation.height
        
        map = mapnik.Map(width,height,'+proj=latlong +datum=WGS84')
        map.background = mapnik.Color('steelblue')
        
        aggimage = mapnik.Image(map.width, map.height)
        mapnik.render(map, aggimage, 0, 0)
        data = aggimage.tostring()
        
        pixbuf = gtk.gdk.pixbuf_new_from_data(data, gtk.gdk.COLORSPACE_RGB, True, 8, map.width, map.height, map.width * 4)
        self.set_from_pixbuf(pixbuf)
