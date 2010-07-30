ADS to BibDesk
==============

ADS to BibDesk is an Automator service that allows you to automatically retrieve the bibtex, abstract and PDF of an astronomical journal article published on [ADS](http://adsabs.harvard.edu) or [arXiv.org](http://arxiv.org/archive/astro-ph) and add it to your [BibDesk](http://bibdesk.sourceforge.net/) database.

ADS to BibDesk comes in two flavours. The *Service* version should be used by Mac OS X 10.6 Snow Leopard users working in Safari or other Cocoa applications. A legacy *Application* version is also available for Mac OS X 10.5 users, and users of non-Cocoa applications (*e.g.* Firefox).

Installing
----------

Download the app from [http://homepage.mac.com/jonathansick/notes/ads_bibdesk/ADS_BibDesk_v2.tar](http://homepage.mac.com/jonathansick/notes/ads_bibdesk/ADS_BibDesk_v2.tar)

* To install the Service, drag 'Add to Bibdesk' (the one with a work-flow icon) to ~/Library/Services. Create the Services folder if necessary. You need at least Mac OS X 10.6 (Snow Leopard) for this.
* To install the application version, drag 'Add to Bibdesk App' (the one with an Automator robot icon) to the Applications folder, and to your dock for easy access.


Usage
-----

You can gather papers from many sources. In any browser window or document, select one of the following pieces of text:

* The URL of an ADS or arXiv article page,
* The ADS bibcode of an article (e.g. 1998ApJ...500..525S), or
* the arXiv identifier of an article (e.g. 0911.4956).

Now activate the 'Add to BibDesk' scripts:

* **If using the Services version,** right-click on the selected text and choose 'Services > Add to Bibdesk'.
* **If using the application version,** copy the selected text to the clipboard and launch the Add to BibDesk application.

The bibtex and abstract of the article will be copied into your currently-open BibDesk database. The scripts are now empowered to try download the article's PDF from ADS, or alternatively, arXiv. A Growl notification will appear when the import is complete.

<!-- Setting up BibDesk for Best Effect

This app works best if you have one main bibliography that you put all papers into. This one bibliography document should always be the top-most document in BibDesk (this doesn't include Publication windows). Otherwise "ADS to BibDesk" will put the bib entry into whatever BibDesk document is active.
"ADS to BibDesk" will launch BibDesk for you if its closed. To have your main bibliography always open on BibDesk launch, set this behaviour in BibDesk's Preferences > General.
A great feature of BibDesk is cite-key generation so that the long ADS cite keys become something nicer like Sick:2008. You can have this set up in BibDesk's Preferences > Cite Key.
Also set the auto-renamning of the files so that the PDFs you attach to the bib items are systematically named. Under BibDesk's Preferences > Auto-File, I use a custom naming scheme: %a1%Y%u0%e so that the articles are named like Sick:2008, or Sick:2008b as necessary. -->

How to update old astro-ph articles to the published versions
-------------------------------------------------------------

Quite often we first encounter an article as a pre-print on astro-ph, but once that article is published we want to update the bibdesk record to the refereed version. A great new feature in v2 is the ability to remove an older bibdesk reference if an article is re-imported.
That is, if you import an article with the same title and author information as an article that already exists in your database, 'Add to Bibdesk' will delete that older article and import the new bibtex and PDF.