#!/usr/bin/env python
"""
hideframelayers.py
Tool for hiding and locking frame layers.
It is part of the Inkscape animation extension

Copyright (C) 2014 Nathan Jent <nathanjent@nathanjent.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
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

    def setlockhide(self, node, hide, lock):
        if lock:
            node.set(inkex.addNS('insensitive', 'sodipodi'), 'true')
        else:
            try:
                del node.attrib[inkex.addNS('insensitive', 'sodipodi')]
            except KeyError:
                pass
        if hide:
            node.set('style', 'display:none')
        else:
            node.set('style', 'display:inline')

    def effect(self):
        self.svg = self.document.getroot()
        
        fromframe = self.options.fromframe
        toframe = self.options.toframe
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
        
        log = ''
        for node in self.svg.iter():
            tag = node.tag.split("}")[1]
            log += '%s\n' % (tag)
            if node.tag == inkex.addNS('g','svg'):
                idattr = node.attrib['id']
                frametype = idattr[:-3]
                frame = idattr[-3:]
                try:
                    framenum = int(frame)
                except:
                    continue
                log += 'idattr:%s type:%s frame:%s\n' % (idattr, frametype, frame)
                if fromframe <= framenum <= toframe:
                    if frametype == 'f':
                        self.setlockhide(node, hframe, lframe)
                    if frametype == 'bg':
                        self.setlockhide(node, hbackground, lbackground)
                    if frametype == 'paint':
                        self.setlockhide(node, hpaint, lpaint)
                    if frametype == 'ink':
                        self.setlockhide(node, hink, link)
                    if frametype == 'pencil':
                        self.setlockhide(node, hpencil, lpencil)
        #uncomment next line to see log
        #inkex.errormsg(log)   

if __name__ == '__main__':
    effect = HideLockSublayers()
    effect.affect()
