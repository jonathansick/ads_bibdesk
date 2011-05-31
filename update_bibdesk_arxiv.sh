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
python -c "import math;l=len('${bibcodes}'.strip().split());t=math.ceil(l*15./60.); print 'Checking %i ArXiv entries for changes...\n(to prevent ADS flooding this will take a while, check back in around %i %s)' % (l, t, t > 1 and 'minutes' or 'minute')"
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
        sleep 15
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

