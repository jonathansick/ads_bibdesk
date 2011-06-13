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
py="eJytO2t32zay3/UrUOmmpBqJjp2z3R41cuIm8cb3JI2P7ZzdruyrhShIQkyRLEha0U1zf/udGYAk+JCtpNUHm4/BYGYwb4C97w6yRB3MZHggwjsWb9NVFHa63W7n5NUlSyP2i5y9EsktGw7ZQkk/lVEYiCRhch1HKmXRgiFgnM0C6XN8C6/CclznZRRvlVyuUua+7LOjJ4eHjF1kkp0LJaTi7JnKpBfrmxfLNZeB50frY8bDeYe1/P47Cnm64iG7lP4te/bR3CZw92LNfRrc6VytZMJiFS0VXzO4XCghWBIt0g1XYsS2UcZ8wKHEXCapkrMsFUymOOlBpNg6msvFtgMPsnAuFEtXgqVCrRNkF2/+8esH9g8RCsUDdk6ss7fSF2EiGE+0MJKVmLPZtoPgpzj7pZmdnUaAlUQ1YELCe8XuhErgnj3NJzDYBixSHZenSLBiUYyD+kDllgU8Lcd5TYZLvuawHoRzFcXAxgqwAWMbGQRsJliWiEUWDDoAyf55dvXm/YcrdvLrb+yfJxcXJ79e/fYzQIJKwFtxJzQeWPlAAlpgRvEw3QLNnXevL16+AfiTX87enl39BmSz07OrX19fXrLT9xfshJ2fXFydvfzw9uSCnX+4OH9/+dpj7FIgQaJzjzgXtBwgtblIQTcSYPU3WLwESArmbMXvBCyiL+QdEMSZD8r28Bp1eBCFS2IMIEu5AUVnCxZG6YAlQNmzVZrGo4ODzWbjLcPMi9TyINAYkoNjIOQXnsCssGylqczRVHiWRmueAuWc7AXVoKK2A9amtgN2ki2zJAUjefL3TucsjEHqa77FZYpCkfO1iIIg2shwOeoMaWY+g6WGmVjMl4J9uHhrns/kzI/mAu64+pe8q8IVT+VchKlcSKHI6o1ZJ9skv4yKKyXyq1Sui2vQypirpHwn1vFCBsV9Evm3Iu3kt/5S5peZCgI5O7JuNaJiZDaDlfHR24BVJXFnoaI1e3P17u05wqncB5VPNMQqXQfIVLqdi0XhqUK+FkcokDgCB9Xp9EClFjwLNDeo4ahrQAR4hiBIOppuLxGpgTNg7tMn/U4HnsHayNDtj8hNoezwP9FhLDVBfwKWmoX+ioBZEEVxBTzWjIwLKXrvaahmx+1bQB6fz6casesM586AOcPhXMyyJVyC3qXjLt11Bzlj41MeoA/RWjjuJqCSYpqqTHR3I8404iwGFyWmXH2Sd87+GA3jAKFS6Qfi7BXwZqahf4BxmQBfBN0DAwV1VGIB/j+EhWa0fq7GwoM+GHS4kEtG+kQUK1zRMTsvxxghyUU+uUdiGBXRg8ZMHC2qGxh8BfTmBKyBKxkH4LfVMluD1iRsmFtOgkYNhhmj1yZvAWZVn8wWFLo90Dy3YL7PjtlhSYkPFr8El4HLDWCOuS+k7GycfgGM2ggRwtCCTlyEQKGC2awJRpUg2WNJIERMYw//Bl4M5DeH1QA+QArgwFPyDAvQwzl4kMpYVG+PhruHf+tXXgG7VSGOGqE5VmBUrGuo7RZ018gDB4YxEuRpeagEHGSuYRV4Pk/AnYG4ctfgwUUWJhB/Utd10D+D1AxpADxdS6Ui5dyAKMHbHTxKHPYonwWeoYid/rfypqkB1vRFjTOijxw0coYuqdRaix9gBt6XHsulycf0t18H1ibj6vn+BNkeiCAVnzTp5qaOrXyD6cOvEHBGwFWFVraACCyaadketFj0nJ6cvf1w8XrUMuN33cZAUOBUhpnYTa6XW8h343ypd8nCeSQ99iiBtAFUDmxjLZhWETd8fDgoFaWJvL8D4/FxbtTtGi/AXe5DDSQdOaIGPc25G0IxQz0/iEBfCu8aRmrNdTzrNKnpsVcCs1oJucUG08KNcCjR4oE06ZHHrkChlxEgkeQNl+CvOeYYOsnP/SH+CmMlpYXL0ktNntwYMy150WtImIy6VdiEBMQTn8DMDTOa4IeMbG8D221cMMl8AYEahEa4wXnKFP8tpILcDHK7VaQGRTJFq4QqXFn6HvtwdTr8CTw2Pi4txiy8432EHMRd89gN+Ho25+zTiH3yNLTrZOli+JPTH7AJkgkiP3916sKt88cffziDVtva54fIDC9/ASYtCFrZvwJbIc6/AJkx3ekUcE6nbv8GXL7O2ArVlOEUQkmulKPcYAJQb/0Kk25uqYGO/wYMFRBtkNIFk5ZTFYyJNYJgfoAKBhYkExxuJrTCtRJppkKdCJiXnhJ8nis80lANfDrsGVhDSZm9g8+IWKHJQABAeYm/EuDkxmPQOdvwreD7vGnAfyra5pJtBNsHooQxDaDMaUTYVG3rec48Ch3wWDxJcZ1ioRbCT4Mt+KpojgygXHfmElh1eAYodwC58HN48ckXcVGjeG+urs5fI7t1QupV1PPqrJjZ7SFVhwCxxHT2k+YeErWkSkSiXA051cSvLl3NWAolBUhBgoQhzUY116wWSm7/GkI1EzXEWuLPDQYsSSmRxJCpYtiBqILm1ChO6wj+jLZCDTrEjheYwPT3TKjtVzscLdFRfZFqCwTpOOQY6Qr4chK2UVEt5d5Px/BnvAXGydxXaQnliykC0AatRQ7WCmj9oUjBgdl2j+E75jGWzqXjoJoLZYnVqgw/giEV0Z2ReEoXgfglFjDOgQliOBE5Oi15eN6fHI1u+oO/xK98+0pVVsjQbZbICHAjdP+Is1D6oqWVAhIyvJN0S5GigIleKJ0TTW0yavKr9aKcDrMr7MWpKJtBRFlBAduSljWW2jwwPrHT8QOeJJUKOJrhopWdiHc8BPoTMiS7uo5C7AvemoVma7GO1NazUVFpxn3suZi0heIe1GcchlLVz9V2GMhbZAWyxwX3hVe0NOgCA+10KkOZQvBNRLCwoh7eeiS6c9AZLIRNmCRdiijbEeGd67x5/+41pkAOinimG2tWcUx4pqX0ARPpDiygt+Lqjqu5J+bZA9ri+DACEoZsiMuezJbeQj00JLvFEZCvQwa+XPG1x30vu31olEgiHAb/tI+/H5oyIiW9LJTDlQBTDWZCLb252GegDHnCQ089yDwCr3nk3Upx52V8L6JATpEXZz5UGvvAR6E3e1CiJE+gAwT5Md4HeKaB/XAvcWQ+555QYLkgmodGYK8XRwUylt4y8uTcuem0aC/om1ZB0NdXunOBVpS4fbD0N6B9VA/M865GYhlPgS0Um/M6rhJJAAqD3Xllel7kpdF6W6gxTSg3x4jjozuhFKhOSQJZcomxZku3YltQopHiE7duchJs/iycQ8EzZsND2+CBeni5NjY/YDC8me6W6Cfw/sYenzTHD9gdDzLR6j9oPBBBEPvyYvsnYKTpnywyS+BQfErrgBAPGgIZU/OvJKE/PKwVtW0itAEUl1DfXqZRfJZipw80Zqf8H4/ZYat4ae5JDdwWdV1na6yBIx9pfKOK1y82ILIggJlo7y9voVtRBnsGstQu3IvC3QuINz43xTsqoZNYg3SJBaBrmSSYBXJc/iGtLcRiqTybujrXn7tl1tAdUcerFge6TbPvUk5QjsJ42wI1jzYhmuI0ni8AClvHLVBJspoiU7vxIAQA3N0Ho9v3I0ZN9i/VBdu1UheQXlc76CBJ4y3+U422/xkwH7LxlBIBSOhx53ED+ubZIs292+cvVtqoh6EyNJbbrBxum4W6WrD7yvQ8LYI8vddclGT122xko0Bzq461dMPY3Q5QoajUuBcbEABVcKpk7PYp7UFyiifwn6s0QcfoOj2n38y7MakeOzQKt2/aG5s9NuNzqD2BrjX4fDCNtN5cz3+t7Uz83YKvA7FbpOl0euw0aycj1bt2ahANJY/1F5TE3hUTBNEGd5iQL9fBLRwsMbciaRNDjpd2Tr4G7wJVGRGH0X14SeP3RYzdDNA24Xwl/yZsUNDo1H2IDomlyTUVsGl7xfUldUVbfKG2Dvf/Dqwstt+KIre7FpWu7QsVjWcCGCAWXUxrV9YpfeH4UYLbnLpQNG97zA0EVj10uAG9OBR6mfHLNiSjbVI6w6BPH5RT9Du27zSz5I6Snb86TZ53bL9pIGgy2v8xUxJaKDaiDBgC98FhMdYROJo191fYlUZDX4gUb5ZIuRasmPdxEgggeIyDSrgwMkWL7tgF207ukXHu0vfCHYgLG+xWIlGrOStvLD7hXau+2fA213VcOUX74Ckpdm4sx6dzmUqT/0WsQGVUui1UtyyK7klu7NqpKCl/kbMr8Wm0o4obsGoD09belzpAaARg+eBXKTZgFEK9MS/szpM93LTQm725oisagDrYyWgxwmGmDzEp/XwRHzTUTT9/0xyuLyZKeIngyocw8GJyMvz3zePrz07e2jdhwu2PbqrJWLqNhVnjYuuI7mS4iIr8Ezse8No1yCopb7o7BXUGOWPOC4c9LmeEa+dz8cRMfAP3E+dRMjb7WXLAPmpB4BXKoiDMwyw7wa44YvrilAQVpOrlNgS3r7g+52DtfeiWUUuZU0nYQCqWrN3nz8b/86LvPj9/hpwda9H3P+MDw9jx9eVjAkDSjwfe4/6X/ypXplwPg1gHTXdwnVxvHl8n4+ukD9DKW6ooi10HkVR60nqhkGp34srJ4egG1C0OuC8w9FK/KFcekGN+WZXs/8KjBIaOjtDiJ0d4AdKtL2hBBLKKrY3igWEVnyFBhT2C5bymDiGezCiuzILEAGFDWjte5WV/tzH/gAcx4N8Ptxu8spa5HO5V2zhV7QeTvK1lilpH+RLt0qk+hRR2Ckl5I9bTSzqsI4XBVn1XmGolptOrolvX9pJ2uloI0ftW2C/aVdhrgSDFrkPPQA8+f8Ga+gOeXYA0dx2nW7swQocHTsrzPDwB8hHPcOUpcw5t99hy//i8XJw1xPl1cF+OoY+yAUprXqro38HQd2/Z8BjiuSRLhCQzP1CIHrhAYZ1n2zyl42w49sCHQgmkCCMOZlsexCvu4QmqVio2T1GkX4eoXADNZdMHPAMxH/e9x+7z8bMDunYGjViweZpvJgxw/Kv3Vydv3/aNDVn7NhVdyp8WIUGTMBkND29yb3Ed1lPTRGfi+vWgloH35DKkA4l5F/eT7kFA7oFdUefDk6OjH38cPnny9OlPTmUkFhPDopgAl9GyYdMDfHwufIkb97CmmOtp9AN9Pg3WeNXcDcm5niSTJze5m7qhHnSKzql4hi5uwA5/bLinHEMtHDwY+k8hH6PNSvL/dEx1E9qH9LDq0vv2Czz4ymrHT2xcjZ0osssFzEDbDHa1RrsGuqTbmTRAKqBP9Nm7+7jJkp/4K5WmuhEDeQrtwwyYUKpRUFYSvgc23h4lNNccBJNiYMb9ABtMN3wqjh6mtM88xFagbXSfHt5Q7VZP8JDTHtXaIRqydOr2NI6e2SlSCI2huUqFn9a5nlsCT3IcN/3msNxN1zzCZ+0NvqAjsNBTAjNxaBCgy42/jNmfTcwuHnzRD5oTl3GAVxJHDpze1yP+KkL1JDalxqmQ4jp9qyu3gieBmJKOQwg1dgdXA8bTVNkBupcHPnuhALJSIa+UnsSOvi3LZsXQPHoXBTe4Ifs8SnPwrqBerm49F+hpNlkUAGU+D0M8tq2PCSXF7lupgNQBqHMm18u9WMPJH5vkTosQCivlO1aK933v6U8/Y6whr+o+/cnKDXtVW2glhTsN7wCCFwsyF2vipn9AKFYjjkbuSV3+o01RQOQvpTlg+3viNk+NIOq+R8Ct/aQiB0XCCay9uYKgKJcpJbEPABcrod0AQU6s4TcYq4w4MVYhka2I9Ob2nKf8T8xbDm+dt26ICG6MEC9bWv8Pax6MK1cT0owBlqu2c5+JpQxDbHjj8YrcFClO2tMRotxJod6dGFCnZfLSKK1zzsbsMB0rI32NY31kHmRh2MYD8/uyjS1JAMeFqZ6zb66QD5RVYSZ4e9MAtEVpTMDv1w/JVUa1n7bsUQvJZH67mqmVOmRHm9fn/krn37sbOFb6SfcmsW9v4hqJ7TG3n+MrEr12mX2b3HbLjvgG+azoRGikbvGga9FA5MnQ2unZRYPzPXYriNnHzPnZqapkUbRA8ZDQyRUksK6b+PbbNLNFGpgTE4qmVIp5zanLewqyU9IqANKxyIjE9B+REU6fwkQKKzXsA5d7WFdK6kPvkZoLK8EcsrzDmQfFe16xTO+UhbSRU/RMXWyz5r1G9j0rW4l9C5k5ygXOCXM/64UIhJ+qCATFPkIyH0IVgl60VQK26bSkhXkjS58aL3MA483tVmlhBboGzzdqdrdW22fCMTkczlgA4YriEqD7d/GipkEWkiT2zvXXGdS71/20fAjkeCsRBOP2bcCK2qVQH6ZjxHZ2/vpBWEj6c1hsOOHYymlQ/PUKFagk6EYd7s3Q9WFSOyXPR1VdSA9LsKKHbr/BQ9Hj4tsub32Lly61ED1ckToaPDyI6TSVW5gGs1DUPh1oPXdIogeEuOkxg0Se9mHce0q8WgTY+0Rdj82z9Xrb/EijTkVBhEMD7PidLwE6gXnk0/dDtA6FrgGOluQv33OaLzot4pdhvg+i7bYGgpseKEvcRUFbv7x8Yz6/xT1zkjUGCf0xLq0BfeMI0Oi/v6sFTCS/2JloMcP2HQzcqkdja57bx99X6Qr+/DUdKQT8YG8voGa+7qZRBt613DXDgT+zDR5gHL6vPWfX191HCfy57jr1vR1r12XnDsug2iOwqDoisvyYDX/XlI1qM5t2+9fPiIrRzHhy3wNTV1xN3Z00XIYfrdcY3fAU0P14j/5KxN+i/PhrMwCzUVnxbXmAute59XYdTG56vQJf1e2ZHc+WfWPqG0p9fKXNCbWfGHi2Ojx+xqmuGHcPusdEPqJpl0YxvdVbqKNwvR+4mnz6140+JY7tBkTYlsdRdPVH5QnfB6anIqQ6e2X4uJtPBulS21nuUtbNwhPHTWiG0fDo/to2L8naJ+jRlrH5tBp8nRGav4oSgV9YFx9hmI3uNhwgGbe6p1s0Y0uvh59d1nKP6jaw7jqa+e91hLuFUxx/Lr/SGBiUplV02Ce3RAdn9BXVsfpyofgS7W2HrEgHdjPwpwm9Z4v8m2nWh9O1JYNLaYX56sCCv70zilI5oYjAWh1R9tvzjPz3rQ4Qf5YTbHu9uyCzBhfny0mEzeS94k2FeXivN7UPCRivWYy7aRybKZL7TkfiFiMmydMp9SimU/zkfTo1PQr9sXzn/wFcjWAd"
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
nbibcodes=$(echo $bibcodes | wc -w)
python -c "import math;n=$nbibcodes;t=math.ceil(n*15./60.); print 'Checking %i ArXiv entries for changes...\n(to prevent ADS flooding this will take a while, check back in around %i %s)' % (n, t, t > 1 and 'minutes' or 'minute')"
python py.py -u $bibcodes
# python py.py -u $bibcodes --debug # DEBUG MODE

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
on hasAnnotations(theFile)
	try
		set cmd to "strings " & quoted form of theFile & " | grep  -E 'Contents[ ]{0,1}\\\('" -- this triple backslash is IMPORTANT
		tell me
			set theOutput to do shell script cmd
		end tell
	on error
		set theOutput to ""
	end try
	return theOutput is not ""
end hasAnnotations

on safeDelete(thePub)
	tell document 1 of application "BibDesk"
		tell thePub
			--remove PDFs
			repeat with theFile in (linked files whose POSIX path does not contain "_notes_" and POSIX path ends with ".pdf")
				-- keep backup with Skim notes
				if Skim notes of theFile is not {} or my hasAnnotations(POSIX path of theFile) then
					tell application "Finder"
						set theSuffix to 1
						set thePath to (container of file theFile as string)
						set AppleScript's text item delimiters to "."
						set tmpName to items 1 thru -2 of (text items of (name of file theFile as string)) as string
						set AppleScript's text item delimiters to ""
						-- find a non-existing backup name
						repeat
							set backupName to tmpName & "_notes_" & theSuffix & ".pdf"
							if not (item (thePath & backupName) exists) then exit repeat
							set theSuffix to theSuffix + 1
						end repeat
						-- change file name (BibDesk will properly reference it automatically)
						set name of file theFile to backupName
					end tell
					-- delete PDFs without notes
				else
					tell application "Finder"
						delete file theFile
					end tell
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






