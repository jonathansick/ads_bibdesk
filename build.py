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
from xml.etree import ElementTree

def compress(obj):
    import binascii, zlib
    return binascii.b2a_base64(zlib.compress(obj))

if __name__ == '__main__':

    service = os.path.join(os.path.dirname(__file__), 'build/Add to BibDesk.workflow/Contents/document.wflow')
    app = os.path.join(os.path.dirname(__file__), 'build/ADS to BibDesk.app/Contents/document.wflow')
    update_arxiv = os.path.join(os.path.dirname(__file__), 'update_bibdesk_arxiv.sh')

    # embed applescript into adsbibdesk.py script
    f = open('adsbibdesk.py', 'r')
    tmp = f.read()[:-1]
    tmp = re.sub('==SCPT==', compress(open('adsbibdesk_injector.applescript').read()).strip(), tmp)
    f.close()
    if os.path.exists('build/adsbibdesk/adsbibdesk.py'): os.remove('build/adsbibdesk/adsbibdesk.py')
    f = open('build/adsbibdesk/adsbibdesk.py', 'w')
    f.write(tmp)
    f.close()

    for workflow in (service, app):
        xml = ElementTree.fromstring(open(workflow).read())
        for arr in xml.find('dict').find('array').getchildren():

            # fetch Python and AppleScript code inside the xml
            py = [c for c in arr.find('dict').getchildren()
                 if c.tag == 'dict' and
                 any([i.text and '/usr/bin/env' in i.text for i in c.getchildren()])]

            # rewrite with current files
            if py:
                py[0].find('string').text = open('adsbibdesk.py').read()

        open(workflow, 'w').write(ElementTree.tostring(xml))

    # replace into update arxiv script
    # TODO updated .sh script will be deprecated
    # tmp = open(update_arxiv).read()[:-1]
    # tmp = re.sub('(?<=py=").*(?="\n)', compress(open('adsbibdesk_built.py').read()).strip(), tmp)
    # tmp = re.sub('(?<=scpt=").*(?="\n)', compress(open('adsbibdesk.applescript').read()).strip(), tmp)
    # print >> open(update_arxiv, 'w'), tmp
