#!/usr/bin/env python

__author__ = 'Rui Pereira <rui.pereira@gmail.com>'

import os
import re
from xml.etree import ElementTree

def compress(obj):
    import binascii, zlib, cPickle
    return binascii.b2a_base64(zlib.compress(cPickle.dumps(obj, protocol=-1)))

if __name__ == '__main__':

    service = os.path.join(os.path.dirname(__file__), 'Add to BibDesk.workflow/Contents/document.wflow')
    app = os.path.join(os.path.dirname(__file__), 'Add to BibDesk App.app/Contents/document.wflow')
    update_arxiv = os.path.join(os.path.dirname(__file__), 'update_bibdesk_arxiv.sh')

    for workflow in (service, app):
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
                ascript[0].find('string').text = open('adsbibdesk.scpt').read()

        open(workflow, 'w').write(ElementTree.tostring(xml))

    # replace into update arxiv script
    tmp = open(update_arxiv).read()
    tmp = re.sub('(?<=py=").*(?="\n)', compress(open('adsbibdesk.py').read()).strip(), tmp)
    tmp = re.sub('(?<=scpt=").*(?="\n)', compress(open('adsbibdesk.scpt').read()).strip(), tmp)
    print >> open(update_arxiv, 'w'), tmp
    