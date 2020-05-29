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
import shutil
import inkex
from inkex.base import TempDirMixin
from inkex.command import take_snapshot


class OutputFrames(TempDirMixin, inkex.OutputExtension):
    """ Write frame layers to a series of image files """

    def add_arguments(self, pars):
        pars.add_argument(
            "--output_file",
            type=str,
            dest="output_file",
            help="The base filename for exporting frames",
        )
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
            "--include_background",
            type=inkex.Boolean,
            dest="include_background",
            help="Include background sublayer",
        )
        pars.add_argument(
            "--include_pencils",
            type=inkex.Boolean,
            dest="hide_pencil",
            default=True,
            help="Include pencils sublayer",
        )
        pars.add_argument(
            "--background_opacity",
            type=float,
            dest="background_opacity",
            help="Document background opacity",
        )

    def xpath_frame_node(self, xpath):
        """ Iterate over nodes of the given XPath. Node id defines 'type_frame' """
        for node in self.svg.xpath(xpath):
            *node_type, frame_num_str = node.get("id").split("_")
            node.type = " ".join(node_type)
            node.frame_num_str = frame_num_str
            try:
                node.frame_num = int(frame_num_str)
            except ValueError:
                continue
            yield node

    def save(self, stream):
        """ Save frame layers as image sequence """
        opt = self.options
        base_file = Path(opt.output_file)
        if base_file.suffix != ".png":
            base_file = base_file.with_suffix(".png")

        xpath_layers = (
            "/svg:svg//*[name()='g'"
            " and @inkscape:groupmode='layer'"
            " and starts-with(@id, 'frame_')"
            " or starts-with(@id, 'pencils_')"
            " or starts-with(@id, 'background_')"
            "][@id]"
        )
        for layer in self.xpath_frame_node(xpath_layers):
            if opt.from_frame <= layer.frame_num <= opt.to_frame:
                if layer.type == "pencils":
                    set_hidden(layer, opt.include_pencils)
                if layer.type == "background":
                    set_hidden(layer, opt.include_background)
                if layer.type == "frame":
                    set_hidden(layer, False)

                    # Save layer image
                    name = f"{base_file.stem}_{layer.frame_num_str}"
                    out_file = take_snapshot(
                        self.document,
                        dirname=self.tempdir,
                        name=name,
                        ext=base_file.suffix.strip("."),
                        export_id=layer.get("id"),
                        export_id_only=True,
                        export_area_page=True,
                        export_background_opacity=opt.background_opacity,
                    )
                    newname = base_file.parent.joinpath(
                        f"{name}{base_file.suffix}")
                    shutil.copy(out_file, newname)


def set_hidden(node, hide):
    """ Set display style attribute """
    if hide:
        node.set("style", "display:none")
    else:
        node.set("style", "display:inline")


if __name__ == "__main__":
    OutputFrames().run()
