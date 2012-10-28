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
import re
import subprocess
from xml.etree import ElementTree


def main():
    rel_path = lambda path: os.path.join(os.path.dirname(__file__), path)
    servicePath = rel_path("build/Add to BibDesk.workflow/Contents/document.wflow")
    appPath = rel_path("build/ADS to BibDesk.app/Contents/document.wflow")
    builtPyPath = rel_path("build/adsbibdesk/adsbibdesk.py")
    origPyPath = rel_path("adsbibdesk.py")
    injectorScptPath = rel_path("adsbibdesk_injector.applescript")

    # embed applescript into adsbibdesk.py script
    f = open(origPyPath, 'r')
    tmp = f.read()[:-1]
    tmp = re.sub('==SCPT==', compress(open(injectorScptPath).read()).strip(), tmp)
    f.close()
    if os.path.exists(builtPyPath): os.remove(builtPyPath)
    f = open(builtPyPath, 'w')
    f.write(tmp)
    f.close()
    # Executable as a CLI interface for ADS to BibDesk unto its own
    subprocess.call("chmod +x %s" % builtPyPath, shell=True)

    for workflow in (servicePath, appPath):
        xml = ElementTree.fromstring(open(workflow).read())
        for arr in xml.find('dict').find('array').getchildren():

            # fetch Python and AppleScript code inside the xml
            py = [c for c in arr.find('dict').getchildren()
                 if c.tag == 'dict' and
                 any([i.text and '/usr/bin/env' in i.text for i in c.getchildren()])]

            # rewrite with current files
            if py:
                py[0].find('string').text = open(builtPyPath).read()

        open(workflow, 'w').write(ElementTree.tostring(xml))


def compress(obj):
    import binascii, zlib
    return binascii.b2a_base64(zlib.compress(obj))

if __name__ == '__main__':
    main()
