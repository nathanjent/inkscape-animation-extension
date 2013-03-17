#!/usr/bin/env python
import sys, os
sys.path.append('/usr/share/inkscape/extensions')
import inkex
from simplestyle import *

try:
    from subprocess import Popen, PIPE
    bsubprocess = True
except:
    bsubprocess = False

"""
# leftover stuff from GifAnimate extension, used gimp_xcf extension instead
class OutputFrames(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):
        infile = sys.argv[-1]

        # Get access to main SVG document element and get its dimensions.
        from xml.dom.minidom import parse, parseString
        dom = parse(infile)
        svg = dom.getElementsByTagName('svg')[0]

        layers = svg.getElementsByTagName('g')
        command = "inkscape %s -C -i '%s' -j -e /tmp/%s.png 2>&1 > /dev/null"

        layerids = []
        for l in layers:
                layerids.append(l.getAttribute('id'))

        [os.system(pngcommand % (infile, id, id)) for id in layerids if id.startswith('f')]
	if bsubprocess:
                p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
                return_code = p.wait()
                f = p.stdout
                err = p.stderr
        else:
        _, f, err = os.open3(command)
        f.close()

# Create effect instance and apply it.
effect = OutputFrames()
effect.affect()
	"""
class OutputFrames(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('--fromframe', action = 'store',
         				type = 'int', dest = 'fromframe', default = '1',
          				help = 'From frame #')
        self.OptionParser.add_option('--toframe', action = 'store',
          				type = 'int', dest = 'toframe', default = '10',
          				help = 'From frame #')
        self.OptionParser.add_option("--directory", action="store", 
                                        type="string", dest="directory",
                                        default="~/output/", help="Directory to save images to")                               
        self.OptionParser.add_option("--image", action="store", 
                                        type="string", dest="image", 
                                        default=None, help="Image name (without extension)")
        self.OptionParser.add_option("--hpencil", action="store", 
                                        type="inkbool", dest="hpencil", 
                                        default="true", help="Hide pencil sublayer during export?")

    def check_dir_exists(self, dir):
        if not os.path.isdir(dir):
            os.makedirs(dir)

    def effect(self):
        fromframe = self.options.fromframe
        toframe = self.options.toframe+1
        svg_file = self.args[-1]
        docname = self.xpathSingle('/svg:svg/@sodipodi:docname')[:-4]
	dirname = os.path.dirname(self.options.directory)
	if dirname == '' or dirname == None:
            dirname = './'
        inkex.errormsg(dirname)
        dirname = os.path.expanduser(dirname)
        dirname = os.path.expandvars(dirname)
        #self.check_dir_exists(dirname)
	image = self.options.image
	hpencil = self.options.hpencil

	for r in range(fromframe, toframe):
	    i = format(r, '03d')
	    
	    layer = self.getElementById('%s' % (i))
	    layer.set('style', 'display:inline')
	    pencil = self.getElementById('pencil%s' % (i))
	    if hpencil:
		pencil.set('style', 'display:none')
	    else:
		pencil.set('style', inkex.addNS('inline', 'display'))
	    
            filename = dirname + os.path.sep + image + i + ".png"
            command = "inkscape %s -i %s -j -C -e %s" % (svg_file, i, filename)
   	    if bsubprocess:
                p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
                return_code = p.wait()
                f = p.stdout
                err = p.stderr
            else:
                _, f, err = os.open3(command)
            f.close()

if __name__ == '__main__':
    e = OutputFrames()
    e.affect()

