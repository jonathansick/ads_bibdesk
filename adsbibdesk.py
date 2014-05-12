#!/usr/bin/env python
"""
ADS to BibDesk -- frictionless import of ADS publications into BibDesk
Copyright (C) 2014  Rui Pereira <rui.pereira@gmail.com> and
                    Jonathan Sick <jonathansick@mac.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Based on ADS to Bibdesk automator action by
Jonathan Sick, jonathansick@mac.com, August 2007

Input may be one of the following:
- ADS abstract page URL
- ADS bibcode
- arXiv abstract page
- arXiv identifier
"""
import datetime
import difflib
import fnmatch
import glob
import logging
import math
import optparse
import os
import pprint
import re
import socket
import sys
import tempfile
import time

# cgi.parse_qs is deprecated since 2.6
# but OS X 10.5 only has 2.5
import cgi
import urllib2
import urlparse

import subprocess as sp
try:
    import AppKit
except ImportError:
    # is this not the system python?
    syspath = eval(sp.Popen('/usr/bin/python -c "import sys; print(sys.path)"',
                            shell=True, stdout=sp.PIPE).stdout.read())
    for p in syspath:
        if os.path.isdir(p) and glob.glob(os.path.join(p, '*AppKit*')):
            sys.path.insert(0, p)
            break

    # retry
    try:
        import AppKit
    except ImportError:
        import webbrowser
        url = 'http://pythonhosted.org/pyobjc/install.html'
        msg = 'Please install PyObjC...'
        print msg
        sp.call(r'osascript -e "tell application \"System Events\" to '
                'display dialog \"%s\" buttons {\"OK\"} default button \"OK\""'
                % msg, shell=True, stdout=open('/dev/null', 'w'))
        # open browser in PyObjC install page
        webbrowser.open(url)
        sys.exit()

from HTMLParser import HTMLParser, HTMLParseError
from htmlentitydefs import name2codepoint

# default timeout for url calls
socket.setdefaulttimeout(30)

VERSION = "3.2.0"


def main():
    """Parse options and launch main loop"""
    usage = """Usage: %prog [options] [article_token or pdf_directory]

adsbibdesk helps you add astrophysics articles listed on NASA/ADS
and arXiv.org to your BibDesk database. There are three modes
in this command line interface:

1. Article mode, for adding single papers to BibDesk given tokens.
2. PDF Ingest mode, where PDFs in a directory are analyzed and added to
   BibDesk with ADS meta data.
3. Pre-print Update mode, for updating arXiv pre-prints automatically
   with newer bibcodes.

In article mode, adsbibdesk accepts many kinds of article tokens:
 - the URL of an ADS or arXiv article page,
 - the ADS bibcode of an article (e.g. 1998ApJ...500..525S), or
 - the arXiv identifier of an article (e.g. 0911.4956).
(Example: `adsbibdesk 1998ApJ...500..525S`)

In PDF Ingest mode, you specify a directory containing PDFs instead of
an article token (Example: `adsbibdesk -p pdfs` will ingest PDFs from
the pdfs/ directory).

In Pre-print Update mode, every article with an arXiv bibcode will be
updated if it has a new bibcode."""
    epilog = "For more information, visit www.jonathansick.ca/adsbibdesk" \
        " email jonathansick at mac.com or tweet @jonathansick"
    parser = optparse.OptionParser(usage=usage, version=VERSION,
                                   epilog=epilog)
    parser.add_option(
        '-d', '--debug',
        dest="debug", default=False, action="store_true",
        help="Debug mode; prints extra statements")
    parser.add_option(
        '-o', '--only_pdf',
        default=False, action='store_true',
        help="Download and open PDF for the selected [article_token].")

    pdf_ingest_group = optparse.OptionGroup(parser, "PDF Ingest Mode",
                                            description=None)
    pdf_ingest_group.add_option(
        '-p', '--ingest_pdfs',
        dest="ingest_pdfs", default=False, action="store_true",
        help="Ingest a folder of PDFs."
             " Positional argument should be directory"
             " containing PDFs."
             " e.g., `adsbibdesk -p .` for the current directory")
    pdf_ingest_group.add_option(
        '-r', '--recursive',
        dest='recursive', action="store_true",
        help="Search for PDFs recursively in the directory tree.")
    parser.add_option_group(pdf_ingest_group)

    arxiv_update_group = optparse.OptionGroup(parser, "Pre-print Update Mode",
                                              description=None)
    arxiv_update_group.add_option(
        '-u', '--update_arxiv',
        default=False, action="store_true",
        help='Check arXiv pre-prints for updated bibcodes')
    arxiv_update_group.add_option(
        '-f', '--from_date',
        help='MM/YY date of publication from which to start updating arXiv')
    arxiv_update_group.add_option(
        '-t', '--to_date',
        help='MM/YY date of publication up to which update arXiv')
    parser.add_option_group(arxiv_update_group)
    options, args = parser.parse_args()

    # Get preferences from (optional) config file
    prefs = Preferences()
    # inject options into preferences for later reference
    prefs['options'] = options.__dict__
    if options.debug:
        prefs['debug'] = True

    # Logging saves to log file on when in DEBUG mode
    # Always prints to STDOUT as well
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)s %(levelname)s %(message)s',
        filename=prefs['log_path'])
    if not prefs['debug']:
        logging.getLogger('').setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(ch)

    logging.info("Starting ADS to BibDesk")
    logging.debug("ADS to BibDesk version %s" % VERSION)
    logging.debug("Python: %s", sys.version)

    # Launch the specific workflow
    if options.ingest_pdfs:
        ingest_pdfs(options, args, prefs)
    elif options.only_pdf:
        # short-circuit process_articles
        # since BibDesk is not needed
        # FIXME smells like a refactor
        process_token(args[0], prefs, None)
    elif options.update_arxiv:
        update_arxiv(options, prefs)
    else:
        process_articles(args, prefs)


def process_articles(args, prefs, delay=15):
    """Workflow for processing article tokens and running process_token()
    to add the article to BibDesk.
    """
    # FIXME is there ever actually a case where args is None?
    if args:
        article_tokens = list(args)
    else:
        # Try to use standard input
        article_tokens = [s.strip() for s in sys.stdin.readlines()
                          if s.strip()]

    # AppKit hook for BibDesk
    bibdesk = BibDesk()

    for article_token in article_tokens:
        try:
            process_token(article_token, prefs, bibdesk)
        except ADSException, err:
            logging.debug('%s failed - %s' % (article_token, err))
        if len(article_tokens) > 1 and article_token != article_tokens[-1]:
            time.sleep(delay)

    bibdesk.app.dealloc()


# FIXME this function needs to be refactored
def process_token(article_token, prefs, bibdesk):
    """Process a single article token from the user, adding it to BibDesk.

    Parameters
    ----------
    article_token : str
        Any user-supplied `str` token.
    prefs : :class:`Preferences`
        A `Preferences` instance.
    bibdesk : :class:`BibDesk`
        A `BibDesk` AppKit hook instance.
    """
    # Determine what we're dealing with
    # The goal is to get a URL into ADS
    logging.debug("process_token found article token %s", article_token)
    connector = ADSConnector(article_token, prefs)
    ads_parser = ADSHTMLParser(prefs=prefs)

    if isinstance(connector.ads_read, basestring):
        # parse the ADS HTML file
        ads_parser.parse(connector.ads_read)

    elif connector.ads_read and getattr(connector, 'bibtex') is not None:
        # parsed from arXiv - dummy ads info
        ads_parser.bibtex = connector.bibtex
        ads_parser.arxivid = ads_parser.bibtex.Eprint
        ads_parser.author = ads_parser.bibtex.Author.split(' and ')
        ads_parser.title = ads_parser.bibtex.Title
        ads_parser.abstract = ads_parser.bibtex.Abstract
        ads_parser.comment = ads_parser.bibtex.AdsComment
        # original URL where we *should* have gotten the info
        ads_parser.bibtex.AdsURL = connector.ads_url
        # inject arXiv mirror into ArXivURL
        if 'arxiv_mirror' in prefs and prefs['arxiv_mirror']:
            tmpurl = urlparse.urlsplit(ads_parser.bibtex.ArXivURL)
            ads_parser.bibtex.ArXivURL = urlparse.urlunsplit(
                (tmpurl.scheme,
                 prefs['arxiv_mirror'],
                 tmpurl.path, tmpurl.query,
                 tmpurl.fragment))
        # link for PDF download
        try:
            link = [l.get('href', '') for l in ads_parser.bibtex.info['link']
                    if l.get('title') == 'pdf'][0]
            ads_parser.links = {'preprint': link}
        except IndexError:
            logging.debug("process_token could not find preprint PDF link")
            pass

    elif connector.ads_read is None:
        logging.debug("process_token skipping %s", article_token)
        return False

    # get PDF first
    pdf = ads_parser.get_pdf()

    # TODO refactor this out into a 'show_pdf' function
    if prefs['options'].get('only_pdf'):
        if not pdf.endswith('.pdf'):
            return False
        # just open PDF
        reader = ('pdf_reader' in prefs and
                  prefs['pdf_reader'] is not None) and \
            prefs['pdf_reader'] or 'Finder'
        app = AppKit.NSAppleScript.alloc()
        app.initWithSource_(
            'tell application "%s" '
            'to open ("%s" as POSIX file)' % (reader, pdf)).\
            executeAndReturnError_(None)
        # get name of the used viewer
        # (Finder may be defaulted to something else than Preview)
        if reader == 'Finder':
            reader = app.initWithSource_(
                'return name of (info for (path to frontmost application))').\
                executeAndReturnError_(None)[0].stringValue()
        logging.debug('opening %s with %s' % (pdf, reader))
        if 'skim' in reader.lower():
            time.sleep(1)  # give it time to open
            app.initWithSource_(
                'tell application "%s" to set view settings '
                'of first document to {auto scales:true}'
                % reader).executeAndReturnError_(None)
        app.dealloc()
        return True

    # search for already existing publication
    # with exactly the same title and first author
    # match title and first author using fuzzy string comparison
    # FIXME put cutoff into preferences; could be related to problems
    # FIXME refactor this out
    found = difflib.get_close_matches(
        ads_parser.title, bibdesk.titles,
        n=1, cutoff=.7)
    kept_pdfs = []
    kept_fields = {}
    # first author is the same
    if found and difflib.SequenceMatcher(
            None,
            bibdesk.authors(bibdesk.pid(found[0]))[0],
            ads_parser.author[0]).ratio() > .6:
        # further comparison on abstract
        abstract = bibdesk('abstract', bibdesk.pid(found[0])).stringValue()
        if not abstract or difflib.SequenceMatcher(
                None, abstract,
                ads_parser.abstract).ratio() > .6:
            pid = bibdesk.pid(found[0])
            # keep all fields for later comparison
            # (especially rating + read bool)
            kept_fields = dict((k, v) for k, v in
                               zip(bibdesk('return name of fields', pid, True),
                               bibdesk('return value of fields', pid, True))
                               # Adscomment may be arXiv only
                               if k != 'Adscomment')
            # plus BibDesk annotation
            kept_fields['BibDeskAnnotation'] = bibdesk(
                'return its note', pid).stringValue()
            kept_pdfs += bibdesk.safe_delete(pid)
            notify('Duplicate publication removed',
                   article_token, ads_parser.title)
            bibdesk.refresh()

    # FIXME refactor out this bibdesk import code?
    # add new entry
    pub = bibdesk(
        'import from "%s"' % ads_parser.bibtex.__str__().
        replace('\\', r'\\').replace('"', r'\"'))
    # pub id
    pub = pub.descriptorAtIndex_(1).descriptorAtIndex_(3).stringValue()
    # automatic cite key
    bibdesk('set cite key to generated cite key', pub)

    # abstract
    if ads_parser.abstract.startswith('http://'):
        # old scanned articles
        bibdesk(
            'make new linked URL at end of linked URLs '
            'with data "%s"' % ads_parser.abstract, pub)
    else:
        bibdesk(
            'set abstract to "%s"'
            % ads_parser.abstract.replace('\\', r'\\').replace('"', r'\"'),
            pub)

    doi = bibdesk('value of field "doi"', pub).stringValue()
    if pdf.endswith('.pdf'):
        # register PDF into BibDesk
        bibdesk('add POSIX file "%s" to beginning of linked files' % pdf, pub)
        # automatic file name
        bibdesk('auto file', pub)
    elif 'http' in pdf and not doi:
        # URL for electronic version - only add it if no DOI link present
        # (they are very probably the same)
        bibdesk(
            'make new linked URL at end of linked URLs with data "%s"'
            % pdf, pub)

    # add URLs as linked URL if not there yet
    urls = bibdesk(
        'value of fields whose name ends with "url"',
        pub, strlist=True)
    urlspub = bibdesk('linked URLs', pub, strlist=True)
    for u in [u for u in urls if u not in urlspub]:
        bibdesk(
            'make new linked URL at end of linked URLs with data "%s"'
            % u, pub)

    # add old annotated files
    for kept_pdf in kept_pdfs:
        bibdesk('add POSIX file "%s" to end of linked files' % kept_pdf, pub)

    # re-insert custom fields
    bibdesk(
        'set its note to "%s"' % kept_fields.pop('BibDeskAnnotation', ''),
        pub)
    newFields = bibdesk('return name of fields', pub, True)
    for k, v in kept_fields.iteritems():
        if k not in newFields:
            bibdesk('set value of field "%s" to "%s"' % (k, v), pub)
    notify('New publication added',
           bibdesk('cite key', pub).stringValue(),
           ads_parser.title)


def ingest_pdfs(options, args, prefs):
    """Workflow for attempting to ingest a directory of PDFs into BibDesk.

    This workflow attempts to scape DOIs from the PDF text, which are then
    added to BibDesk using the usual `process_token` function.
    """
    assert len(args) == 1, "Please pass a path to a directory"
    pdf_dir = args[0]
    assert os.path.exists(pdf_dir) is True, "%s does not exist" % pdf_dir
    print "Searching", pdf_dir

    if options.recursive:
        # Recursive glob solution from
        # http://stackoverflow.com/a/2186565
        pdf_paths = []
        for root, dirnames, filenames in os.walk(pdf_dir):
            for filename in fnmatch.filter(filenames, '*.pdf'):
                pdf_paths.append(os.path.join(root, filename))
    else:
        pdf_paths = glob.glob(os.path.join(pdf_dir, "*.pdf"))

    # Process each PDF, looking for a DOI
    grabber = PDFDOIGrabber()
    found = []
    for i, pdf_path in enumerate(pdf_paths):
        dois = grabber.search(pdf_path)
        if not dois:
            logging.info(
                "%i of %i: no DOIs for %s"
                % (i + 1, len(pdf_paths), pdf_path))
        else:
            found.extend(dois)
            for doi in dois:
                logging.info(
                    "%i of %i: %s = %s"
                    % (i + 1, len(pdf_paths), os.path.basename(pdf_path), doi))

    # let process_articles inject everything
    if found:
        logging.info('Adding %i articles to BibDesk...' % len(found))
        process_articles(found, prefs)


def update_arxiv(options, prefs):
    """
    Workflow for updating arXiv pre-prints automatically with newer bibcodes.
    """
    assert options.from_date is None or \
        re.match('^\d{2}/\d{2}$', options.from_date) is not None, \
        '--from_date needs to be in MM/YY format'
    assert options.to_date is None or \
        re.match('^\d{2}/\d{2}$', options.to_date) is not None, \
        '--to_date needs to be in MM/YY format'

    def b2d(bibtex):
        """BibTex -> publication date"""
        m = re.search('Month = \{?(\w*)\}?', bibtex).group(1)
        y = re.search('Year = \{?(\d{4})\}?', bibtex).group(1)
        return datetime.datetime.strptime(m + y, '%b%Y')

    def recent(added, fdate, tdate):
        fromdate = fdate is not None and \
            datetime.datetime.strptime(fdate, '%m/%y')\
            or datetime.datetime(1900, 1, 1)
        todate = tdate is not None and \
            datetime.datetime.strptime(tdate, '%m/%y')\
            or datetime.datetime(3000, 1, 1)
        return fromdate <= added <= todate

    # frontmost opened BibDesk document
    bibdesk = BibDesk()
    ids = []

    # check for adsurl containing arxiv or astro.ph bibcodes
    arxiv = bibdesk(
        'return publications whose '
        '(value of field "Adsurl" contains "arXiv") or '
        '(value of field "Adsurl" contains "astro.ph")')

    if arxiv.numberOfItems():
        # extract arxiv id from the ADS url
        ids = [u.split('bib_query?')[-1].split('abs/')[-1] for u in
               bibdesk(
                   'tell publications whose '
                   '(value of field "Adsurl" contains "arXiv") or '
                   '(value of field "Adsurl" contains "astro.ph") '
                   'to return value of field "Adsurl"', strlist=True)]
        dates = [b2d(b) for b in
                 bibdesk(
                     'tell publications whose '
                     '(value of field "Adsurl" contains "arXiv") or '
                     '(value of field "Adsurl" contains "astro.ph") '
                     'to return bibtex string', strlist=True)]
        # arxiv ids to search
        ids = [b for d, b in zip(dates, ids)
               if recent(d, options.from_date, options.to_date)]

    bibdesk.app.dealloc()

    if not ids:
        print 'Nothing to update!'
        sys.exit()
    else:
        n = len(ids)
        t = math.ceil(n * 15. / 60.)
        if t > 1:
            time_unit = "minutes"
        else:
            time_unit = "minute"
        logging.info('Checking %i arXiv entries for changes...' % n)
        logging.info(
            '(to prevent ADS flooding this will take a while, '
            'check back in around %i %s)' % (t, time_unit))

    changed = []
    for n, i in enumerate(ids):
        # sleep for 15 seconds, to prevent ADS flooding
        time.sleep(15)
        logging.debug("arxiv id %s" % i)
        # these are ADS bibcodes by default
        adsURL = urlparse.urlunsplit(
            ('http', prefs['ads_mirror'],
             'cgi-bin/bib_query', i, ''))
        logging.debug("adsURL %s" % adsURL)
        # parse the ADS HTML file
        ads_parser = ADSHTMLParser(prefs=prefs)
        try:
            ads_parser.parse_at_url(adsURL)
        except ADSException, err:
            logging.debug('%s update failed: %s' % (i, err))
            continue
        logging.debug("ads.bibtex %s" % ads_parser.bibtex)
        if ads_parser.bibtex is None:  # ADSHTMLParser failed
            logging.debug("FAILURE: ads.bibtex is None!")
            continue
        if ads_parser.bibtex.bibcode != i:
            logging.info(
                '%i. %s has become %s'
                % (n + 1, i, ads_parser.bibtex.bibcode))
            changed.append(i)
        else:
            logging.info('%i. %s has not changed' % (n + 1, i))
            continue

    # run changed entries through the main loop
    if changed and raw_input(
            'Updating %i entries, continue? (y/[n]) '
            % len(changed)) in ('Y', 'y'):
        logging.info(
            '(to prevent ADS flooding, we will wait for a while '
            'between each update, so go grab a coffee)')
        process_articles(changed, prefs)
    elif not changed:
        logging.info('Nothing to update!')


def notify(title, subtitle, desc, sticky=False):
    """Publish a notification to Notification Center

    Adaptation of original by Moises Aranas
    https://github.com/maranas/pyNotificationCenter
    """
    try:
        import objc
        notification = objc.lookUpClass('NSUserNotification').alloc().init()
        notification.setTitle_(title)
        notification.setInformativeText_(desc)
        notification.setSubtitle_(subtitle)
        objc.lookUpClass('NSUserNotificationCenter').\
            defaultUserNotificationCenter().scheduleNotification_(notification)
        notification.dealloc()
    # this will be either ImportError or objc.nosuchclass_error
    except Exception:
        # revert to growl
        if subtitle:
            desc = subtitle + ': ' + desc
        growl_notify(title, desc, sticky)


def growl_notify(title, desc, sticky=False):
    title = title.replace('"', r'\"')
    desc = desc.replace('"', r'\"')
    # http://bylr.net/3/2011/09/applescript-and-growl/
    # is growl running?
    app = AppKit.NSAppleScript.alloc()
    growl = app.initWithSource_(
        'tell application "System Events" to return '
        'processes whose creator type contains "GRRR"').\
        executeAndReturnError_(None)[0]
    if growl.numberOfItems():
        growlapp = growl.descriptorAtIndex_(1).descriptorAtIndex_(3).\
            stringValue()
        # register
        app.initWithSource_(
            'tell application "%s" to register as '
            'application "BibDesk" '
            'all notifications {"BibDesk notification"} '
            'default notifications {"BibDesk notification"}'
            % growlapp).executeAndReturnError_(None)
        # and notify
        app.initWithSource_(
            'tell application "%s" to notify with name '
            '"BibDesk notification" application name "BibDesk" '
            'priority 0 title "%s" description "%s" %s'
            % (growlapp, title, desc, "with sticky" if sticky else '')).\
            executeAndReturnError_(None)
    app.dealloc()


def has_annotationss(f):
    return sp.Popen(
        "strings %s | grep  -E 'Contents[ ]{0,1}\('" % f,
        shell=True, stdout=sp.PIPE,
        stderr=open('/dev/null', 'w')).stdout.read() != ''


def get_redirect(url):
    """Utility function to intercept final URL of HTTP redirection"""
    try:
        out = urllib2.urlopen(url)
    except urllib2.URLError, out:
        pass
    return out.geturl()


class PDFDOIGrabber(object):
    """Converts PDFs to text and attempts to match all DOIs"""
    def __init__(self):
        super(PDFDOIGrabber, self).__init__()
        regstr = r'(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>\)\.,])\S)+)'
        self.pattern = re.compile(regstr)

    def search(self, pdfPath):
        """Return a list of DOIs in the text of the PDF at `pdfPath`"""
        json_path = os.path.splitext(pdfPath)[0] + ".json"
        if os.path.exists(json_path):
            os.remove(json_path)
        sp.call('pdf2json -q "%s" "%s"' % (pdfPath, json_path), shell=True)
        data = open(json_path, 'r').read()
        doi_matches = self.pattern.findall(data)
        if os.path.exists(json_path):
            os.remove(json_path)

        # strings can find some stuff that pdf2json does not
        if not doi_matches:
            data = sp.Popen(
                "strings %s" % pdfPath,
                shell=True, stdout=sp.PIPE,
                stderr=open('/dev/null', 'w')).stdout.read()
            doi_matches = self.pattern.findall(data)

        return list(set(doi_matches))


class ADSConnector(object):
    """Receives input (token), derives an ADS url, and attempts to connect
    to the corresponding ADS abstract page with urllib2.urlopen().

    Tokens are tested in order of:

    - arxiv identifiers
    - bibcodes / digital object identifier (DOI)
    - ADS urls
    - arxiv urls
    """
    def __init__(self, token, prefs):
        super(ADSConnector, self).__init__()
        self.token = str(token)
        self.prefs = prefs
        self.ads_url = None  # string URL to ADS
        self.ads_read = None  # a urllib2.urlopen connection to ADS
        self.url_parts = urlparse.urlsplit(token)  # supposing it is a URL

        # An arXiv identifier or URL?
        if self._is_arxiv():
            logging.debug("ADSConnector found arXiv ID %s", self.token)
            # Try to open the ADS page
            if not self._read(self.ads_url):
                # parse arxiv instead:
                logging.debug('ADS page (%s) not found for %s' %
                              (self.ads_url, self.token))
                notify('ADS page not found', self.token,
                       'Parsing the arXiv page...')
                arxiv_bib = ArXivParser()
                try:
                    arxiv_bib.parse_at_id(self.arxiv_id)
                    logging.debug(
                        "arXiv page (%s) parsed for %s"
                        % (arxiv_bib.url, self.token))
                except ArXivException, err:
                    logging.debug("ADS and arXiv failed, you're in trouble...")
                    raise ADSException(err)

                # dummy ads_read and bibtex
                self.ads_read = True
                self.bibtex = arxiv_bib

        # A bibcode from ADS?
        elif not self.url_parts.scheme and self._is_bibcode():
            logging.debug("ADSConnector found bibcode/DOI %s", self.token)
        else:
            # If the path lacks http://, tack it on because
            # the token *must* be a URL now
            if not self.token.startswith("http://"):
                self.token = 'http://' + self.token
            # supposing it is a URL
            self.url_parts = urlparse.urlsplit(self.token)

            # An abstract page at any ADS mirror site?
            if self.url_parts.netloc in self.prefs.adsmirrors \
                    and self._is_ads_page():
                logging.debug("ADSConnector found ADS page %s", self.token)

    def _is_arxiv(self):
        """Try to classify the token as an arxiv article, either:

        - new style (YYMM.NNNN), or
        - old style (astro-ph/YYMMNNN)

        :return: True if ADS page is recovered
        """
        arxiv_pattern = re.compile('(\d{4,6}\.\d{4,6}|astro\-ph/\d{7})')
        arxiv_matches = arxiv_pattern.findall(self.token)
        if len(arxiv_matches) == 1:
            self.arxiv_id = arxiv_matches[0]
            self.ads_url = urlparse.urlunsplit((
                'http',
                self.prefs['ads_mirror'],
                'cgi-bin/bib_query',
                'arXiv:%s' % self.arxiv_id, ''))
            return True
        else:
            self.arxiv_id = None
            return False

    def _is_bibcode(self):
        """Test if the token corresponds to an ADS bibcode or DOI"""
        self.ads_url = urlparse.urlunsplit((
            'http', self.prefs['ads_mirror'],
            'doi/%s' % self.token, '', ''))
        read = self._read(self.ads_url)
        if read:
            return read
        else:
            self.ads_url = urlparse.urlunsplit((
                'http',
                self.prefs['ads_mirror'], 'abs/%s' % self.token, '', ''))
            read = self._read(self.ads_url)
            return read

    def _is_ads_page(self):
        """Test if the token is a url to an ADS abstract page"""
        # use our ADS mirror
        url = self.url_parts
        self.ads_url = urlparse.urlunsplit((
            url.scheme,
            self.prefs['ads_mirror'],
            url.path, url.query, url.fragment))
        return self._read(self.ads_url)

    def _read(self, ads_url):
        """Attempt a connection to ads_url, saving the read to
        self.ads_read.

        :return: True if successful, False otherwise
        """
        try:
            # remove <head>...</head> - often broken HTML
            self.ads_read = re.sub(
                r'<head>[\s\S]*</head>', '',
                urllib2.urlopen(ads_url).read())
            return True
        except urllib2.HTTPError:
            return False


class Preferences(object):
    """Manages the preferences on disk and in memory. Preferences are accessed
    with by a dictionary-like interface.
    """

    def __init__(self):
        self.prefs_path = os.path.expanduser('~/.adsbibdesk')
        self._adsmirrors = ['adsabs.harvard.edu',
                            'cdsads.u-strasbg.fr',
                            'ukads.nottingham.ac.uk',
                            'esoads.eso.org',
                            'ads.ari.uni-heidelberg.de',
                            'ads.inasan.ru',
                            'ads.mao.kiev.ua',
                            'ads.astro.puc.cl',
                            'ads.on.br',
                            'ads.nao.ac.jp',
                            'ads.bao.ac.cn',
                            'ads.iucaa.ernet.in',
                            'www.ads.lipi.go.id']

        self.prefs = self._get_default_prefs()  # Hard coded defaults dict
        new_prefs = self._get_prefs()  # load user prefs from disk
        self.prefs.update(new_prefs)  # override defaults with user prefs
        self._keys = self.prefs.keys()
        self._iter_index = -1

    def __getitem__(self, key):
        return self.prefs[key]

    def __setitem__(self, key, value):
        self.prefs[key] = value
        self._keys = self.prefs.keys()

    def __iter__(self):
        return self

    def next(self):
        if self._iter_index == len(self._keys) - 1:
            self._iter_index = -1
            raise StopIteration
        self._iter_index += 1
        return self._keys[self._iter_index]

    def _get_default_prefs(self):
        """:return: a dictionary of the full set of default preferences. This
        is done in case the user's preference file is missing a key-value pair.
        """
        return {"ads_mirror": "adsabs.harvard.edu",
                "arxiv_mirror": None,
                "download_pdf": True,
                "pdf_reader": None,
                "ssh_user": None,
                "ssh_server": None,
                "debug": False,
                "log_path": os.path.expanduser("~/.adsbibdesk.log")}

    def _get_prefs(self):
        """Read preferences files from `self.prefs_path`, creates one
        otherwise.
        """
        prefs = {}
        # create a default preference file if non existing
        if not os.path.exists(self.prefs_path):
            self._write_default_prefs()

        for l in open(self.prefs_path):
            if l.strip() and not l.strip().startswith('#'):
                if '=' not in l:
                    # badly formed setting
                    continue
                k, v = l.strip().split('=')
                if not v:
                    v = None
                elif v.strip().lower() in ('true', 'yes'):
                    v = True
                elif v.strip().lower() in ('false', 'no'):
                    v = False
                elif v.strip().lower() == 'none':
                    v = None
                prefs[k] = v

        return prefs

    def _write_default_prefs(self):
        """
        Set a default preferences file (~/.adsbibdesk)
        """
        prefs = open(self.prefs_path, 'w')
        print >> prefs, """# ADS mirror
ads_mirror=%s

# arXiv mirror
# (leave it unset to use the arXiv mirror pointed by your ADS mirror)
arxiv_mirror=%s

# download PDFs?
download_pdf=%s

# set these to use your account on a remote machine for fetching
# (refereed) PDF's you have no access locally
ssh_user=%s
ssh_server=%s""" % (self.prefs['ads_mirror'], self.prefs['arxiv_mirror'],
                    self.prefs['download_pdf'], self.prefs['ssh_user'],
                    self.prefs['ssh_server'])

        prefs.close()

    @property
    def adsmirrors(self):
        return self._adsmirrors


class BibTex(object):

    def __init__(self, url):
        """
        Create BibTex instance from ADS BibTex URL
        """
        bibtex = urllib2.urlopen(url).readlines()
        bibtex = ' '.join([l.strip() for l in bibtex]).strip()
        bibtex = bibtex[re.search('@[A-Z]+\{', bibtex).start():]
        self.type, self.bibcode, self.info = self.parsebib(bibtex)

    def __str__(self):
        return (','.join(
            ['@' + self.type + '{' + self.bibcode] +
            ['%s=%s' % (i, j) for i, j in self.info.items()]) + '}').\
            encode('utf-8')

    def parsebib(self, bibtex):
        """
        Parse bibtex code into dictionary
        """
        r = re.search(
            '(?<=^@)(?P<type>[A-Z]+){(?P<bibcode>\S+)(?P<info>,.+)}$',
            bibtex)
        s = re.split('(,\s\w+\s=\s)', r.group('info'))
        info = dict(
            [(i[1:].replace('=', '').strip(), j.strip())
                for i, j in zip(s[1::2], s[2::2])])
        return r.group('type'), r.group('bibcode'), info


class BibDesk(object):
    def __init__(self):
        """
        Manage BibDesk publications using AppKit
        """
        self.app = AppKit.NSAppleScript.alloc()
        self.refresh()

    def __call__(self, cmd, pid=None, strlist=False, error=False):
        """
        Run AppleScript command on first document of BibDesk
        :param cmd: AppleScript command string
        :param pid: address call to first/last publication of document
        :param strlist: return output as list of string
        :param error: return full output of call, including error
        """
        if pid is None:
            # address all publications
            cmd = 'tell first document of application "BibDesk" to %s' % cmd
        else:
            # address a single publicatin
            cmd = 'tell first document of application "BibDesk" to '\
                  'tell first publication whose id is "%s" to %s' % (pid, cmd)
        output = self.app.initWithSource_(cmd).executeAndReturnError_(None)
        if not error:
            output = output[0]
            if strlist:
                # objective C nuisances...
                output = [output.descriptorAtIndex_(i + 1).stringValue()
                          for i in range(output.numberOfItems())]
        return output

    def refresh(self):
        # is there an opened document yet?
        if self('return name of first document '
                'of application "BibDesk"', error=True)[1] is not None:
            # create blank one
            self('tell application "BibDesk" to make new document')
        self.titles = self('return title of publications', strlist=True)
        self.ids = self('return id of publications', strlist=True)

    def pid(self, title):
        return self.ids[self.titles.index(title)]

    def authors(self, pid):
        """
        Get name of authors of publication
        """
        return self('name of authors', pid, strlist=True)

    def safe_delete(self, pid):
        """
        Safely delete publication + PDFs, taking into account
        the existence of PDFs with Skim notes
        """
        keptPDFs = []
        files = self('POSIX path of linked files', pid, strlist=True)
        notes = self('text Skim notes of linked files', pid, strlist=True)

        for f, n in zip([f for f in files if f is not None],
                        [n for n in notes if n is not None]):
            if f.lower().endswith('pdf'):
                if '_notes_' in f:
                    keptPDFs.append(f)
                else:
                    # check for annotations
                    if n or has_annotationss(f):
                        suffix = 1
                        path, ext = os.path.splitext(f)
                        backup = path + '_notes_%i.pdf' % suffix
                        while os.path.exists(backup):
                            suffix += 1
                            backup = path + '_notes_%i.pdf' % suffix
                        # rename
                        os.rename(f, backup)
                        keptPDFs.append(backup)
                        if os.path.exists(path + '.skim'):
                            os.rename(path + '.skim',
                                      path + '_notes_%i.skim' % suffix)
                    else:
                        # remove file
                        os.remove(f)
        # delete publication
        self('delete', pid)
        return keptPDFs


class ADSException(Exception):
    pass


class ADSHTMLParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self)
        self.links = {}
        self.tag = ''
        self.get_abs = False
        # None = not seen yet, False = seen but do not store yet, True = store
        self.get_comment = None
        self.entities = {}

        self.bibtex = None
        self.abstract = None
        self.comment = None
        self.title = ''
        self.author = []
        self.arxivid = None

        self.prefs = kwargs.get('prefs', Preferences()).prefs

    def mathml(self):
        """
        Generate dictionary with MathML -> unicode conversion from
        http://www.w3.org/Math/characters/byalpha.html
        """
        w3 = 'http://www.w3.org/Math/characters/byalpha.html'
        mathml = re.search('(?<=<pre>).+(?=</pre>)',
                           urllib2.urlopen(w3).read(), re.DOTALL).group()
        entities = {}
        for l in mathml[:-1].splitlines():
            s = l.split(',')
            # ignore double hex values like 'U02266-00338'
            if '-' not in s[1]:
                # hexadecimal -> int values, for unichr
                entities[s[0].strip()] = int(s[1].strip()[1:], 16)
        return entities

    def parse_at_url(self, url):
        """Helper method to read data from URL, and passes on to parse()."""
        try:
            html_data = urllib2.urlopen(url).read()
        except urllib2.URLError, err:
            logging.debug("ADSHTMLParser timed out on URL: %s", url)
            raise ADSException(err)
        self.parse(html_data)

    def parse(self, html_data):
        """
        Feed url into our own HTMLParser and parse found bibtex

        html_data is a string containing HTML data from ADS page.
        """
        self.feed(html_data)

        logging.debug("ADSHTMLParser found links: %s",
                      pprint.pformat(self.links))

        if 'bibtex' in self.links:
            self.bibtex = BibTex(self.links['bibtex'])
            self.title = re.search(
                '(?<={).+(?=})',
                self.bibtex.info['title']).group()\
                .replace('{', '').replace('}', '').encode('utf-8')
            self.author = [
                a.strip().encode('utf-8') for a in
                re.search('(?<={).+(?=})', self.bibtex.info['author'])
                .group().split(' and ')]
            # bibtex do not have the comment from ADS
            if self.comment:
                self.bibtex.info.update(
                    {'adscomment': '"' + self.comment.replace('"', "'") + '"'})
            # construct ArXivURL from arXiv identifier
            if self.arxivid:
                if 'arxiv_mirror' not in self.prefs \
                        or not self.prefs['arxiv_mirror']:
                    # test HTTP redirect to get the arXiv mirror used by ADS
                    try:
                        mirror = urlparse.urlsplit(
                            get_redirect(self.links['preprint'])).netloc
                    except KeyError:
                        mirror = 'arxiv.org'  # this should not happen
                else:
                    mirror = self.prefs['arxiv_mirror']
                url = urlparse.urlunsplit((
                    'http', mirror,
                    'abs/' + self.arxivid, None, None))
                self.bibtex.info.update({'arxivurl': '"' + url + '"'})

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'hr' and self.get_abs:
            # abstract
            self.abstract = self.tag.strip().decode('utf-8')
            self.get_abs = False
            self.tag = ''
        elif tag.lower() == 'img' and self.get_abs:
            # handle old scanned articles abstracts
            self.tag += dict(attrs)['src'].replace('&#38;', unichr(38))
        elif tag.lower() == 'a':
            # links
            if 'href' in dict(attrs):
                href = dict(attrs)['href'].replace('&#38;', unichr(38))
                query = cgi.parse_qs(urlparse.urlsplit(href).query)
                if 'bibcode' in query:
                    if 'link_type' in query:
                        self.links[query['link_type'][0].lower()] = href
                    elif 'data_type' in query:
                        self.links[query['data_type'][0].lower()] = href
        elif tag.lower() == 'td' and self.get_comment is False \
                and 'valign' in dict(attrs):
            # comment
            self.get_comment = True

    def handle_endtag(self, tag):
        if self.get_comment and tag.lower() == 'td':
            self.comment = self.tag.strip().decode('utf-8')
            self.get_comment = None
            self.tag = ''

    def handle_data(self, data):
        if self.get_abs:
            self.tag += data.replace('\n', ' ')
        if self.get_comment:
            self.tag += data

        # beginning of abstract found
        if data.strip() == 'Abstract':
            self.get_abs = True
        if data.strip() == 'Comment:':
            self.get_comment = False
        # store arXiv identifier
        # FIXME perhaps compile this regular expression as a global?
        if re.search('arXiv:(\d{4,6}.\d{4,6}|astro\-ph/\d{7})', data) \
                is not None:
            self.arxivid = re.search(
                'arXiv:(\d{4,6}.\d{4,6}|astro\-ph/\d{7})',
                data).group(1)

    # handle html entities
    def handle_entityref(self, name):
        if self.get_abs:
            if name in name2codepoint:
                c = name2codepoint[name]
                self.tag += unichr(c).encode('utf-8')
            else:
                # fetch mathml
                if not self.entities:
                    # cache dict
                    self.entities = self.mathml()
                if name in self.entities:
                    c = self.entities[name]
                    self.tag += unichr(c).encode('utf-8')
                else:
                    # nothing worked, leave it as-is
                    self.tag += '&' + name + ';'

    # handle unicode chars in utf-8
    def handle_charref(self, name):
        if self.get_abs:
            self.tag += unichr(int(name)).encode('utf-8')

    def get_pdf(self):
        """
        Fetch PDF and save it locally in a temporary file. Tries by order:

        - refereed article
        - refereed article using another machine (set ssh_user & ssh_server)
        - arXiv preprint
        - electronic journal link
        """
        if not self.links:
            return 'failed'
        elif 'download_pdf' in self.prefs and not self.prefs['download_pdf']:
            return 'not downloaded'

        def filetype(filename):
            return sp.Popen('file %s' % filename, shell=True,
                            stdout=sp.PIPE,
                            stderr=sp.PIPE).stdout.read()

        # refereed
        if 'article' in self.links:
            url = self.links['article']
            # Resolve URL
            resolved_url = get_redirect(url)
            logging.debug("Resolve article URL: %s" % resolved_url)
            if "filetype=.pdf" in resolved_url:
                # URL will directly resolve into a PDF
                pdf_url = resolved_url
            elif "MNRAS" in resolved_url:
                # Special case for MNRAS URLs to deal with iframe
                parser = MNRASParser(self.prefs)
                try:
                    parser.parse(url)
                except MNRASException:
                    # this probably means we have a PDF directly from ADS
                    # afterall just continue.
                    # NOTE this case may be deprecated by resolving the URL
                    pdf_url = resolved_url
                if parser.pdfURL is not None:
                    pdf_url = parser.pdfURL
                else:
                    pdf_url = resolved_url
            else:
                pdf_url = resolved_url

            # try locally
            fd, pdf = tempfile.mkstemp(suffix='.pdf')
            # test for HTTP auth need
            try:
                os.fdopen(fd, 'wb').write(urllib2.urlopen(pdf_url).read())
            except urllib2.URLError, err:  # HTTPError derives from URLError
                logging.debug('%s failed: %s' % (pdf_url, err))
                # dummy file
                open(pdf, 'w').write('dummy')

            if 'PDF document' in filetype(pdf):
                return pdf

            # try in remote server
            # you need to set SSH public key authentication for this to work!
            elif 'ssh_user' in self.prefs and self.prefs['ssh_user'] \
                    is not None:
                fd, pdf = tempfile.mkstemp(suffix='.pdf')
                cmd = 'ssh %s@%s \"touch adsbibdesk.pdf; ' \
                    'wget -O adsbibdesk.pdf \\"%s\\"\"' % \
                    (self.prefs['ssh_user'], self.prefs['ssh_server'], pdf_url)
                cmd2 = 'scp -q %s@%s:adsbibdesk.pdf %s' \
                    % (self.prefs['ssh_user'], self.prefs['ssh_server'], pdf)
                sp.Popen(cmd, shell=True,
                         stdout=sp.PIPE, stderr=sp.PIPE).communicate()
                sp.Popen(cmd2, shell=True,
                         stdout=sp.PIPE, stderr=sp.PIPE).communicate()
                if 'PDF document' in filetype(pdf):
                    return pdf

        # arXiv
        if 'preprint' in self.links:
            # arXiv page
            url = self.links['preprint']
            mirror = None

            # fetch PDF directly without parsing the arXiv page
            if self.arxivid is not None:
                # user defined mirror?
                if 'arxiv_mirror' not in self.prefs \
                        or not self.prefs['arxiv_mirror']:
                    # test HTTP redirect to get the arXiv mirror used by ADS
                    mirror = urlparse.urlsplit(get_redirect(url)).netloc
                else:
                    mirror = self.prefs['arxiv_mirror']
                url = urlparse.urlunsplit((
                    'http', mirror, 'pdf/' + self.arxivid, None, None))
                logging.debug('arXiv PDF (%s)' % url)

            else:
                # search for PDF link in the arXiv page
                # this should be *deprecated*
                for line in urllib2.urlopen(url):
                    if '<h1><a href="/">' in line:
                        mirror = re.search(
                            '<h1><a href="/">(.*ar[xX]iv.org)',
                            line)
                    elif 'dc:identifier' in line:
                        begin = re.search('dc:identifier="', line).end()
                        url = urlparse.urlsplit(
                            line[begin:-2].replace('&#38;', unichr(38)).
                            lower())
                        # use automatic mirror chosen by the ADS mirror
                        if ('arxiv_mirror' not in self.prefs
                                or not self.prefs['arxiv_mirror']) \
                                and mirror is not None:
                            url = urlparse.urlunsplit((
                                url.scheme,
                                mirror.group(1), url.path, url.query,
                                url.fragment))
                            break
                        elif self.prefs['arxiv_mirror']:
                            url = urlparse.urlunsplit((
                                url.scheme,
                                self.prefs['arxiv_mirror'],
                                url.path, url.query,
                                url.fragment))
                            break
                logging.debug(
                    'arXiv PDF url (*should be DEPRECATED!*): %s' % url)

            # get arXiv PDF
            fd, pdf = tempfile.mkstemp(suffix='.pdf')
            os.fdopen(fd, 'wb').write(urllib2.urlopen(
                url.replace('abs', 'pdf')).read())
            if 'PDF document' in filetype(pdf):
                return pdf
            # PDF was not yet generated in the mirror?
            elif '...processing...' in open(pdf).read():
                while '...processing...' in open(pdf).read():
                    logging.debug('waiting 30s for PDF regeneration')
                    notify('Waiting for arXiv...', '',
                           'PDF is being generated, retrying in 30s...')
                    time.sleep(30)
                    open(pdf, 'wb').write(urllib2.urlopen(
                        url.replace('abs', 'pdf')).read())
                if 'PDF document' in filetype(pdf):
                    return pdf
                else:
                    return url
            else:
                return url

        # electronic journal
        if 'ejournal' in self.links:
            return self.links['ejournal']

        return 'failed'


class ArXivException(Exception):
    pass


class ArXivParser(object):

    def __init__(self):
        """
        Parse arXiv information for a *single* arxiv_id

        :param arxiv_id: arXiv identifier
        """
        pass

    def parse_at_id(self, arxiv_id):
        """Helper method to read data from URL, and passes on to parse()."""
        from xml.etree import ElementTree
        self.url = 'http://export.arxiv.org/api/query?id_list=' + arxiv_id
        try:
            self.xml = ElementTree.fromstring(urllib2.urlopen(self.url).read())
        except (urllib2.HTTPError, urllib2.URLError), err:
            logging.debug("ArXivParser failed on URL: %s", self.url)
            raise ArXivException(err)
        self.info = self.parse(self.xml)
        self.bib = self.bibtex(self.info)  # FIXME looks like self.bib is None

    def parse(self, xml):
        # recursive xml -> list of (tag, info)
        getc = lambda e: [
            (c.tag.split('}')[-1], c.getchildren() and
                dict(getc(c)) or (c.text is not None and re.sub('\s+', ' ',
                                  c.text.strip()) or c.attrib))
            for c in e.getchildren()]

        # article info
        info = {}
        for k, v in getc(xml.getchildren()[-1]):  # last item is article
            if isinstance(v, dict):
                info.setdefault(k, []).append(v)
            else:
                info[k] = v
        return info

    def bibtex(self, info):
        """
        Create BibTex entry. Sets a bunch of "attributes" that are used
        explictly on __str__ as BibTex entries

        :param info: parsed info dict from arXiv
        """
        # TODO turn these into properties?
        self.Author = ' and '.join(
            ['{%s}, %s' % (a['name'].split()[-1],
                           '~'.join(a['name'].split()[:-1]))
             for a in info['author']
             if len(a['name'].strip()) > 1]).encode('utf-8')
        self.Title = info['title'].encode('utf-8')
        self.Abstract = info['summary'].encode('utf-8')
        self.AdsComment = info['comment'].replace('"', "'").encode('utf-8') \
            if 'comment' in info else ""
        self.Jornal = 'ArXiv e-prints'
        self.ArchivePrefix = 'arXiv'
        self.ArXivURL = info['id']
        self.Eprint = info['id'].split('abs/')[-1]
        self.PrimaryClass = info['primary_category'][0]['term']
        self.Year, self.Month = datetime.datetime.strptime(
            info['published'],
            '%Y-%m-%dT%H:%M:%SZ').strftime('%Y %b').split()

    def __str__(self):
        import string
        return '@article{%s,\n' % self.Eprint +\
            '\n'.join([
                '%s = {%s},' % (k, v)
                for k, v in
                sorted([(k, v.decode('utf-8'))
                        for k, v in self.__dict__.iteritems()
                        if k[0] in string.uppercase])]) +\
            '}'


class MNRASException(Exception):
    pass


class MNRASParser(HTMLParser):
    """Handle MNRAS refereed article PDFs.

    Unlike other journals, the ADS "Full Refereed Journal Article" URL for a
    MNRAS article points to a PDF embedded in an iframe. This class extracts
    the PDF url given the ADS link.
    """
    def __init__(self, prefs):
        HTMLParser.__init__(self)
        self.prefs = prefs
        self.pdf_url = None

    def parse(self, url):
        """Parse URL to MNRAS PDF from MNRAS article page.
        """
        try:
            # Detect and decode page's charset
            logging.debug("Parsing MNRAS url %s" % url)
            connection = urllib2.urlopen(url)
            encoding = connection.headers.getparam('charset')
            if encoding is not None:
                logging.debug("Detected MNRAS encoding %s" % encoding)
                page = connection.read().decode(encoding)
                self.feed(page)
            else:
                logging.debug("No detected MNRAS encoding")
                page = connection.read()
                self.feed(page)
        except urllib2.URLError, err:  # HTTP timeout
            logging.debug("MNRASParser timed out: %s", url)
            raise MNRASException(err)
        except HTMLParseError, err:
            raise MNRASException(err)

    def handle_starttag(self, tag, attrs):
        """Called against each HTML tag, looks for metadata indicating
        the PDF URL.
        """
        if tag.lower() == "meta":
            attrs = dict(attrs)
            if u'name' in attrs and attrs[u'name'] == u'citation_pdf_url':
                self.pdf_url = attrs[u'content']


if __name__ == '__main__':
    main()
