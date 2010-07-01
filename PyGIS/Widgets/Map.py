import pygtk
pygtk.require('2.0')
import gtk
import mapnik

"""
Map widget implemented using mapnik
"""
class Map(gtk.Image):

    """
    Construct the image and map with initial values and connect to signal to handle resizes
    """
    def __init__(self):
        gtk.Image.__init__(self)

        self.width = 1
        self.height = 1
        
        self.map = mapnik.Map(self.width, self.height, '+proj=latlong +datum=WGS84')
        self.map.background = mapnik.Color('steelblue')

        self.createstyle()
        self.rendermap()

    """
    Resize the map by zooming to the new dimensions then call render
    """
    def resize(self, rectangle):
        if self.width == rectangle.width and self.height == rectangle.height: return
        
        self.width = rectangle.width
        self.height = rectangle.height
        self.map.width = self.width
        self.map.height = self.height
        
        self.map.zoom_to_box(self.lyr.envelope())
        
        self.rendermap()
    
    """
    Render a mapnik image and convert to gtk.Image
    """
    def rendermap(self):
        aggimage = mapnik.Image(self.map.width, self.map.height)
        mapnik.render(self.map, aggimage, 0, 0)
        data = aggimage.tostring()
        pixbuf = gtk.gdk.pixbuf_new_from_data(data, gtk.gdk.COLORSPACE_RGB, True, 8, self.map.width, self.map.height, self.map.width * 4)
        self.set_from_pixbuf(pixbuf)
    
    """
    Create style and layer for the map from mapnik tutorial data
    """
    def createstyle(self):
        s = mapnik.Style()
        r = mapnik.Rule()
        r.symbols.append(mapnik.PolygonSymbolizer(mapnik.Color('#f2eff9')))
        r.symbols.append(mapnik.LineSymbolizer(mapnik.Color('rgb(50%,50%,50%)'),0.1))
        s.rules.append(r)
        self.map.append_style('My Style',s)

        self.lyr = mapnik.Layer('world',"+proj=latlong +datum=WGS84")
        self.lyr.datasource = mapnik.Shapefile(file='world_borders')
        self.lyr.styles.append('My Style')
        
        self.map.layers.append(self.lyr)
        self.map.zoom_to_box(self.lyr.envelope())
