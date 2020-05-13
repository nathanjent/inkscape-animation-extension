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

    def layers(self, document=None):
        """ iterate over layers """
        if document is None:
            document = self.document
        for node in document.getroot().iterchildren():
            if isinstance(node, inkex.Layer) and node.label:
                yield (node.label, node)

    def effect(self):
        """ Apply the effect """
        opt = self.options
        duration_ms = 1000 / opt.frame_rate

        for (label, layer) in self.layers():
            *frame_type, frame_num_str = label.split("-")
            frame_type = " ".join(frame_type)
            if frame_type == "frame":
                frame_num = int(frame_num_str)
                if opt.from_frame <= frame_num <= opt.to_frame:
                    set_hidden_locked(
                        layer, opt.hide_frame_layers, opt.lock_frame_layers
                    )

                    # update frame display duration for browser preview
                    for sub_node in layer.iterchildren():
                        set_node_id = sub_node.get("id")
                        set_node_type, *_ = set_node_id.split("-")
                        if isinstance(sub_node, inkex.Layer) and sub_node.label:
                            sub_label = sub_node.label
                            if sub_label == "background":
                                set_hidden_locked(
                                    sub_node,
                                    opt.hide_background_layers,
                                    opt.lock_background_layers,
                                )
                            if sub_label == "paint":
                                set_hidden_locked(
                                    sub_node, opt.hide_paint_layers, opt.lock_paint_layers
                                )
                            if sub_label == "ink":
                                set_hidden_locked(
                                    sub_node, opt.hide_ink_layers, opt.lock_ink_layers
                                )
                            if sub_label == "pencils":
                                set_hidden_locked(
                                    sub_node, opt.hide_pencil_layers, opt.lock_pencil_layers
                                )
                        if isinstance(sub_node, elements.SetElement):
                            if set_node_type == "init":
                                sub_node.set(
                                    "dur", "%sms" % (duration_ms * (frame_num - 1))
                                )
                            if set_node_type == "on":
                                sub_node.set("dur", "%sms" % (duration_ms))
                            if frame_type == "off":
                                sub_node.set(
                                    "dur",
                                    "%sms"
                                    % (
                                        (duration_ms * (opt.to_frame - 1))
                                        - (duration_ms * (frame_num - 1))
                                        + 1
                                    ),
                                )
                        if isinstance(sub_node, inkex.TextElement):
                            # set frame number display
                            if set_node_type == "frametext":
                                if opt.show_frame_numbers:
                                    sub_node.set(
                                        "style",
                                        """
                                        display:inline;
                                        font-size:18px;
                                        font-style:normal;
                                        font-weight:normal;
                                        line-height:125%;
                                        letter-spacing:0px;
                                        word-spacing:0px;
                                        fill:#000000;
                                        fill-opacity:0.3;
                                        stroke:none;
                                        font-family:Sans
                                        """,
                                    )
                                else:
                                    sub_node.set(
                                        "style",
                                        """
                                        display:none;
                                        font-size:18px;
                                        font-style:normal;
                                        font-weight:normal;
                                        line-height:125%;
                                        letter-spacing:0px;
                                        word-spacing:0px;
                                        fill:#000000;
                                        fill-opacity:0.3;
                                        stroke:none;
                                        font-family:Sans
                                        """,
                                    )


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
        # FIXME don't lose other existing styles
        style_attr = node.get("style")
        if hidden:
            node.set("style", "display:none")
        else:
            node.set("style", "display:inline")


if __name__ == "__main__":
    HideLockSublayers().run()
