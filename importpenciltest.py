#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2014 Nathan Jent <nathanjent@nathanjent.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

"""
Tool for creating animation frame layers. A pencil test can also be imported as
a series of images linked to the frame layers.
It is part of the Inkscape animation extension.
"""
import inkex


class ImportPenciltest(inkex.InputExtension):
    """ Import from a series of images or generate the animation layers. """

    def add_arguments(self, pars):
        pars.add_argument(
            "--fromframe", type=int, dest="fromframe", default="1", help="From frame #",
        )
        pars.add_argument(
            "--toframe", type=int, dest="toframe", default="12", help="From frame #",
        )
        pars.add_argument(
            "--filename",
            type="string",
            dest="filename",
            default="frame",
            help="Base file name",
        )
        pars.add_argument(
            "--filetype",
            type="string",
            dest="filetype",
            default=".png",
            help="Base file name",
        )
        pars.add_argument(
            "--svgw", type=int, dest="svgw", default="560", help="SVG Document Width",
        )
        pars.add_argument(
            "--svgh", type=int, dest="svgh", default="316", help="SVG Document Height",
        )
        pars.add_argument(
            "--importpencil",
            type="inkbool",
            dest="importpencil",
            default="false",
            help="Import pencil test images?",
        )
        pars.add_argument(
            "--tab",
            type="string",
            dest="tab",
            default="Frames",
            help="The selected UI-tab when OK was pressed",
        )
        pars.add_argument(
            "--bgcolor",
            type="string",
            dest="bgcolor",
            default=0,
            help="Frame background color",
        )
        pars.add_argument(
            "--duration",
            type=float,
            dest="duration",
            default="83.3",
            help="Display frame duration in milliseconds",
        )

    def unsignedLong(self, signedLongString):
        long_color = long(signedLongString)
        if long_color < 0:
            long_color = long_color & 0xFFFFFFFF
        return long_color

    def getColorString(self, longColor):
        """ A*256^0 + B*256^1 + G*256^2 + R*256^3 """
        longColor = self.unsignedLong(longColor)
        hexColor = hex(longColor)[2:-3]
        hexColor = hexColor.rjust(6, "0")
        return "#" + hexColor.upper()

    def effect(self):
        fromframe = self.options.fromframe
        toframe = self.options.toframe + 1
        duration = self.options.duration
        filename = self.options.filename
        filetype = self.options.filetype
        svgw = self.options.svgw
        svgh = self.options.svgh
        importpencil = self.options.importpencil
        bgcolor = self.getColorString(self.options.bgcolor)

        svg = self.document.getroot()
        # or alternatively
        # svg = self.document.xpath('//svg:svg',namespaces=inkex.NSS)[0]

        # set svg document dimensions
        svg.set("width", "%s" % (svgw))
        svg.set("height", "%s" % (svgh))
        # latest version of inkscape requires update to the viewbox as well
        svg.set("viewBox", "0 0 %s %s" % (svgw, svgh))

        for framenum in range(fromframe, toframe):
            i = format(framenum, "03d")

            # Create a new frame layer.
            layer = inkex.etree.SubElement(
                svg, "g", id="f%s" % (i), style="display:none"
            )
            layer.set(inkex.addNS("label", "inkscape"), "f%s" % (i))
            layer.set(inkex.addNS("groupmode", "inkscape"), "layer")

            # Add SMIL animation timing for browser preview
            initialstate = inkex.etree.SubElement(
                layer,
                "set",
                id="init%s" % (i),
                attributeName="display",
                attributeType="CSS",
                to="none",
                begin="0ms; off%s.end" % (format(toframe - 1, "03d")),
                dur="%sms" % (duration * (framenum - 1)),
            )  # the first frame displays for (duration * 0) seconds, the next frame for (duration * 1) seconds ...
            onstate = inkex.etree.SubElement(
                layer,
                "set",
                id="on%s" % (i),
                attributeName="display",
                attributeType="CSS",
                to="inline",
                begin="init%s.end" % (i),  # begins when intialstate ends
                dur="%sms" % (duration),
            )  # holds frame for 1 duration
            offstate = inkex.etree.SubElement(
                layer,
                "set",
                id="off%s" % (i),
                attributeName="display",
                attributeType="CSS",
                to="none",
                begin="on%s.end" % (i),  # begins when onstate ends
                dur="%sms"
                % ((duration * (toframe - 1)) - (duration * (framenum - 1)) + 1),
            )

            # Create ink, paint, background, and pencil layers.
            background = inkex.etree.SubElement(layer, "g", id="bg%s" % (i))
            background.set(inkex.addNS("label", "inkscape"), "background")
            background.set(inkex.addNS("groupmode", "inkscape"), "layer")
            background.set(inkex.addNS("insensitive", "sodipodi"), "true")
            # create a rect the same size as the document and fill with the selected color
            bgfill = inkex.etree.SubElement(
                background,
                "rect",
                id="bgfill%s" % (i),
                width="%d" % (svgw),
                height="%s" % (svgh),
                style="fill:%s" % (bgcolor),
            )
            if importpencil:
                pencil = inkex.etree.SubElement(
                    layer, "g", id="pencil%s" % (i), style="opacity:0.4"
                )
                pencil.set(inkex.addNS("label", "inkscape"), "pencil")
                pencil.set(inkex.addNS("groupmode", "inkscape"), "layer")
                pencil.set(inkex.addNS("insensitive", "sodipodi"), "true")
                pimage = inkex.etree.SubElement(pencil, "image", id="pimage%s" % (i))
                pimage.set(
                    inkex.addNS("href", "xlink"), "%s%s%s" % (filename, i, filetype)
                )
            paint = inkex.etree.SubElement(layer, "g", id="paint%s" % (i))
            paint.set(inkex.addNS("label", "inkscape"), "paint")
            paint.set(inkex.addNS("groupmode", "inkscape"), "layer")
            ink = inkex.etree.SubElement(layer, "g", id="ink%s" % (i))
            ink.set(inkex.addNS("label", "inkscape"), "ink")
            ink.set(inkex.addNS("groupmode", "inkscape"), "layer")

            # Add the frame number to the layer.
            frametext = inkex.etree.SubElement(
                layer,
                "text",
                id="frametext%s" % (i),
                x="0",
                y="14",
                style="display:none;font-size:18px;font-style:normal;font-weight:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:0.3;stroke:none;font-family:Sans",
            )
            frametextspan = inkex.etree.SubElement(
                frametext, "tspan", id="tspan%s" % (i), x="0", y="14"
            )
            frametextspan.text = i


# Create effect instance and apply it.
effect = ImportPenciltest()
effect.affect()
