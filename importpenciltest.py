#!/usr/bin/env python
import sys, os.path
sys.path.append('/usr/share/inkscape/extensions')
import inkex
from simplestyle import *

class ImportPenciltest(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('--fromframe', action = 'store',
         				type = 'int', dest = 'fromframe', default = '1',
          				help = 'From frame #')
        self.OptionParser.add_option('--toframe', action = 'store',
          				type = 'int', dest = 'toframe', default = '10',
          				help = 'From frame #')
	self.OptionParser.add_option('--filename', action = 'store',
	  				type = 'string', dest = 'filename', default = 'frame',
	  				help = 'Base file name')
	self.OptionParser.add_option('--filetype', action = 'store',
	  				type = 'string', dest = 'filetype', default = '.png',
	  				help = 'Base file name')
	self.OptionParser.add_option('--svgw', action = 'store',
	  				type = 'int', dest = 'svgw', default = '560',
	  				help = 'SVG Document Width')
	self.OptionParser.add_option('--svgh', action = 'store',
	  				type = 'int', dest = 'svgh', default = '316',
	  				help = 'SVG Document Height')
        self.OptionParser.add_option("--tab",
                                        action="store", type="string", 
                                        dest="tab", default="Frames",
                                        help="The selected UI-tab when OK was pressed")
	self.OptionParser.add_option('--bgcolor', action = 'store',
	  				type = 'string', dest = 'bgcolor', default = 0,
	  				help = 'Frame background color')

    def unsignedLong(self, signedLongString):
	longColor = long(signedLongString)
	if longColor < 0:
	 longColor = longColor & 0xFFFFFFFF
	return longColor

	#A*256^0 + B*256^1 + G*256^2 + R*256^3
    def getColorString(self, longColor):
	longColor = self.unsignedLong(longColor)
	hexColor = hex(longColor)[2:-3]
	hexColor = hexColor.rjust(6, '0')
	return '#' + hexColor.upper()

    def effect(self):
        fromframe = self.options.fromframe
        toframe = self.options.toframe+1
	filename = self.options.filename
	filetype = self.options.filetype
	svgw = self.options.svgw
	svgh = self.options.svgh
	bgcolor = self.getColorString(self.options.bgcolor)

        svg = self.document.getroot()
        # or alternatively
        # svg = self.document.xpath('//svg:svg',namespaces=inkex.NSS)[0]

	#set svg document dimensions
	svg.set('width', '%s' % (svgw))
	svg.set('height', '%s' % (svgh))

        width  = inkex.unittouu(svg.get('width'))
        height = inkex.unittouu(svg.attrib['height'])
	
	for r in range(fromframe, toframe):
	 i = format(r, '03d')
         # Create a new layer.
         layer = inkex.etree.SubElement(svg, 'g')
         layer.set(inkex.addNS('label', 'inkscape'), '%s' % (i))
         layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
	 layer.set(inkex.addNS('id'), '%s' % (i))
	 layer.set('style', 'display:none')
	
	# Create ink, paint, and pencil layers.
	 background = inkex.etree.SubElement(self.getElementById('%s' % (i)), 'g')
	 background.set(inkex.addNS('label', 'inkscape'), 'background')
	 background.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
	 background.set(inkex.addNS('insensitive', 'sodipodi'), 'true')
	 background.set(inkex.addNS('id'), 'bg%s' % (i))
	 bgfill = inkex.etree.SubElement(self.getElementById('bg%s' % (i)), 'rect')
	 bgfill.set('width', '%s' % (width))
	 bgfill.set('height', '%s' % (height))
	 bgfill.set('style', 'fill:%s' % (bgcolor))
	 bgfill.set(inkex.addNS('id'), 'bgfill%s' % (i))
	 pencil = inkex.etree.SubElement(self.getElementById('%s' % (i)), 'g')
	 pencil.set(inkex.addNS('label', 'inkscape'), 'pencil')
	 pencil.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
	 pencil.set('style', 'opacity:0.4')
	 pencil.set(inkex.addNS('insensitive', 'sodipodi'), 'true')
	 pencil.set(inkex.addNS('id'), 'pencil%s' % (i))
	 pimage = inkex.etree.SubElement(self.getElementById('pencil%s' % (i)), inkex.addNS('image','svg'))
	 pimage.set(inkex.addNS('href','xlink'), '%s%s%s' % (filename,i,filetype))
	 pimage.set(inkex.addNS('id'), 'pimage%s' % (i))
	 paint = inkex.etree.SubElement(self.getElementById('%s' % (i)), 'g')
	 paint.set(inkex.addNS('label', 'inkscape'), 'paint')
	 paint.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
	 paint.set(inkex.addNS('id'), 'paint%s' % (i))
	 ink = inkex.etree.SubElement(self.getElementById('%s' % (i)), 'g')
	 ink.set(inkex.addNS('label', 'inkscape'), 'ink')
	 ink.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
	 ink.set(inkex.addNS('id'), 'ink%s' % (i))

# Create effect instance and apply it.
effect = ImportPenciltest()
effect.affect()

