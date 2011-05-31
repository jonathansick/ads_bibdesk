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

# check for changed bibcodes
python -c "import math;l=len('${bibcodes}'.strip().split()); print 'Checking %i ArXiv entries for changes...\n(to prevent ADS flooding this will take a while, check back in around %i minutes)' % (l, math.ceil(l*10./60.))"
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

echo "To prevent ADS flooding, we will wait 1 minute between each query, so go drink a coffee."
# update bibcodes
for bibcode in `cat changed_arxiv`; do
    echo "Updating $bibcode..."
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
    sleep 60
done

#clean up
cd -
rm -rf $tmpdir









