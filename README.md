ADS to BibDesk
==============

ADS to BibDesk is an Automator service that allows you to automatically retrieve the bibtex, abstract and PDF of an astronomical journal article published on [ADS](http://adsabs.harvard.edu) or [arXiv.org](http://arxiv.org/archive/astro-ph) and add it to your [BibDesk](http://bibdesk.sourceforge.net/) database.

ADS to BibDesk comes in two flavours. The *Service* version should be used by Mac OS X 10.6 Snow Leopard users working in Safari or other Cocoa applications. A legacy *Application* version is also available for Mac OS X 10.5 users, and users of non-Cocoa applications (*e.g.* Firefox).


Quick Instructions
------------------

You can gather papers from many sources. In any browser window or document, select one of the following pieces of text:

* The URL of an ADS or arXiv article page,
* The ADS bibcode of an article (e.g. 1998ApJ...500..525S), or
* the arXiv identifier of an article (e.g. 0911.4956).

Now activate the 'Add to BibDesk' scripts:

* **If using the Services version,** right-click on the selected text and choose 'Services > Add to Bibdesk'.
* **If using the application version,** copy the selected text to the clipboard and launch the Add to BibDesk application.

The bibtex and abstract of the article will be copied into your currently-open BibDesk database. The scripts are now empowered to try download the article's PDF from ADS, or alternatively, arXiv. A Growl notification will appear when the import is complete.

For more details, see the [ADS to BibDesk homepage](http://www.jonathansick.ca/adsbibdesk/index.html).

Developer Notes
---------------

ADS to BibDesk is built around two source files

1. `adsbibdesk.py` &mdash; scrapes arXiv and ADS pages for bibliographic information
2. `adsbibdesk.scpt` &mdash; adds the bibtex, abstract and PDF to BibDesk using AppleScript hooks.

These sources are used by the Apple Automator files and `update_bibdesk_arxiv.sh`. Thus after editing either of the adsbibdesk source files, run the `build.py` script to update the Automator files and shell scripts.

License
-------

Copyright 2011 Jonathan Sick, Rui Pereira and Dan-Foreman Mackey

ADS to BibDesk is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ADS to BibDesk is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.