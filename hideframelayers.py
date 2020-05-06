#! /usr/bin/env python
# coding=utf-8

"""
Tool for hiding and locking frame layers.
It is part of the Inkscape animation extension
"""

import sys
import inkex
import simplestyle

sys.path.append("/usr/share/inkscape/extensions")


class HideLockSublayers(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument(
            "--hframe",
            type=inkex.Boolean,
            dest="hframe",
            default="false",
            help="Hide all frame layers",
        )
        pars.add_argument(
            "--lframe",
            type=inkex.Boolean,
            dest="lframe",
            default="false",
            help="Lock all frame layers",
        )
        pars.add_argument(
            "--hink",
            type=inkex.Boolean,
            dest="hink",
            default="false",
            help="Hide all ink sublayers",
        )
        pars.add_argument(
            "--link",
            type=inkex.Boolean,
            dest="link",
            default="false",
            help="Lock all ink sublayers",
        )
        pars.add_argument(
            "--hpaint",
            type=inkex.Boolean,
            dest="hpaint",
            default="false",
            help="Hide all paint sublayers",
        )
        pars.add_argument(
            "--lpaint",
            type=inkex.Boolean,
            dest="lpaint",
            default="false",
            help="Lock all paint sublayers",
        )
        pars.add_argument(
            "--hbackground",
            type=inkex.Boolean,
            dest="hbackground",
            default="false",
            help="Hide all background sublayers",
        )
        pars.add_argument(
            "--lbackground",
            type=inkex.Boolean,
            dest="lbackground",
            default="false",
            help="Lock all background sublayers",
        )
        pars.add_argument(
            "--hpencil",
            type=inkex.Boolean,
            dest="hpencil",
            default="false",
            help="Hide all pencil sublayers",
        )
        pars.add_argument(
            "--lpencil",
            type=inkex.Boolean,
            dest="lpencil",
            default="false",
            help="Lock all pencil sublayers",
        )
        pars.add_argument(
            "--fromframe", type=int, dest="fromframe", default="1", help="From frame #",
        )
        pars.add_argument(
            "--toframe", type=int, dest="toframe", default="12", help="From frame #",
        )
        pars.add_argument(
            "--duration",
            type=float,
            dest="duration",
            default="83.3",
            help="Display frame duration in milliseconds",
        )
        pars.add_argument(
            "--showframenum",
            type=inkex.Boolean,
            dest="showframenum",
            default="false",
            help="Display the frame number",
        )

    def setlockhide(self, node, hide, lock):
        if lock:
            node.set(inkex.addNS("insensitive", "sodipodi"), "true")
        else:
            try:
                del node.attrib[inkex.addNS("insensitive", "sodipodi")]
            except KeyError:
                pass
        if hide:
            node.set("style", "display:none")
        else:
            node.set("style", "display:inline")

    def effect(self):
        self.svg = self.document.getroot()

        fromframe = self.options.fromframe
        toframe = self.options.toframe
        duration = self.options.duration
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
        showframenum = self.options.showframenum

        log = ""
        for node in self.svg.iter():
            tag = node.tag.split("}")[1]
            try:
                idattr = node.attrib["id"]
                frametype = idattr[:-3]
                frame = idattr[-3:]
                framenum = int(frame)
            except:
                continue
            if fromframe <= framenum <= toframe:
                if node.tag == inkex.addNS("g", "svg"):
                    if frametype == "f":
                        self.setlockhide(node, hframe, lframe)
                    if frametype == "bg":
                        self.setlockhide(node, hbackground, lbackground)
                    if frametype == "paint":
                        self.setlockhide(node, hpaint, lpaint)
                    if frametype == "ink":
                        self.setlockhide(node, hink, link)
                    if frametype == "pencil":
                        self.setlockhide(node, hpencil, lpencil)

                # update frame display duration for browser preview
                if node.tag == inkex.addNS("set", "svg"):
                    if frametype == "init":
                        node.set("dur", "%sms" % (duration * (framenum - 1)))
                    if frametype == "on":
                        node.set("dur", "%sms" % (duration))
                    if frametype == "off":
                        node.set(
                            "dur",
                            "%sms"
                            % (
                                (duration * (toframe - 1))
                                - (duration * (framenum - 1))
                                + 1
                            ),
                        )

                # set frame number display
                if node.tag == inkex.addNS("text", "svg"):
                    if frametype == "frametext":
                        if showframenum:
                            node.set(
                                "style",
                                "display:inline;font-size:18px;font-style:normal;font-weight:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:0.3;stroke:none;font-family:Sans",
                            )
                        else:
                            node.set(
                                "style",
                                "display:none;font-size:18px;font-style:normal;font-weight:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:0.3;stroke:none;font-family:Sans",
                            )
        # uncomment next line to see log
        # inkex.errormsg(log)


if __name__ == "__main__":
    effect = HideLockSublayers()
    effect.affect()
