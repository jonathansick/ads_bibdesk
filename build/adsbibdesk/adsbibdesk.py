#!/usr/bin/env python
"""
ADS to BibDesk -- frictionless import of ADS publications into BibDesk
Copyright (C) 2011  Rui Pereira <rui.pereira@gmail.com> and
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
import sys
import os
import re
import time
import optparse
import tempfile
import socket
import binascii
import zlib
import subprocess

import cgi
import urllib2
import urlparse

import subprocess as sp
from HTMLParser import HTMLParser, HTMLParseError
from htmlentitydefs import name2codepoint

# default timeout for url calls
socket.setdefaulttimeout(30)




def main():
    """
    Parse options and launch main loop
    """
    parser = optparse.OptionParser()
    parser.add_option('-d', '--debug', dest="debug", default=False, action="store_true")
    parser.add_option('-u', '--update_arxiv', default=False, action="store_true")
    options, articleID = parser.parse_args()

    if len(articleID) == 1:
        articleIDs = list(articleID)
    else:
        # Try to use standard input
        articleIDs = map(lambda s: s.strip(), sys.stdin.readlines())

    # Get preferences from (optional) config file
    prefs = Preferences()
    if options.debug:
        prefs['debug'] = True

    # Make the embedder script
    insertScript = EmbeddedInsertionScript()
    insertScript.install()

    # multiple arguments - bibcodes to compare with ADS
    if options.update_arxiv or len(articleIDs) > 1:
        changed = open('changed_arxiv', 'w')
        for n, bibcode in enumerate(articleIDs):
            # sleep for 15 seconds, to prevent ADS flooding
            time.sleep(15)
            if prefs['debug']:
                print "bibcode", bibcode
            # these are ADS bibcodes by default
            adsURL = urlparse.urlunsplit(('http', prefs['ads_mirror'], 'abs/%s' % bibcode, '', ''))
            if prefs['debug']:
                print "adsURL", adsURL
            # parse the ADS HTML file
            ads = ADSHTMLParser(prefs=prefs)
            ads.parse(adsURL)
            if prefs['debug']:
                print "ads.bibtex", ads.bibtex
            if ads.bibtex is None: # ADSHTMLParser failed
                if prefs['debug']:
                    print "FAILURE: ads.bibtex is None!"
                continue
            if ads.bibtex.bibcode != bibcode:
                print '%i. %s has become %s' % (n+1, bibcode, ads.bibtex.bibcode)
                print >> changed, bibcode
            else:
                print '%i. %s has not changed' % (n+1, bibcode)
                continue
        changed.close()

    # normal call
    else:
        # Determine what we're dealing with. The goal is to get a URL into ADS
        # adsURL = parseURL(articleID[0], prefs)
        if prefs['debug']: print "article token", articleIDs[0]
        connector = ADSConnector(articleIDs[0], prefs)
        if prefs['debug']: print "derived url", connector.adsURL
        if connector.adsRead is None:
            sys.exit()

        # parse the ADS HTML file
        ads = ADSHTMLParser(prefs=prefs)
        ads.parse(connector.adsRead)
        # pdf local file, title, first author, abstract, bibtex code
        # UTF-8 encoded
        output = ''.join(map(lambda x: x.encode('utf-8'), [ads.getPDF(), '|||',
                                                        ads.title, '|||',
                                                        ads.author[0], '|||',
                                                        ads.abstract, '|||',
                                                        ads.bibtex.__str__()]))
        # Escape double quotes
        output = output.replace('"', '\\"')
        cmd = 'osascript %s "%s"' % (insertScript.compiledPath, output)
        if prefs['debug']:
            print cmd
        subprocess.call(cmd, shell=True)


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
        self.adsURL = None # string URL to ADS
        self.adsRead = None # a urllib2.urlopen connection to ADS
        self.urlParts = urlparse.urlsplit(token) # supposing it is a URL

        # An arXiv identifier?
        if self._is_arxiv():
            if self.prefs['debug']:
                print "Found arXiv ID", self.token
        # A bibcode from ADS?
        elif not self.urlParts.scheme and self._is_bibcode():
            if self.prefs['debug']:
                print "Found ADS bibcode / DOI", self.token
        else:
            # If the path lacks http://, tack it on because the token *must* be a URL now
            if not self.token.startswith("http://"):
                self.token = 'http://' + self.token
            self.urlParts = urlparse.urlsplit(self.token) # supposing it is a URL

            # An abstract page at any ADS mirror site?
            if self.urlParts.netloc in self.prefs.adsmirrors and self._is_ads_page():
                if self.prefs['debug']:
                    print "Found ADS page", self.token
            elif "arxiv" in self.urlParts.netloc and self._is_arxiv_page():
                if self.prefs['debug']:
                    print "Found arXiv page", self.token

    def _is_arxiv(self):
        """Try to classify the token as an arxiv article, either:
        - new style (YYMM.NNNN), or
        - old style (astro-ph/YYMMNNN)
        :return: True if ADS page is recovered
        """
        arxivPattern = re.compile('(\d{4,6}.\d{4,6}|astro\-ph/\d{7})')
        arxivMatches = arxivPattern.findall(self.token)
        if len(arxivMatches) == 1:
            arxivID = arxivMatches[0]
            self.adsURL = urlparse.urlunsplit(('http', self.prefs['ads_mirror'],
                                               'cgi-bin/bib_query', 'arXiv:%s' % arxivID, ''))
            # Try to open the ADS page
            return self._read(self.adsURL)
        else:
            return False
    
    def _is_bibcode(self):
        """Test if the token corresponds to an ADS bibcode or DOI"""
        self.adsURL = urlparse.urlunsplit(('http', self.prefs['ads_mirror'],
                                           'doi/%s' % self.token, '', ''))
        return self._read(self.adsURL)

    def _is_ads_page(self):
        """Test if the token is a url to an ADS abstract page"""
        # use our ADS mirror
        url = self.urlParts
        self.adsURL = urlparse.urlunsplit((url.scheme, self.prefs['ads_mirror'],
                                           url.path, url.query, url.fragment))
        return self._read(self.adsURL)
    
    def _is_arxiv_page(self):
        """Test if the token is a url to an arxiv abstract page."""
        # get paper identifier from URL and inject into ADS query
        url = self.urlParts
        arxivid = '/'.join(url.path.split('/')[2:]),
        self.adsURL = urlparse.urlunsplit(('http', self.prefs['ads_mirror'],
                                           'cgi-bin/bib_query', 'arXiv:%s' % arxivid, ''))
        return self._read(self.adsURL)
    
    def _read(self, adsURL):
        """Attempt a connection to adsURL, saving the read to
        self.adsread.
        :return: True if successful, False otherwise
        """
        try:
            self.adsRead = urllib2.urlopen(adsURL).read()
            return True
        except urllib2.HTTPError:
            return False


class Preferences(object):
    """Manages the preferences on disk and in memory. Preferences are accessed
    with by a dictionary-like interface.
    """

    def __init__(self):
        self.prefsPath = os.path.join(os.getenv('HOME'), '.adsbibdesk')
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

        self.prefs = self._getDefaultPrefs() # Hard coded defaults dictionary
        newPrefs = self._getPrefs() # load user prefs from disk
        self.prefs.update(newPrefs) # override defaults with user prefs
        self._keys = self.prefs.keys()
        self._iterIndex = -1

    def __getitem__(self, key):
        return self.prefs[key]

    def __setitem__(self, key, value):
        self.prefs[key] = value
        self._keys = self.prefs.keys()

    def __iter__(self):
        return self

    def next(self):
        if self._iterIndex == len(self._keys)-1:
            self._iterIndex = -1
            raise StopIteration
        self._iterIndex += 1
        return self._keys[self._iterIndex]

    def _getDefaultPrefs(self):
        """:return: a dictionary of the full set of default preferences. This
        is done in case the user's preference file is missing a key-value pair.
        """
        return {"ads_mirror": "adsabs.harvard.edu",
                "arxiv_mirror": None,
                "download_pdf": True,
                "ssh_user": None,
                "ssh_server": None,
                "debug": False}

    def _getPrefs(self):
        """Read preferences files from `self.prefsPath`, creates one otherwise."""
        prefs = {}
        # create a default preference file if non existing
        if not os.path.exists(self.prefsPath):
            self._writeDefaultPrefs()

        for l in open(self.prefsPath):
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

    def _writeDefaultPrefs(self):
        """
        Set a default preferences file (~/.adsbibdesk)
        """
        prefs = open(self.prefsPath, 'w')
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


class BibTex:

    def __init__(self, url):
        """
        Create BibTex instance from ADS BibTex URL
        """
        bibtex = urllib2.urlopen(url).readlines()
        bibtex = ' '.join([l.strip() for l in bibtex]).strip()
        bibtex = bibtex[re.search('@[A-Z]+\{', bibtex).start():]
        self.type, self.bibcode, self.info = self.parsebib(bibtex)

    def __str__(self):
        return ','.join(['@' + self.type + '{' + self.bibcode] + ['%s=%s' % (i, j) for i, j in self.info.items()]) + '}'

    def parsebib(self, bibtex):
        """
        Parse bibtex code into dictionary
        """
        r = re.search('(?<=^@)(?P<type>[A-Z]+){(?P<bibcode>\S+)(?P<info>,.+)}$', bibtex)
        s = re.split('(,\s\w+\s=\s)', r.group('info'))
        info = dict([(i[1:].replace('=', '').strip(), j.strip()) for i, j in zip(s[1::2], s[2::2])])
        return r.group('type'), r.group('bibcode'), info


class ADSException(Exception):
    pass


class ADSHTMLParser(HTMLParser):

    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self)
        self.links = {}
        self.tag = ''
        self.get_abs = False
        self.entities = {}

        self.bibtex = None
        self.abstract = None
        self.title = ''
        self.author = []

        self.prefs = kwargs.get('prefs', Preferences()).prefs

    def mathml(self):
        """
        Generate dictionary with MathML -> unicode conversion from
        http://www.w3.org/Math/characters/byalpha.html
        """
        w3 = 'http://www.w3.org/Math/characters/byalpha.html'
        mathml = re.search('(?<=<pre>).+(?=</pre>)', urllib2.urlopen(w3).read(), re.DOTALL).group()
        entities = {}
        for l in mathml[:-1].split('\n'):
            s = l.split(',')
            #ignore double hex values like 'U02266-00338'
            if '-' not in s[1]:
                #hexadecimal -> int values, for unichr
                entities[s[0].strip()] = int(s[1].strip()[1:], 16)
        return entities
    
    def parse(self, url):
        """
        Feed url into our own HTMLParser and parse found bibtex
        """
        try:
            self.feed(url.startswith('http') and urllib2.urlopen(url).read() or url)
        # HTTP timeout
        except urllib2.URLError, err:
            if self.prefs['debug']:
                print '%s timed out', url
            raise ADSException(err)

        if self.prefs['debug']:
            print "ADSHTMLParser links:",
            print self.links

        if 'bibtex' in self.links:
            self.bibtex = BibTex(self.links['bibtex'])
            self.title = re.search('(?<={).+(?=})', self.bibtex.info['title']).group().replace('{', '').replace('}', '')
            self.author = [a.strip() for a in
                           re.search('(?<={).+(?=})', self.bibtex.info['author']).group().split(' and ')]
    
    def handle_starttag(self, tag, attrs):
        #abstract
        if tag.lower() == 'hr' and self.get_abs:
            self.abstract = self.tag.strip().decode('utf-8')
            self.get_abs = False
            self.tag = ''
        #handle old scanned articles abstracts
        elif tag.lower() == 'img' and self.get_abs:
            self.tag += dict(attrs)['src'].replace('&#38;', unichr(38))
        #links
        elif tag.lower() == 'a':
            if 'href' in dict(attrs):
                href = dict(attrs)['href'].replace('&#38;', unichr(38))
                query = cgi.parse_qs(urlparse.urlsplit(href).query)
                if 'bibcode' in query:
                    if 'link_type' in query:
                        self.links[query['link_type'][0].lower()] = href
                    elif 'data_type' in query:
                        self.links[query['data_type'][0].lower()] = href

    def handle_data(self, data):
        if self.get_abs:
            self.tag += data.replace('\n', ' ')

        #beginning of abstract found
        if data.strip() == 'Abstract':
            self.get_abs = True

    #handle html entities
    def handle_entityref(self, name):
        if self.get_abs:
            if name in name2codepoint:
                c = name2codepoint[name]
                self.tag += unichr(c).encode('utf-8')
            else:
                #fetch mathml
                if not self.entities:
                    #cache dict
                    self.entities = self.mathml()
                if name in self.entities:
                    c = self.entities[name]
                    self.tag += unichr(c).encode('utf-8')
                else:
                    #nothing worked, leave it as-is
                    self.tag += '&' + name + ';'

    #handle unicode chars in utf-8
    def handle_charref(self, name):
        if self.get_abs:
            self.tag += unichr(int(name)).encode('utf-8')

    def getPDF(self):
        """
        Fetch PDF and save it locally in a temporary file.
        Tries by order:
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
            if "MNRAS" in url: # Special case for MNRAS URLs to deal with iframe
                parser = MNRASParser(self.prefs)
                try:
                    parser.parse(url)
                except MNRASException:
                    # this probably means we have a PDF directly from ADS, just continue
                    pass
                if parser.pdfURL is not None:
                    url = parser.pdfURL

            # try locally
            pdf = tempfile.mktemp() + '.pdf'
            # test for HTTP auth need
            try:
                open(pdf, 'wb').write(urllib2.urlopen(url).read())
            except urllib2.HTTPError:
                # dummy file
                open(pdf, 'w').write('dummy')

            if 'PDF document' in filetype(pdf):
                return pdf

            # try in remote server
            # you need to set SSH public key authentication for this to work!
            elif 'ssh_user' in self.prefs and self.prefs['ssh_user'] is not None:
                pdf = tempfile.mktemp() + '.pdf'
                cmd = 'ssh %s@%s \"touch adsbibdesk.pdf; wget -O adsbibdesk.pdf \\"%s\\"\"' % (self.prefs['ssh_user'], self.prefs['ssh_server'], url)
                cmd2 = 'scp -q %s@%s:adsbibdesk.pdf %s' % (self.prefs['ssh_user'], self.prefs['ssh_server'], pdf)
                sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE).communicate()
                sp.Popen(cmd2, shell=True, stdout=sp.PIPE, stderr=sp.PIPE).communicate()
                if 'PDF document' in filetype(pdf):
                    return pdf

        # arXiv
        if 'preprint' in self.links:
            # arXiv page
            url = self.links['preprint']
            mirror = None
            for line in urllib2.urlopen(url):
                if '<h1><a href="/">' in line:
                    mirror = re.search('<h1><a href="/">(.*ar[xX]iv.org)', line)
                elif 'dc:identifier' in line:
                    begin = re.search('dc:identifier="', line).end()
                    url = urlparse.urlsplit(line[begin:-2].replace('&#38;', unichr(38)).lower())
                    # use automatic mirror chosen by the ADS mirror
                    if ('arxiv_mirror' not in self.prefs or not self.prefs['arxiv_mirror']) and mirror is not None:
                        url = urlparse.urlunsplit((url.scheme, mirror.group(1), url.path, url.query, url.fragment))
                    elif self.prefs['arxiv_mirror']:
                        url = urlparse.urlunsplit((url.scheme, self.prefs['arxiv_mirror'], url.path, url.query, url.fragment))
                    # get arXiv PDF
                    pdf = tempfile.mktemp() + '.pdf'
                    open(pdf, 'wb').write(urllib2.urlopen(url.replace('abs', 'pdf')).read())
                    if 'PDF document' in filetype(pdf):
                        return pdf
                    else:
                        return url

        #electronic journal
        if 'ejournal' in self.links:
            return self.links['ejournal']

        return 'failed'

    
def test_mnras():
    prefs = Preferences()
    prefs['debug'] = True
    
    data = '<iframe id="pdfDocument" src="http://onlinelibrary.wiley.com/store/10.1111/j.1365-2966.2010.18174.x/asset/j.1365-2966.2010.18174.x.pdf?v=1&amp;t=gp75eg4q&amp;s=c7ec3f26d269f5f4187799ff6faf44ebe01bbb01" width="100%" height="100%"></iframe>'
    parser = MNRASParser(prefs)
    # parser.parse(mnrasURL)
    parser.feed(data)
    print parser.pdfURL


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
        self.pdfURL = None
    
    def parse(self, url):
        """Parse URL to MNRAS PDF page"""
        try:
            self.feed(urllib2.urlopen(url).read())
        except urllib2.URLError, err: # HTTP timeout
            if self.prefs['debug']:
                print 'MNRAS timed out: %s' % url
            raise MNRASException(err)
        except HTMLParseError, err:
            raise MNRASException(err)
    
    def handle_starttag(self, tag, attrs):
        """
        def get_mnras_pdf(url):
           soup = BeautifulSoup(urllib2.urlopen(url))
           pdfurl = soup.find('iframe')['src']
           open('mnras.pdf', 'wb').write(urllib2.urlopen(pdfurl).read())
        """
        if tag.lower() == "iframe":
            attrDict = dict(attrs)
            self.pdfURL = attrDict['src']


class EmbeddedInsertionScript(object):
    """Manages the bibdesk insertion applescript.
    
    In order to make adsbibdesk.py a single-file installation (and Automator
    action) we need this Python script to spawn the AppleScript interface to
    BibDesk itself. The `build.py` script is responsible for embedding
    adsbibdesk.applescript into this Python script.
    """
    def __init__(self):
        super(EmbeddedInsertionScript, self).__init__()
        self._txtData = "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"
        self.compiledPath = os.path.expanduser("~/.adsbibdesk_injector.scpt")

    def install(self):
        """Install the compiled script"""
        # Write the embedded applescript to a temp file
        scptTxt = zlib.decompress(binascii.a2b_base64(self._txtData))
        txtPath = tempfile.mktemp() + '.applescript'
        tmpFile = open(txtPath, 'w')
        tmpFile.write(scptTxt)
        tmpFile.close()
        # Compile the applescript
        if os.path.exists(self.compiledPath):
            print "Compiled applescript %s already exists; skipping compile step" % self.compiledPath
            # os.remove(self.compiledPath)
        else:
            cmd = "osacompile -o %s %s" % (self.compiledPath, txtPath)
            print "Compiling applescript via:"
            print cmd
            subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    main()
    # test_mnras()
    # scpt = EmbeddedInsertionScript()
    # scpt.install()