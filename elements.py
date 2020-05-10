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
Define elements for animation not already defined by inkex module.
"""

import inkex


class SetElement(inkex.BaseElement):
    """A set element"""

    tag_name = "set"

    @classmethod
    def new(cls, attr_name, to_value, attr_type, *children, **attrs):
        attrs["attributeName"] = attr_name
        attrs["to"] = to_value
        attrs["attributeType"] = attr_type
        return super(SetElement, cls).new(*children, **attrs)


class SetCssElement(SetElement):
    """Set element for CSS attributes"""

    @classmethod
    def new(cls, attr_name, to_value, *children, **attrs):
        return super(SetCssElement, cls).new(
            attr_name, to_value, "CSS", *children, **attrs
        )


class SetXmlElement(SetElement):
    """Set element for XML attributes"""

    @classmethod
    def new(cls, attr_name, to_value, *children, **attrs):
        return super(SetXmlElement, cls).new(
            attr_name, to_value, "XML", *children, **attrs
        )
