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

import inkex
import elements


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
        opt = self.options

        duration_ms = 1000 / opt.frame_rate
        (width, _, height, _) = self.get_size()

        # Including images are optional
        if opt.frame_images is not None:
            opt.frame_images = opt.frame_images.split("|")

        # Rename default layer to "Background"
        default_layer = self.svg.getElementById("layer1")
        default_layer.set("inkscape:label", "Shot Background")
        if opt.background_image is not None:
            image_path = pathlib.Path(opt.background_image)
            if image_path.is_file():
                image_elem = inkex.Image()
                # Set background image to the view size
                image_elem.set("width", width)
                image_elem.set("height", height)
                image_elem.set("xlink:href", str(image_path.as_uri()))
                default_layer.add(image_elem)

        index = 0
        frame_image = None
        to_frame_fmt = format(opt.to_frame, "03d")
        to_frame_duration = duration_ms * opt.to_frame
        for frame_number in range(opt.from_frame, opt.to_frame + 1):
            frame_num_fmt = format(frame_number, "03d")

            if opt.frame_images is not None:
                if index < len(opt.frame_images):
                    frame_image = opt.frame_images[index]
                index += 1

            # Create a new frame layer.
            frame_id = f"frame-{frame_num_fmt}"
            frame_layer = inkex.Layer.new(frame_id, id=frame_id, style="display:none",)
            self.svg.add(frame_layer)

            # Add SMIL animation timing for browser preview

            # set initial state of layer
            initial_duration = duration_ms * (frame_number - 1)
            set_display_init = elements.SetElement.new(
                "display",
                "none",
                id=f"init-{frame_num_fmt}",
                begin=f"0ms; off-{to_frame_fmt}.end",
                # the first frame displays for (duration * 0) seconds
                # the next frame for (duration * 1) seconds ...
                dur=f"{initial_duration}ms",
            )
            frame_layer.add(set_display_init)

            # set onstate of layer
            # holds frame for 1 duration
            set_display_on = elements.SetElement.new(
                "display",
                "inline",
                id=f"on-{frame_num_fmt}",
                # begins when intialstate ends
                begin=f"init-{frame_num_fmt}.end",
                dur=f"{duration_ms}ms",
            )
            frame_layer.add(set_display_on)

            # Set offstate of layer
            off_duration = to_frame_duration - (duration_ms * (frame_number - 1)) + 1
            set_display_off = elements.SetElement.new(
                "display",
                "none",
                id=f"off-{frame_num_fmt}",
                # begins when onstate ends
                begin=f"on-{frame_num_fmt}.end",
                dur=f"{off_duration}ms",
            )
            frame_layer.add(set_display_off)

            # Add background sub-layer
            frame_background = inkex.Layer.new(
                "background", id=f"background-{frame_num_fmt}",
            )
            frame_layer.add(frame_background)

            # create a rect element the same size as the document and fill
            # with the selected color
            frame_background_rect = inkex.Rectangle.new(
                0,
                0,
                width,
                height,
                id=f"bgfill-{frame_num_fmt}",
                style=f"fill:{opt.background_color}",
            )
            frame_background.add(frame_background_rect)

            if frame_image is not None:
                # Add frame image as pencils layer
                frame_image_layer = inkex.Layer.new(
                    "pencils", id=f"pencils-{frame_num_fmt}", style="opacity:0.4",
                )
                frame_layer.add(frame_image_layer)

                # Create image set to the view size
                image_path = pathlib.Path(frame_image)
                pencil_image = inkex.Image(id=f"pimage-{frame_num_fmt}")
                pencil_image.set("width", width)
                pencil_image.set("height", height)
                pencil_image.set("xlink:href", str(image_path.as_uri()))
                frame_image_layer.add(pencil_image)

            paint_layer = inkex.Layer.new("paint", id=f"paint-{frame_num_fmt}")
            frame_layer.add(paint_layer)

            ink_layer = inkex.Layer.new("ink", id=f"ink-{frame_num_fmt}")
            frame_layer.add(ink_layer)

            # Add the frame number to the layer
            frame_number_text = inkex.TextElement(
                id=f"frametext-{frame_num_fmt}",
                x="0",
                y="14",
                style="display:none;fill-opacity:0.3;font-family:monospace",
            )
            frame_layer.add(frame_number_text)
            frame_num_tspan = inkex.Tspan(
                frame_num_fmt, x="0", y="14", id=f"frametspan-{frame_num_fmt}",
            )
            frame_number_text.add(frame_num_tspan)

        return self.document


if __name__ == "__main__":
    ImportPenciltest().run()
