# Contributing to ADS to BibDesk

Thanks for helping out with ADS to BibDesk. I rely on the community to identify bugs and contribute fixes so we can all get on with reading papers. The prerequisite for working on ADS to BibDesk is a [GitHub](http://github.com) account. This document gives tips on how to submit bug reports, or if you're a developer, how to build the source code to test changes, and what to do when submitting a pull request.

## Contents

* [Submitting a Bug Report (Issues)](#issues)
* [Building & Editing ADS to BibDesk (Development)](#dev)
  - [Code Overview & Philosophy](#code-overview)
  - [Building ADS to BibDesk](#building)
  - [Making & Submitting Changes (Pull Request)](#pull-requests)

***

<a name="issues"></a>
## Submitting a Bug Report

If ADS to BibDesk crashes, *submit an [Issue](https://github.com/jonathansick/ads_bibdesk/issues)*. I've been slow to respond to issues in the past, but I'd like to fix that now. I promise.

To help us out, you'll want to re-run ADS to BibDesk on the offending paper/command in debug mode, which will print out some extra info to help us figure out what's happening.

- If you're running on the command line, just add the `--debug` flag to your command.
- If you're running the Service, edit `~/.adsbibdesk` and set/change the line `debug = true`. Re-run the Service, and you'll see output appearing in `~/.adsbibdesk.log`.

When submitting an [Issue](https://github.com/jonathansick/ads_bibdesk/issues), mention the command or paper you're running, and copy the debugging output of the the log file or terminal. If you're using an old version of Mac OS X, that would be helpful to know too.

*Thank you!*

***

<a name="dev"></a>
## Building & Editing ADS to BibDesk

<a name="code-overview"></a>
### Code Overview & Philosophy

At its core, ADS to BibDesk is a Python script that can either be run directly on the command line, embedded and run within a Mac OS X Service. Because of the latter, we needed to make a few unusual constraints on the code:

- All python code must fit within a single source file, `adsbibdesk.py` and we cannot install separate modules,
- We can't install or use third-party python packages (the exception to this is [PyObjC](http://pythonhosted.org/pyobjc/)),
- We need to use Python features that exist in Python 2.6 to support older versions of Mac OS X.

If you want to understand how `adsbibdesk.py` works, start with the `main()` function and follow the execution flow.

<a name="building"></a>
### Building ADS to BibDesk

First, clone the source code from GitHub:

    git clone https://github.com/jonathansick/ads_bibdesk.git
    cd ads_bibdesk

(If you're making changes to the source, you'll want to work from your own fork, see below.)

To install the command line version of ADS to BibDesk, run

    python setup.py install

To check your installation, you can run commands like:

    rehash
    which adsbibdesk
    adsbibdesk --version
    adsbibdesk --help

To build the Service version of ADS to BibDesk to use inside Mac apps, just run

    python setup.py service

and the built Service will located at `build/Add to BibDesk.workflow`. Double-click it to install.

Although we need to track the Automator workflow, we don't need to commit changes to the Python script we embed in it. Thus it may be handy to ignore those changes by running: `git update-index --assume-unchanged "build/Add to BibDesk.workflow/Contents/document.wflow"`

<a name="pull-request"></a>
### Making & Submitting Changes (Pull Request)

Here are some guidelines for developing ADS to BibDesk to fix a bug or implement a new feature.

1. Submit an [Issue](https://github.com/jonathansick/ads_bibdesk/issues) so we know what you're up to. This Issue will get closed by the pull request, and also make sure that effort isn't duplicated.
2. Fork ADS to BibDesk; [this guide](https://guides.github.com/activities/forking/) will tell you how.
3. Use the `git update-index --assume-unchanged` trick to make sure you don't commit a change to the automator workflow.
4. Work from a branch, e.g., `git co -b dev/my_fix`.
5. Follow our procedure for building the command line app and Service to test things out.
6. Make sure your changes conform to [PEP8](http://legacy.python.org/dev/peps/pep-0008/). The pep8 package helps with this: `pip install pep8` then run `pep8 adsbibdesk.py`. Also, all variables should be named `like_this` and not `likeThis` (i.e., use underscore separators, not camel case).
7. Submit the Pull Request as mentioned in the GitHub guide. In the comment for your pull request, mention the Issue number (e.g. 'fixes #33.')

*Thank you*