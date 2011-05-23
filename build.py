#!/usr/bin/env python

__author__ = 'Rui Pereira <rui.pereira@gmail.com>'

import os
from xml.etree import ElementTree

workflow = os.path.join(os.path.dirname(__file__), 'Add to BibDesk.workflow/Contents/document.wflow')
xml = ElementTree.fromstring(open(workflow).read())
for arr in xml.find('dict').find('array').getchildren():

    # fetch Python and AppleScript code inside the xml
    py = [c for c in arr.find('dict').getchildren()
         if c.tag == 'dict' and
         any([i.text and '/usr/bin/env' in i.text for i in c.getchildren()])]

    ascript = [c for c in arr.find('dict').getchildren()
               if c.tag == 'dict' and
               any([i.text and 'AppleScript' in i.text for i in c.getchildren()])]

    # rewrite with current files
    if py:
        py[0].find('string').text = open('adsbibdesk.py').read()
    elif ascript:
        ascript[0].find('string').text = open('adsbibdesk.applescript').read()

open(workflow, 'w').write(ElementTree.tostring(xml))
