#!/usr/bin/env python
# ADS to BibDesk -- frictionless import of ADS publications into BibDesk
# Copyright (C) 2011  Rui Pereira <rui.pereira@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Rui Pereira <rui.pereira@gmail.com>'

import os
from xml.etree import ElementTree


def main():
    rel_path = lambda path: os.path.join(os.path.dirname(__file__), path)
    service_path = rel_path(os.path.join("build", "Add to BibDesk.workflow",
        "Contents", "document.wflow"))
    app_path = rel_path(os.path.join("build", "ADS to BibDesk.app", "Contents",
        "document.wflow"))
    py_path = rel_path("adsbibdesk.py")

    for workflow in (service_path, app_path):
        xml = ElementTree.fromstring(open(workflow).read())
        for arr in xml.find('dict').find('array').getchildren():

            # fetch Python code inside the xml
            py = [c for c in arr.find('dict').getchildren()
                 if c.tag == 'dict' and
                 any([i.text and '/usr/bin/env' in i.text
                     for i in c.getchildren()])]

            # rewrite with current file
            if py:
                py[0].find('string').text = open(py_path).read()

        open(workflow, 'w').write(ElementTree.tostring(xml))


if __name__ == '__main__':
    main()
