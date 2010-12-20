#!/usr/bin/env python
"""
Rui Pereira <rui.pereira@gmail.com>
July 2010
--
Based on ADS to Bibdesk automator action by
Jonathan Sick, jonathansick@mac.com, August 2007

Input may be one of the following:
- ADS abstract page URL
- ADS bibcode
- arXiv abstract page
- arXiv identifier
"""
import cgi
import os
import re
import subprocess
import sys
import optparse
import tempfile
import urllib
import urlparse
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint


def main():
    """docstring for main"""
    parser = optparse.OptionParser()
    parser.add_option('-d', '--debug', dest="debug", default=False, action="store_true")
    options, articleID = parser.parse_args()

    # Get preferences from (optional) config file
    prefs = Preferences()
    if options.debug:
        prefs['debug'] = True

    # Determine what we're dealing with. The goal is to get a URL into ADS
    url = urlparse.urlsplit(articleID[0])
    if url.scheme == '':
        # ADS bibcode?
        adsURL = urlparse.urlunsplit(('http', prefs['ads_mirror'], 'abs/%s' % articleID[0], '', ''))
        # arXiv identifier?
        if 'No bibcodes' in urllib.urlopen(adsURL).read():
            adsURL = urlparse.urlunsplit(('http', 'arxiv.org', 'abs/%s' % articleID[0], '', ''))
            if 'not recognized' in urllib.urlopen(adsURL).read():
                # something's wrong
                sys.exit()
            else:
                adsURL = urlparse.urlunsplit(('http', prefs['ads_mirror'], 'cgi-bin/bib_query',
                                              'arXiv:%s' % articleID[0], ''))
    # arXiv URL
    elif 'arxiv' in url.netloc:
        # get paper identifier from URL and inject into ADS query
        arxivid = '/'.join(url.path.split('/')[2:]),
        adsURL = urlparse.urlunsplit(('http', prefs['ads_mirror'], 'cgi-bin/bib_query',
                                      'arXiv:%s' % arxivid, ''))
    elif url.netloc in prefs.adsmirrors:
        # we have a nice ADS abstract page entry
        adsURL = articleID[0]
    else:
        # we're in trouble here
        sys.exit()

    # parse the ADS HTML file
    ads = ADSHTMLParser(prefs=prefs)
    ads.parse(adsURL)
    #pdf local file, title, first author, abstract, bibtex code
    #UTF-8 encoded
    print ''.join(map(lambda x: x.encode('utf-8'), [ads.getPDF(), '|||',
                                                    ads.title, '|||',
                                                    ads.author[0], '|||',
                                                    ads.abstract, '|||',
                                                    ads.bibtex.__str__()]))


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

        f = open(self.prefsPath, 'r')
        for l in f:
            if l.strip() and not l.strip().startswith('#'):
                if '=' not in l:
                    # badly formed setting
                    continue
                k, v = l.strip().split('=')
                if not v:
                    v = None
                elif v.strip() in ['True', 'true', 'yes', 'Yes']:
                    v = True
                elif v.strip() in ['False', 'false', 'no', 'No']:
                    v = False
                elif v.strip() in ['None', 'none']:
                    v = None
                prefs[k] = v
        f.close()
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
        bibtex = urllib.urlopen(url).readlines()
        bibtex = ' '.join([l.strip() for l in bibtex]).strip()
        bibtex = bibtex[re.search('@[A-Z]+{', bibtex).start():]
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

        if 'prefs' in kwargs:
            self.prefs = kwargs['prefs']
        else:
            self.prefs = {} # Use an empty dictionary instead... or just create an empty Preferences instance?

    def mathml(self):
        """
        Generate dictionary with MathML -> unicode conversion from
        http://www.w3.org/Math/characters/byalpha.html
        """
        w3 = 'http://www.w3.org/Math/characters/byalpha.html'
        mathml = re.search('(?<=\<pre\>).+(?=</pre>)', urllib.urlopen(w3).read(), re.DOTALL).group()
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
        self.feed(urllib.urlopen(url).read())
        #parse bibtex
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
            return subprocess.Popen('file %s' % filename, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE).stdout.read()

        #refereed
        if 'article' in self.links:
            url = self.links['article']
            #try locally
            pdf = tempfile.mktemp() + '.pdf'
            urllib.urlretrieve(url, pdf)
            if 'PDF document' in filetype(pdf):
                return pdf

            #try in remote server
            # you need to set SSH public key authentication
            # for this to work!
            elif self.prefs.get('ssh_user') is not None:
                pdf = tempfile.mktemp() + '.pdf'
                cmd = 'ssh %s@%s \"touch adsbibdesk.pdf; wget -O adsbibdesk.pdf \\"%s\\"\"' % (self.prefs['ssh_user'], self.prefs['ssh_server'], url)
                cmd2 = 'scp -q %s@%s:adsbibdesk.pdf %s' % (self.prefs['ssh_user'], self.prefs['ssh_server'], pdf)
                subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                if 'PDF document' in filetype(pdf):
                    return pdf

        #arXiv
        if 'preprint' in self.links:
            #arXiv page
            url = self.links['preprint']
            for line in urllib.urlopen(url):
                if '<h1><a href="/">' in line:
                    mirror = re.search('<h1><a href="/">(.*ar[xX]iv.org)', line)
                elif 'dc:identifier' in line:
                    begin = re.search('dc:identifier="', line).end()
                    url = urlparse.urlsplit(line[begin:-2].replace('&#38;', unichr(38)).lower())
                    # use automatic mirror chosen by the ADS mirror
                    if not self.prefs.get('arxiv_mirror') and mirror is not None:
                        url = urlparse.urlunsplit((url.scheme, mirror.group(1), url.path, url.query, url.fragment))
                    elif self.prefs['arxiv_mirror']:
                        url = urlparse.urlunsplit((url.scheme, self.prefs['arxiv_mirror'], url.path, url.query, url.fragment))
                    #get arXiv PDF
                    pdf = tempfile.mktemp() + '.pdf'
                    urllib.urlretrieve(url.replace('abs', 'pdf'), pdf)
                    if 'PDF document' in filetype(pdf):
                        return pdf
                    else:
                        return url

        #electronic journal
        if 'ejournal' in self.links:
            return self.links['ejournal']

        return 'failed'


if __name__ == '__main__':
    main()
