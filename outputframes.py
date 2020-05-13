#! /usr/bin/env python
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
Tool for outputting frame layers to a series of png images.
It is part of the Inkscape animation extension
"""
from pathlib import Path
import inkex


class OutputFrames(inkex.OutputExtension):
    """ Write frame layers to a series of image files """

    def add_arguments(self, pars):
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
            default="10",
            help="End frame number",
        )
        pars.add_argument(
            "--base_file",
            type=str,
            dest="base_file",
            default=None,
            help="Base filename to save frame images",
        )
        pars.add_argument(
            "--hide_pencil",
            type=inkex.Boolean,
            dest="hide_pencil",
            default=True,
            help="Hide pencil sublayer during export?",
        )

    def layers(self, document=None):
        """ iterate over layers """
        if document is None:
            document = self.document
        for node in document.getroot().iterchildren():
            if isinstance(node, inkex.Layer) and node.label:
                yield (node.label, node)

    def save(self, stream):
        """ Save frame layers as multiple images """
        svg = self.document.getroot()
        opt = self.options

        base_file = Path(opt.base_file)
        output_dir = base_file.parent

        for (label, layer) in self.layers():
            frame_id = layer.get("id")
            *_, frame_num_str = label.split("-")
            frame_num = int(frame_num_str)

            if opt.from_frame <= frame_num <= opt.to_frame:
                set_hidden(layer, False)
                for (sub_label, sub_layer) in self.layers(layer):
                    if sub_label == "pencils":
                        set_hidden(sub_layer, opt.hide_pencil)

                # Save layer image
                if inkex.command.is_inkscape_available():
                    inkex.command.take_snapshot(
                        svg,
                        output_dir,
                        name=(base_file.stem + frame_num_str),
                        ext=base_file.suffix,
                        export_id=frame_id,
                        export_id_only=True,
                    )


def set_hidden(node, hide):
    """ Set display style attribute """
    if hide:
        node.set("style", "display:none")
    else:
        node.set("style", "display:inline")


if __name__ == "__main__":
    OutputFrames().run()
