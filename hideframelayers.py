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
Tool for hiding and locking frame layers.
It is part of the Inkscape animation extension
"""

import inkex
import elements


class HideLockSublayers(inkex.EffectExtension):
    """ Hide or lock frame layers """

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
            "--show_frame_numbers",
            type=inkex.Boolean,
            dest="show_frame_numbers",
            default=False,
            help="Display the frame number",
        )
        pars.add_argument(
            "--hide_frame_layers",
            type=inkex.Boolean,
            dest="hide_frame_layers",
            default=False,
            help="Hide all frame layers",
        )
        pars.add_argument(
            "--lock_frame_layers",
            type=inkex.Boolean,
            dest="lock_frame_layers",
            default=False,
            help="Lock all frame layers",
        )
        pars.add_argument(
            "--hide_ink_layers",
            type=inkex.Boolean,
            dest="hide_ink_layers",
            default=False,
            help="Hide all ink sublayers",
        )
        pars.add_argument(
            "--lock_ink_layers",
            type=inkex.Boolean,
            dest="lock_ink_layers",
            default=False,
            help="Lock all ink sublayers",
        )
        pars.add_argument(
            "--hide_paint_layers",
            type=inkex.Boolean,
            dest="hide_paint_layers",
            default=False,
            help="Hide all paint sublayers",
        )
        pars.add_argument(
            "--lock_paint_layers",
            type=inkex.Boolean,
            dest="lock_paint_layers",
            default=False,
            help="Lock all paint sublayers",
        )
        pars.add_argument(
            "--hide_background_layers",
            type=inkex.Boolean,
            dest="hide_background_layers",
            default=False,
            help="Hide all background sublayers",
        )
        pars.add_argument(
            "--lock_background_layers",
            type=inkex.Boolean,
            dest="lock_background_layers",
            default=False,
            help="Lock all background sublayers",
        )
        pars.add_argument(
            "--hide_pencil_layers",
            type=inkex.Boolean,
            dest="hide_pencil_layers",
            default=False,
            help="Hide all pencil sublayers",
        )
        pars.add_argument(
            "--lock_pencil_layers",
            type=inkex.Boolean,
            dest="lock_pencil_layers",
            default=False,
            help="Lock all pencil sublayers",
        )

    def layers(self, node=None):
        """ iterate over layers """
        if node is None:
            node = self.document.getroot()
        for sub_node in node.iterchildren():
            if isinstance(sub_node, inkex.Layer) and sub_node.label:
                yield (sub_node.label, sub_node)

    def effect(self):
        """ Apply the effect """
        opt = self.options
        duration_ms = 1000 / opt.frame_rate

        to_frame_duration = duration_ms * opt.to_frame

        # Hide or lock layers and sublayers
        xpath_layers = (
            "/svg:svg//*[name()='g'"
            " and @inkscape:groupmode='layer'"
            " and starts-with(@id, 'frame-')"
            " or starts-with(@id, 'ink-')"
            " or starts-with(@id, 'paint-')"
            " or starts-with(@id, 'pencil-')"
            " or starts-with(@id, 'background-')"
            "][@id]"
        )
        for layer in self.svg.xpath(xpath_layers):
            *layer_type, frame_num_str = layer.get("id").split("-")
            layer_type = " ".join(layer_type)
            try:
                frame_num = int(frame_num_str)
            except ValueError:
                continue

            if opt.from_frame <= frame_num <= opt.to_frame:
                if layer_type == "frame":
                    set_hidden_locked(
                        layer, opt.hide_frame_layers, opt.lock_frame_layers
                    )
                if layer_type == "background":
                    set_hidden_locked(
                        layer, opt.hide_background_layers, opt.lock_background_layers,
                    )
                if layer_type == "paint":
                    set_hidden_locked(
                        layer, opt.hide_paint_layers, opt.lock_paint_layers,
                    )
                if layer_type == "ink":
                    set_hidden_locked(layer, opt.hide_ink_layers, opt.lock_ink_layers)
                if layer_type == "pencils":
                    set_hidden_locked(
                        layer, opt.hide_pencil_layers, opt.lock_pencil_layers,
                    )

        # Update frame display duration for browser preview
        xpath_set_nodes = (
            "/svg:svg//*[name()='set'"
            " and starts-with(@id, 'init-')"
            " or starts-with(@id, 'on-')"
            " or starts-with(@id, 'off-')"
            "][@id]"
        )
        for set_node in self.svg.xpath(xpath_set_nodes):
            *set_node_type, frame_num_str = set_node.get("id").split("-")
            set_node_type = " ".join(set_node_type)
            try:
                frame_num = int(frame_num_str)
            except ValueError:
                continue
            if opt.from_frame <= frame_num <= opt.to_frame:
                if set_node_type == "init":
                    adjusted_init_duration = duration_ms * (frame_num - 1)
                    set_node.set("dur", f"{adjusted_init_duration}ms")
                if set_node_type == "on":
                    set_node.set("dur", f"{duration_ms}ms")
                if set_node_type == "off":
                    adjusted_off_duration = (
                        to_frame_duration - (duration_ms * (frame_num - 1)) + 1
                    )
                    set_node.set("dur", f"{adjusted_off_duration}ms")

        # Hide/show frame numbers
        xpath_frame_nodes = (
            "/svg:svg//*[name()='text' and starts-with(@id, 'frametext-')][@id]"
        )
        for frame_node in self.svg.xpath(xpath_frame_nodes):
            *frame_node_type, frame_num_str = frame_node.get("id").split("-")
            frame_node_type = " ".join(frame_node_type)
            try:
                frame_num = int(frame_num_str)
            except ValueError:
                continue
            if opt.from_frame <= frame_num <= opt.to_frame:
                # set frame number display
                if opt.show_frame_numbers:
                    frame_node.style["display"] = "inline"
                else:
                    frame_node.style["display"] = "none"


def set_hidden_locked(node, hidden, locked):
    """ Set layer hidden or locked """
    if isinstance(node, inkex.Layer):
        if locked:
            node.set(inkex.addNS("insensitive", "sodipodi"), "true")
        else:
            try:
                del node.attrib[inkex.addNS("insensitive", "sodipodi")]
            except KeyError:
                pass
        if hidden:
            node.style["display"] = "none"
        else:
            node.style["display"] = "inline"


if __name__ == "__main__":
    HideLockSublayers().run()
