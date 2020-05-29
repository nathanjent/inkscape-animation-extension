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

from animation_layers.importpenciltest import ImportPenciltest
from inkex.tester import ComparisonMixin, TestCase


class TestImportPenciltest(ComparisonMixin, TestCase):
    effect_class = ImportPenciltest
    compare_file = "svg/default-inkscape-SVG.svg"
    comparisons = [
        ("--from_frame", "1", "--to_frame", "12"),
        (
            "--from_frame",
            "1",
            "--to_frame",
            "12",
            "--frame_rate",
            "6",
            "--background_color",
            "42",
        ),
    ]
