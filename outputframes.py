#! /usr/bin/env python
# coding=utf-8

"""
Tool for outputting frame layers to a series of png images.
It is part of the Inkscape animation extension
"""

import sys
import os
import inkex
import simplestyle

from cStringIO import StringIO

try:
    from subprocess import Popen, PIPE

    bsubprocess = True
except:
    bsubprocess = False


class OutputFrames(inkex.OutputExtension):
    def add_arguments(self, pars):
        pars.add_argument(
            "--fromframe", type=int, dest="fromframe", default="1", help="From frame #",
        )
        pars.add_argument(
            "--toframe", type=int, dest="toframe", default="10", help="From frame #",
        )
        pars.add_argument(
            "--directory",
            type="string",
            dest="directory",
            default="./",
            help="Directory to save images to",
        )
        pars.add_argument(
            "--image",
            type="string",
            dest="image",
            default=None,
            help="Image name (without extension)",
        )
        pars.add_argument(
            "--hpencil",
            type=inkex.Boolean,
            dest="hpencil",
            default="true",
            help="Hide pencil sublayer during export?",
        )

    def check_dir_exists(self, dir):
        if not os.path.isdir(dir):
            os.makedirs(dir)

    def sethide(self, node, hide):
        if hide:
            node.set("style", "display:none")
        else:
            node.set("style", "display:inline")

    def effect(self):
        self.svg = self.document.getroot()
        fromframe = self.options.fromframe
        toframe = self.options.toframe
        svg_file = self.args[-1]
        docname = self.xpathSingle("/svg:svg/@sodipodi:docname")[:-4]
        dirname = os.path.dirname(self.options.directory)
        image = self.options.image
        hpencil = self.options.hpencil

        if dirname == "" or dirname == None:
            dirname = "./"
        dirname = os.path.expanduser(dirname)
        dirname = os.path.expandvars(dirname)
        # self.check_dir_exists(dirname)
        commands = StringIO()
        log = ""

        # iterate through the xml whenever the layer name is between
        # fromframe and toframe then edit the xml
        for node in self.svg.iter():
            tag = node.tag.split("}")[1]
            if node.tag == inkex.addNS("g", "svg"):
                idattr = node.attrib["id"]
                frametype = idattr[:-3]
                frame = idattr[-3:]
                try:
                    framenum = int(frame)
                except:
                    continue
                log += "idattr:%s type:%s frame:%s\n" % (idattr, frametype, frame)
                if fromframe <= framenum <= toframe:
                    if frametype == "f":
                        self.sethide(node, False)
                        filename = dirname + os.path.sep + image + frame + ".png"
                        commands.write(
                            "%s -i %s -j -C -e %s\n" % (svg_file, idattr, filename)
                        )
                    if frametype == "pencil":
                        self.sethide(node, hpencil)
        # TODO frames not being set to show
        commands.write("quit\n")
        if bsubprocess:
            echo = Popen(["echo", commands.getvalue()], shell=False, stdout=PIPE)
            ink = Popen(
                ["inkscape", "--shell"],
                shell=False,
                stdin=echo.stdout,
                stdout=PIPE,
                stderr=PIPE,
            )
        else:
            # reference: http://stackoverflow.com/questions/7442665/convert-svg-file-to-multiple-different-size-png-files
            _, ink, err = os.open3(
                "inkscape --shell <<COMMANDS\n%sCOMMANDS" % (commands)
            )
            ink.close()
        stdoutdata, stderrdata = ink.communicate()
        log += stdoutdata
        # uncomment next line to see log
        # inkex.errormsg(log + commands.getvalue())


if __name__ == "__main__":
    e = OutputFrames()
    e.affect()
