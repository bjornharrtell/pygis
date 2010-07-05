import pygtk
pygtk.require('2.0')
import gtk
from gtk import gdk

import cairo

import mapnik

"""
Map widget implemented using mapnik

TODO: Make map image generation work in a separate thread
"""
class Map(gtk.DrawingArea):

    # construct the image and map with initial values and connect to signal to handle resizes
    def __init__(self):
        
        gtk.DrawingArea.__init__(self)
        
        self.add_events(gtk.gdk.KEY_PRESS_MASK |
              gtk.gdk.POINTER_MOTION_MASK |
              gtk.gdk.BUTTON_PRESS_MASK |
              gtk.gdk.BUTTON_RELEASE_MASK)

        self.prevenvelope = mapnik.Envelope()
        self.prevwidth = 0
        self.prevheight = 0
        
        self.width = 400
        self.height = 214
        self.dx = 0
        self.dy = 0

        self.drag = False
        
        self.map = mapnik.Map(self.width, self.height, '+proj=latlong +datum=WGS84')
        self.map.background = mapnik.Color('steelblue')

        self.createstyle()
        
        self.map.zoom_all()
        self.map.zoom(0.2)
        self.envelope = self.map.envelope()

        self.connect("expose_event", self.expose)
        self.connect("motion_notify_event", self.motionnotify)
        #self.connect("key-press-event", self.keypress)
        self.connect("button-press-event", self.buttonpress)
        self.connect("button-release-event", self.buttonrelease)
        
    def expose(self, widget, event):
        self.context = widget.window.cairo_create()

        self.resize(event.area)
        self.renderagg(self.context)

    def motionnotify(self, widget, event):
        if self.drag == True:
            self.dx = event.x - self.x
            self.dy = event.y - self.y
            self.window.invalidate_rect(None, True)
    
    def keypress(self, widget):
        print "Not implemented"
        
    def buttonpress(self, widget, event):
        if event.button == 1:
            self.x = event.x
            self.y = event.y
            self.drag = True
        
    def unitperpixel(self):
        unitwidth = self.envelope.maxx - self.envelope.minx
        unitperpixel = unitwidth / self.map.width
        return unitperpixel
    
    def buttonrelease(self, widget, event):
        if event.button == 1:
            self.drag = False

            minx = self.envelope.minx - self.dx * self.unitperpixel()
            maxx = self.envelope.maxx - self.dx * self.unitperpixel()
            miny = self.envelope.miny + self.dy * self.unitperpixel()
            maxy = self.envelope.maxy + self.dy * self.unitperpixel()
            self.envelope = mapnik.Envelope(minx, miny, maxx, maxy)
            
            self.map.zoom_to_box(self.envelope)
            self.dx = 0
            self.dy = 0
            self.window.invalidate_rect(None, True)

    # resize the map by zooming to the new dimension then call render
    def resize(self, rectangle):
        if self.width == rectangle.width and self.height == rectangle.height: return
        
        dx = rectangle.width - self.width
        dy = rectangle.height - self.height
        
        minx = self.envelope.minx
        maxx = self.envelope.maxx + dx * self.unitperpixel()
        miny = self.envelope.miny - dy * self.unitperpixel()
        maxy = self.envelope.maxy
        
        self.envelope = mapnik.Envelope(minx, miny, maxx, maxy)
        
        self.width = rectangle.width
        self.height = rectangle.height
        
        self.map.width = self.width
        self.map.height = self.height
        self.map.zoom_to_box(self.envelope)
        self.envelope = self.map.envelope()
        
    def zoomin(self):
        self.map.zoom(0.5)
        self.envelope = self.map.envelope()
        self.window.invalidate_rect(None, True)
    
    # render the map into context at specified rectangle
    # assumes that the context is clipped to 0,0 pixel origin
    def rendermaprectangle(self, context, rectangle):
        self.map.width = rectangle.width
        self.map.height = rectangle.height
        
        minx = self.envelope.minx + rectangle.x * self.unitperpixel()
        maxx = self.envelope.minx + rectangle.width * self.unitperpixel()
        miny = self.envelope.miny + rectangle.y * self.unitperpixel()
        maxy = self.envelope.miny + rectangle.height * self.unitperpixel()
        self.envelope = mapnik.Envelope(minx, miny, maxx, maxy)
        
        self.map.zoom_to_box(self.envelope)
        
        self.renderagg(context)
        
    # render using mapnik Cairo renderar
    def rendercairo(self, context):
        mapnik.render(self.map, context, 0, 0)
        
    # render using mapnik AGG renderer
    def renderagg(self, context):
        if self.map.width != self.prevwidth or self.map.height != self.prevheight or self.envelope != self.prevenvelope:
            aggimage = mapnik.Image(self.map.width, self.map.height)
            mapnik.render(self.map, aggimage, 0, 0)
            data = aggimage.tostring()
            self.pixbuf = gtk.gdk.pixbuf_new_from_data(data, gtk.gdk.COLORSPACE_RGB, True, 8, self.map.width, self.map.height, self.map.width * 4)

        context.set_source_pixbuf(self.pixbuf, self.dx, self.dy)
        context.paint()
        self.prevwidth = self.map.width
        self.prevheight = self.map.height
        self.prevenvelope = self.envelope
        
    # create style and layer for the map from mapnik tutorial data
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
