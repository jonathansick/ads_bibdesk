#!/usr/bin/env python
# encoding: utf-8
"""
Ingest a folder of PDFs that originated from ADS, but now link them to ADS
and ingest into BibDesk.

2012-09-06 - Created by Jonathan Sick
"""

import re
import os
import glob
import sys
import subprocess


def main():
    workDir = sys.argv[1]
    print workDir
    pdfPaths = glob.glob(os.path.join(workDir, "*.pdf"))
    grabber = PDFDOIGrabber()
    for pdfPath in pdfPaths:
        dois = grabber.search(pdfPath)
        if len(dois) == 0:
            print "No DOIs for", pdfPath
        else:
            for doi in dois:
                print os.path.basename(pdfPath),
                print doi
                subprocess.call("python adsbibdesk.py %s" % doi, shell="True")


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
