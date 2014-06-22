#!/usr/bin/env python
import sys, os.path
sys.path.append('/usr/share/inkscape/extensions')
import inkex
from simplestyle import *

class HideLockSublayers(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('--hframe', action = 'store',
                type = 'inkbool', dest = 'hframe', default = 'false',
                help = 'Hide all frame layers')
        self.OptionParser.add_option('--lframe', action = 'store',
                type = 'inkbool', dest = 'lframe', default = 'false',
                help = 'Lock all frame layers')
        self.OptionParser.add_option('--hink', action = 'store',
                type = 'inkbool', dest = 'hink', default = 'false',
                help = 'Hide all ink sublayers')
        self.OptionParser.add_option('--link', action = 'store',
                type = 'inkbool', dest = 'link', default = 'false',
                help = 'Lock all ink sublayers')
        self.OptionParser.add_option('--hpaint', action = 'store',
                type = 'inkbool', dest = 'hpaint', default = 'false',
                help = 'Hide all paint sublayers')
        self.OptionParser.add_option('--lpaint', action = 'store',
                type = 'inkbool', dest = 'lpaint', default = 'false',
                help = 'Lock all paint sublayers')
        self.OptionParser.add_option('--hbackground', action = 'store',
                type = 'inkbool', dest = 'hbackground', default = 'false',
                help = 'Hide all background sublayers')
        self.OptionParser.add_option('--lbackground', action = 'store',
                type = 'inkbool', dest = 'lbackground', default = 'false',
                help = 'Lock all background sublayers')
        self.OptionParser.add_option('--hpencil', action = 'store',
                type = 'inkbool', dest = 'hpencil', default = 'false',
                help = 'Hide all pencil sublayers')
        self.OptionParser.add_option('--lpencil', action = 'store',
                type = 'inkbool', dest = 'lpencil', default = 'false',
                help = 'Lock all pencil sublayers')
        self.OptionParser.add_option('--fromframe', action = 'store',
                type = 'int', dest = 'fromframe', default = '1',
                help = 'From frame #')
        self.OptionParser.add_option('--toframe', action = 'store',
                type = 'int', dest = 'toframe', default = '2',
                help = 'From frame #')

    def effect(self):
        fromframe = self.options.fromframe
        toframe = self.options.toframe+1
        hframe = self.options.hframe
        lframe = self.options.lframe
        hink = self.options.hink
        link = self.options.link
        hpaint = self.options.hpaint
        lpaint = self.options.lpaint
        hbackground = self.options.hbackground
        lbackground = self.options.lbackground
        hpencil = self.options.hpencil
        lpencil = self.options.lpencil
        
        for r in range(fromframe, toframe):
            i = format(r, '03d')
            layer = self.getElementById('%s' % (i))
            if lframe:
                layer.set(inkex.addNS('insensitive', 'sodipodi'), 'true')
            else:
                try:
                    del layer.attrib[inkex.addNS('insensitive', 'sodipodi')]
                except KeyError:
                    pass
            if hframe:
                layer.set('style', 'display:none')
            else:
                layer.set('style', 'display:inline')
            ink = self.getElementById('ink%s' % (i))
            if link:
                ink.set(inkex.addNS('insensitive', 'sodipodi'), 'true')
            else:
                try:
                    del ink.attrib[inkex.addNS('insensitive', 'sodipodi')]
                except KeyError:
                    pass
            if hink:
                ink.set('style', 'display:none')
            else:
                ink.set('style', 'display:inline')
            paint = self.getElementById('paint%s' % (i))
            if lpaint:
                paint.set(inkex.addNS('insensitive', 'sodipodi'), 'true')
            else:
                try:
                    del paint.attrib[inkex.addNS('insensitive', 'sodipodi')]
                except KeyError:
                    pass
            if hpaint:
                paint.set('style', 'display:none')
            else:
                paint.set('style', 'display:inline')
            background = self.getElementById('bg%s' % (i))
            if lbackground:
                background.set(inkex.addNS('insensitive', 'sodipodi'), 'true')
            else:
                try:
                    del background.attrib[inkex.addNS('insensitive', 'sodipodi')]
                except KeyError:
                    pass
            if hbackground:
                background.set('style', 'display:none')
            else:
                background.set('style', 'display:inline')
            pencil = self.getElementById('pencil%s' % (i))
            if (pencil):
                if lpencil:
                    pencil.set(inkex.addNS('insensitive', 'sodipodi'), 'true')
                else:
                    try:
                        del pencil.attrib[inkex.addNS('insensitive', 'sodipodi')]
                    except KeyError:
                        pass
                if hpencil:
                    pencil.set('style', 'display:none')
                else:
                    pencil.set('style', 'display:inline')


if __name__ == '__main__':
    effect = HideLockSublayers()
    effect.affect()
