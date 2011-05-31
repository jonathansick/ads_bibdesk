#!/bin/sh
# ADS to BibDesk -- frictionless import of ADS publications into BibDesk
# Copyright (C) 2011  Rui Pereira <rui.pereira@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# ugliest hack in the world - harcoded/compressed strings of both applescript and python scripts as in the automator actions
py="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"
scpt="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"
tmpdir=$(python -c "import tempfile; print tempfile.mkdtemp()")
python -c "import binascii,zlib;\
           out=open('${tmpdir}/py.py', 'w'); print >> out, zlib.decompress(binascii.a2b_base64('${py}')); \
           out=open('${tmpdir}/scpt.scpt', 'w'); print >> out, zlib.decompress(binascii.a2b_base64('${scpt}'))"

# go the tmp directory
cd $tmpdir

# fetch arXiv bibcodes from BibDesk using an applescript
bibcodes=$(cat << EOF | osascript -
tell document 1 of application "BibDesk"
	set bibcodes to {}
	repeat with thePub in publications
		if (count (every field of thePub whose name is "Adsurl" and (value contains "arxiv" or value contains "astro.ph"))) > 0 then
			-- get bibcode from ADSurl
			set ADSurl to (value of every field of thePub whose name is "Adsurl")
			set AppleScript's text item delimiters to "/"
			set end of bibcodes to last text item of text item 1 of ADSurl
		end if
	end repeat
end tell
set AppleScript's text item delimiters to " "
return bibcodes as text
EOF
)

if [ "$bibcodes" == "" ]; then echo "Nothing to update!"; exit; fi
# check for changed bibcodes
python -c "import math;l=len('${bibcodes}'.strip().split());t=math.ceil(l*10./60.); print 'Checking %i ArXiv entries for changes...\n(to prevent ADS flooding this will take a while, check back in around %i %s)' % (l, t, t > 1 and 'minutes' or 'minute')"
python py.py $bibcodes
# python py.py $bibcodes --debug # DEBUG MODE

changed=$(wc -l changed_arxiv | awk '{print $1}')
if [ "$changed" -gt "0" ]
then
    echo ""; echo "Updating $changed entries, continue? (y/[n])"
    read -n1 -s continue
else
    echo ""; echo "Nothing to update!"
    exit
fi
if [ "$continue" != "Y" ] && [ "$continue" != "y" ]
then exit
fi

echo "(to prevent ADS flooding, we will wait for a while between each update, so go grab a coffee)"
# update bibcodes
for bibcode in `cat changed_arxiv`; do
    echo "Updating $bibcode..."
    # sleep 1 minute if updating a lot of stuff, if not wait only 10s
    if [ "$changed" -gt "10" ]
    then
        sleep 60
    else
        sleep 10
    fi
    # delete previous arXiv version explicitely
    # the automated same author/title check fails a lot
    cat << EOF | osascript -
on safeDelete(thePub)
	tell document 1 of application "BibDesk"
		tell thePub
			--remove PDFs
			repeat with theFile in (linked files whose POSIX path does not contain "_skim_")
				if POSIX path of theFile ends with ".pdf" then
					-- keep backup with Skim notes
					if Skim notes of theFile is not {} then
						tell application "Finder"
							set theSuffix to 1
							set thePath to (container of file theFile as string)
							set AppleScript's text item delimiters to "."
							set tmpName to items 1 thru -2 of (text items of (name of file theFile as string)) as string
							set AppleScript's text item delimiters to ""
							-- find a non-existing backup name
							repeat
								set backupName to tmpName & "_skim_" & theSuffix & ".pdf"
								if not (item (thePath & backupName) exists) then exit repeat
								set theSuffix to theSuffix + 1
							end repeat
							-- change file name (BibDesk will properly reference it automatically)
							set name of file theFile to backupName
						end tell
						-- delete PDFs without Skim notes
					else
						tell application "Finder"
							delete file theFile
						end tell
					end if
				end if
			end repeat
		end tell
		delete thePub
	end tell
end safeDelete

tell document 1 of application "BibDesk"
	set pub2delete to {}
	repeat with thePub in publications
		if (count (every field of thePub whose name is "Adsurl" and (value contains "${bibcode}"))) > 0 then
			set AppleScript's text item delimiters to {"{", "}"}
			set theTitle to (title of thePub)
			set end of pub2delete to every text item of theTitle
		end if
	end repeat
	set AppleScript's text item delimiters to ""
	repeat with theTitle in pub2delete
		set theTitle to theTitle as text
		repeat with thePub in (search for theTitle)
			my safeDelete(thePub)
		end repeat
	end repeat
end tell
EOF
    osascript scpt.scpt `python py.py ${bibcode}`

done

#clean up
cd - > /dev/null
rm -rf $tmpdir
