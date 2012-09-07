#!/usr/bin/env python
# encoding: utf-8
"""
Ingest a folder of PDFs that originated from ADS, but now link them to ADS
and ingest into BibDesk.

Requirements
------------

1. You need the program pdf2json (http://code.google.com/p/pdf2json/) to use
this script. The easiest way to get pdf2json and its dependencies is through
Homebrew, the Mac package manager: http://mxcl.github.com/homebrew/
Once homebrew is setup, simply run "brew install pdf2json"

2. You also need both this script (ads_pdf_ingest.py) and the ADS to BibDesk
command line interface (adsbibdesk.py) to be somewhere in your path.
/usr/bin/local works, for example.

Usage
----

    ads_pdf_ingest.py my_pdf_dir/

where 'my_pdf_dir' is full of PDFs you want to add to BibDesk with ADS
metadata.

2012-09-06 - Created by Jonathan Sick (jonathansick@mac.com; @jonathansick)
"""

import re
import os
import glob
import sys
import subprocess
import time


def main():
    workDir = sys.argv[1]
    print "Searching", workDir
    pdfPaths = glob.glob(os.path.join(workDir, "*.pdf"))
    grabber = PDFDOIGrabber()
    for i, pdfPath in enumerate(pdfPaths):
        print "%i of %i" % (i+1, len(pdfPaths))
        dois = grabber.search(pdfPath)
        if len(dois) == 0:
            print "No DOIs for", pdfPath
        else:
            for doi in dois:
                print os.path.basename(pdfPath), "=",
                print doi
                subprocess.call("adsbibdesk.py %s" % doi, shell=True)
        # Pacing so ADS won't treat us like a reckless 'bot!
        time.sleep(15.)


class PDFDOIGrabber(object):
    """Converts PDFs to text (via pdf2json) and attempts to match all DOIs
    in that text.
    """
    def __init__(self):
        super(PDFDOIGrabber, self).__init__()
        regstr = r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
        self.pattern = re.compile(regstr)

    def search(self, pdfPath):
        """Return a list of DOIs in the text of the PDF at `pdfPath`"""
        jsonPath = os.path.splitext(pdfPath)[0] + ".json"
        if os.path.exists(jsonPath): os.remove(jsonPath)
        subprocess.call("pdf2json -q %s %s" % (pdfPath, jsonPath), shell=True)
        f = open(jsonPath, 'r')
        data = f.read()
        f.close()
        doiMatches = self.pattern.findall(data)
        if os.path.exists(jsonPath): os.remove(jsonPath)
        return doiMatches


if __name__ == '__main__':
    main()
