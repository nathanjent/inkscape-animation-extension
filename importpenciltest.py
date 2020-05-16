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

    def add_arguments(self, pars):
        """ Overide to process INX input """
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

        duration_ms = 1000 / opt.frame_rate
        (width, _, height, _) = self.get_size()

        # Including images are optional
        if opt.frame_images is not None:
            opt.frame_images = opt.frame_images.split("|")

        # Rename default layer to "Background"
        default_layer = svg.getElementById("layer1")
        default_layer.set("inkscape:label", "Shot Background")
        if opt.background_image is not None:
            image_elem = inkex.Image()
            # Set background image to the view size
            image_elem.set("width", width)
            image_elem.set("height", height)
            image_elem.set(
                "xlink:href", str(pathlib.Path(opt.background_image).as_uri())
            )
            default_layer.add(image_elem)

        index = 0
        frame_image = None
        for frame_number in range(opt.from_frame, opt.to_frame + 1):
            frame_fmt_num = format(frame_number, "03d")

            if opt.frame_images is not None:
                if index < len(opt.frame_images):
                    frame_image = opt.frame_images[index]
                index += 1

            # Create a new frame layer.
            frame_layer = inkex.Layer.new(
                "frame-%s" % (frame_fmt_num),
                id="frame-%s" % (frame_fmt_num),
                style="display:none",
            )
            svg.add(frame_layer)

            # Add SMIL animation timing for browser preview

            # set initial state of layer
            set_display_init = elements.SetElement.new(
                "display",
                "none",
                id="init-%s" % (frame_fmt_num),
                begin="0ms; off-%s.end" % (format(opt.to_frame, "03d")),
                # the first frame displays for (duration * 0) seconds
                # the next frame for (duration * 1) seconds ...
                dur="%sms" % (duration_ms * (frame_number - 1)),
            )
            frame_layer.add(set_display_init)

            # set onstate of layer
            # holds frame for 1 duration
            set_display_on = elements.SetElement.new(
                "display",
                "inline",
                id="on-%s" % (frame_fmt_num),
                # begins when intialstate ends
                begin="init-%s.end" % (frame_fmt_num),
                dur="%sms" % (duration_ms),
            )
            frame_layer.add(set_display_on)

            # Set offstate of layer
            set_display_off = elements.SetElement.new(
                "display",
                "none",
                id="off-%s" % (frame_fmt_num),
                # begins when onstate ends
                begin="on-%s.end" % (frame_fmt_num),
                dur="%sms"
                % (
                    (duration_ms * opt.to_frame)
                    - (duration_ms * (frame_number - 1))
                    + 1
                ),
            )
            frame_layer.add(set_display_off)

            # Add background sub-layer
            frame_background = inkex.Layer.new(
                "background", id="background-%s" % (frame_fmt_num)
            )
            frame_layer.add(frame_background)

            # create a rect element the same size as the document and fill
            # with the selected color
            frame_background_rect = inkex.Rectangle.new(
                0,
                0,
                width,
                height,
                id="bgfill-%s" % (frame_fmt_num),
                style="fill:%s" % (opt.background_color),
            )
            frame_background.add(frame_background_rect)

            if frame_image:
                # Add frame image as pencils layer
                frame_image_layer = inkex.Layer.new(
                    "pencils", id="pencils-%s" % (frame_fmt_num), style="opacity:0.4",
                )
                frame_layer.add(frame_image_layer)
                pencil_image = inkex.Image(id="pimage-%s" % (frame_fmt_num))
                pencil_image.set("xlink:href", "%s" % (frame_image))

            paint_layer = inkex.Layer.new("paint", id="paint-%s" % (frame_fmt_num))
            frame_layer.add(paint_layer)
            ink_layer = inkex.Layer.new("ink", id="ink-%s" % (frame_fmt_num))
            frame_layer.add(ink_layer)

            # Add the frame number to the layer
            frame_number_text = inkex.TextElement(
                id="frametext-%s" % (frame_number),
                x="0",
                y="14",
                style="""
                    display:none;
                    fill-opacity:0.3;
                    font-family:monospace
                    """,
            )
            frame_layer.add(frame_number_text)
            frame_num_tspan = inkex.Tspan(
                frame_fmt_num, x="0", y="14", id="tspan%s" % (frame_number),
            )
            frame_number_text.add(frame_num_tspan)

        return self.document


if __name__ == "__main__":
    ImportPenciltest().run()
