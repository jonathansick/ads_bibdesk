# ADS to BibDesk

ADS to BibDesk is an Automator service that allows you to automatically retrieve the bibtex, abstract and PDF of an astronomical journal article published on [ADS](http://adsabs.harvard.edu) or [arXiv.org](http://arxiv.org/archive/astro-ph) and add it to your [BibDesk](http://bibdesk.sourceforge.net/) database.

ADS to BibDesk comes in two flavours. The *Service* version should be used by Mac OS X 10.6 Snow Leopard users working in Safari or other Cocoa applications. A legacy *Application* version is also available for Mac OS X 10.5 users, and users of non-Cocoa applications (*e.g.* Firefox).

## Quick Instructions

You can gather papers from many sources. In any browser window or document, select one of the following pieces of text:

* The URL of an ADS or arXiv article page,
* The ADS bibcode of an article (e.g. 1998ApJ...500..525S), or
* the arXiv identifier of an article (e.g. 0911.4956).

Now activate the 'Add to BibDesk' scripts:

* **If using the Services version,** right-click on the selected text and choose 'Services > Add to Bibdesk'.
* **If using the application version,** copy the selected text to the clipboard and launch the Add to BibDesk application.

The bibtex and abstract of the article will be copied into your currently-open BibDesk database. The scripts are now empowered to try download the article's PDF from ADS, or alternatively, arXiv. A Growl notification will appear when the import is complete.

**Updating pre-prints:** From the terminal, run the new update_bibdesk_arxiv.sh shell script to automatically update any astro-ph pre-prints that have been recently refereed.

For more details, see the [ADS to BibDesk homepage](http://www.jonathansick.ca/adsbibdesk/index.html).

## Install ADS to BibDesk for the Command Line

ADS to BibDesk can also be run directly from the command line.
Once you've checked out the source, and cd'd into the `ads_bibdesk` directory, run:

    cd build/adsbibdesk
    python setup.py install

You may need to run the last command with `sudo`.

Once ADS to BibDesk is installed, you can call it with the same types of article tokens you can launch the Service with, e.g.,

    adsbibdesk 1998ApJ...500..525S

A full summary of `adsbibdesk` commands is available via

    adsbibdesk --help

## Using PDF Ingest Mode

With the command-line ADS to BibDesk, you can ingest a folder of PDFs that originated from ADS into BibDesk.
This is great for users who have amassed a literature folder, but are just starting to use BibDesk.
This will get you started quickly.

You need the program [pdf2json](http://code.google.com/p/pdf2json/) to use
this script. The easiest way to get pdf2json and its dependencies is through
[Homebrew](http://mxcl.github.com/homebrew/), the Mac package manager.
Once homebrew is setup, simply run `brew install pdf2json`.

To run this workflow,

    adsbibdesk -p my_pdf_dir/

where `my_pdf_dir/` is a directory containing PDFs that you want to ingest.

Note that this workflow relies on a DOI existing in the PDF. As such, it will not identify astro-ph pre-prints, or published papers older than a few years. Typically the DOI is published on the first page of modern papers. This method was inspired by a script by [Dr Lucy Lim](http://www.mit.edu/people/lucylim/BibDesk.html).

## Developer Notes

ADS to BibDesk is built around two source files

1. `adsbibdesk.py` &mdash; scrapes arXiv and ADS pages for bibliographic information
2. `adsbibdesk.scpt` &mdash; adds the bibtex, abstract and PDF to BibDesk using AppleScript hooks.

These sources are used by the Apple Automator files and `update_bibdesk_arxiv.sh`.
Thus after editing either of the adsbibdesk source files, run the `build.py` script to update the Automator files and shell scripts.

## License

Copyright 2012 Jonathan Sick, Rui Pereira and Dan-Foreman Mackey

ADS to BibDesk is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ADS to BibDesk is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ADS to BibDesk.  If not, see <http://www.gnu.org/licenses/>.
