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
A template to create an animated SVG document which uses SVG animation
attributes to cycle through Inkscape layers like animation frames.

A pencil test can also be imported as a series of images linked to the
frame layers.
"""
import pathlib

import elements
import inkex


class ImportPenciltest(inkex.TemplateExtension):
    """ Generate animation layer frames with optional frame imports """
    multi_inx = True

    def __init__(self):
        super(ImportPenciltest, self).__init__()

    def add_arguments(self, pars):
        """ Override """
        pars.add_argument(
            "--from_frame",
            type=int,
            dest="from_frame",
            default="1",
            help="Start frame number",
        )
        pars.add_argument(
            "--to_frame",
            type=int,
            dest="to_frame",
            default="12",
            help="End frame number",
        )
        pars.add_argument(
            "--frame_rate",
            type=int,
            dest="frame_rate",
            default="12",
            help="Frame rate",
        )
        pars.add_argument(
            "--frame_images",
            type=str,
            dest="frame_images",
            help="Included frames for frame layers",
        )
        pars.add_argument(
            "--background_image",
            type=str,
            dest="background_image",
            help="Included background image for frame layers",
        )
        pars.add_argument(
            "--background_color",
            type=inkex.Color,
            dest="background_color",
            default=inkex.Color(0),
            help="Frame background color",
        )

    def get_template(self):
        svg = self.document.getroot()
        opt = self.options

        # Frame range
        from_frame = opt.from_frame
        to_frame = opt.to_frame

        duration = 1000 / opt.frame_rate

        # Including images is optional
        frame_images = opt.frame_images
        background_image = pathlib.Path(opt.background_image).as_uri()

        background_color = opt.background_color

        # Rename default layer to "Background"
        default_layer = svg.getElementById("layer1")
        default_layer.set('inkscape:label', 'Shot Background')
        if background_image is not None:
            image_elem = inkex.Image()
            image_elem.set("xlink:href", "%s" % (background_image))
            default_layer.add(image_elem)

        for frame_number in range(from_frame, to_frame + 1):
            i = format(frame_number, "03d")

            # Create a new frame layer.
            frame_layer = inkex.Layer.new(
                "frame %s" % (i),
                id="f%s" % (i),
                style="display:none",
            )
            svg.add(frame_layer)

            # Add SMIL animation timing for browser preview

            # set initial state of layer
            set_display_init = elements.SetCssElement.new(
                "display",
                "none",
                id="init%s" % (i),
                begin="0ms; off%s.end" % (format(to_frame, "03d")),
                # the first frame displays for (duration * 0) seconds
                # the next frame for (duration * 1) seconds ...
                dur="%sms" % (duration * (frame_number - 1)),
            )
            frame_layer.add(set_display_init)

            # set onstate of layer
            # holds frame for 1 duration
            set_display_on = elements.SetCssElement(
                "display",
                "inline",
                id="on%s" % (i),
                begin="init%s.end" % (i),  # begins when intialstate ends
                dur="%sms" % (duration),
            )
            frame_layer.add(set_display_on)

#            # Set offstate of layer
            set_display_off = elements.SetCssElement(
                "display",
                "none",
                id="off%s" % (i),
                begin="on%s.end" % (i),  # begins when onstate ends
                dur="%sms" % ((duration * to_frame) - (duration * (frame_number - 1)) + 1),
            )
            frame_layer.add(set_display_off)

            # Add background sub-layer
            frame_background = inkex.Layer("background", id="bg%s" % (i))
            frame_layer.add(frame_background)

#            # create a rect element the same size as the document and fill
#            # with the selected color
#            inkex.etree.SubElement(
#                background,
#                "rect",
#                id="bgfill%s" % (i),
#                width="%d" % (width),
#                height="%s" % (height),
#                style="fill:%s" % (background_color),
#            )
#
#            if frame_image:
#                # add list of frames to the pencil test layer
#                pencil = inkex.etree.SubElement(
#                    layer, "g", id="pencil%s" % (i), style="opacity:0.4"
#                )
#                pencil.set(inkex.addNS("label", "inkscape"), "pencil")
#                pencil.set(inkex.addNS("groupmode", "inkscape"), "layer")
#                pencil.set(inkex.addNS("insensitive", "sodipodi"), "true")
#                pimage = inkex.etree.SubElement(pencil, "image", id="pimage%s" % (i))
#                pimage.set(inkex.addNS("href", "xlink"), "%s%s%s" % (frame_image))
#                paint = inkex.etree.SubElement(layer, "g", id="paint%s" % (i))
#                paint.set(inkex.addNS("label", "inkscape"), "paint")
#                paint.set(inkex.addNS("groupmode", "inkscape"), "layer")
#                ink = inkex.etree.SubElement(layer, "g", id="ink%s" % (i))
#                ink.set(inkex.addNS("label", "inkscape"), "ink")
#                ink.set(inkex.addNS("groupmode", "inkscape"), "layer")
#
#                add_frame(layer, i)
#
#def add_frame(layer, frame_number):
#    """ Add the frame number to the layer."""
#    frametext = inkex.ShapeElement(
#        layer,
#        "text",
#        id="frametext%s" % (frame_number),
#        x="0",
#        y="14",
#        style="""
#            display:none;
#            font-size:18px;
#            font-style:normal;
#            font-weight:normal;
#            line-height:125%;
#            letter-spacing:0px;
#            word-spacing:0px;
#            fill:#000000;
#            fill-opacity:0.3;
#            stroke:none;
#            font-family:Sans
#            """,
#    )
#    frametextspan = inkex.ShapeElement(
#        frametext, "tspan", id="tspan%s" % (frame_number), x="0", y="14"
#    )
#    frametextspan.text = frame_number

        return self.document

if __name__ == "__main__":
    ImportPenciltest().run()
