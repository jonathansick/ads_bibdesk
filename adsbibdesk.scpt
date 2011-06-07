--ADS to BibDesk -- frictionless import of ADS publications into BibDesk
--Copyright (C) 2009  Rui Pereira <rui.pereira@gmail.com>
--
--This program is free software: you can redistribute it and/or modify
--it under the terms of the GNU General Public License as published by
--the Free Software Foundation, either version 3 of the License, or
--(at your option) any later version.
--
--This program is distributed in the hope that it will be useful,
--but WITHOUT ANY WARRANTY; without even the implied warranty of
--MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
--GNU General Public License for more details.
--
--You should have received a copy of the GNU General Public License
--along with this program.  If not, see <http://www.gnu.org/licenses/>.
--
--  Based on:
--  AppleScript to convert downloaded Bibtex and abstract information to a BibDesk entry.
--  Jonathan Sick, jonathansick@mac.com, August 2007

on growlNotification(titlestr, descstr)
	tell application "System Events"
		--Growl is running
		if (count of (every process whose name is "GrowlHelperApp")) > 0 then
			tell application "GrowlHelperApp"
				register as application "BibDesk" all notifications {"BibDesk notification"} default notifications {"BibDesk notification"}
				notify with name "BibDesk notification" title titlestr description descstr application name "BibDesk" priority 0 without sticky
			end tell
		end if
	end tell
end growlNotification

on hasAnnotations(theFile)
	try
		set cmd to "strings " & quoted form of theFile & " | grep  -E 'Contents[ ]{0,1}\\('"
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

on findAnnotatedFiles(thePub)
	tell document 1 of application "BibDesk"
		set annotatedFiles to {}
		tell thePub
			repeat with theFile in (linked files whose POSIX path does not contain "_notes_")
				-- name without extension
				set AppleScript's text item delimiters to "/"
				set fileName to last text item of POSIX path of theFile
				set AppleScript's text item delimiters to "."
				set theName to items 1 thru -2 of (text items of fileName) as string
				tell application "Finder"
					set thePath to quoted form of POSIX path of (container of file theFile as string)
				end tell
				-- use shell (applescript is way too slow for this)
				set cmd to "ls " & thePath & "*" & theName & "*notes*pdf | xargs | sed 's/.pdf /.pdf;/g'"
				try
					set AppleScript's text item delimiters to ";"
					tell me
						set annotatedFiles to text items of (do shell script cmd)
					end tell
					set AppleScript's text item delimiters to ""
				end try
			end repeat
		end tell
		return annotatedFiles
	end tell
end findAnnotatedFiles

on run input
	
	set AppleScript's text item delimiters to " "
	set input to (input as text)
	set AppleScript's text item delimiters to "|||"
	set thePDFFile to (text item 1 of input)
	set theTitle to (text item 2 of input)
	set theAuthor to (text item 3 of input)
	set theAbstract to (text item 4 of input)
	set theBibEntry to (text item 5 of input)
	set AppleScript's text item delimiters to ""
	
	tell document 1 of application "BibDesk"
		-- searchs for already existent publication with exactly the same title and first author
		if (count (search for theTitle)) > 0 then
			--delete old one
			repeat with thePub in (search for theTitle)
				if (count (authors of thePub)) > 0 and name of first author of thePub contains theAuthor then
					my safeDelete(thePub)
					my growlNotification("Duplicate publication removed", "\"" & theTitle & "\"")
				end if
			end repeat
		end if

		-- add new publication
		set thePub to first item of (import from theBibEntry)
		tell thePub
			set the cite key to generated cite key as string
			set myCiteKey to cite key
			-- old scanned articles
			if theAbstract starts with "http://" then
				make new linked URL with data (theAbstract as string) at end of linked URLs
			else
				set the abstract to theAbstract as string
			end if
			-- file found?
			if thePDFFile ends with ".pdf" then
				add (POSIX file thePDFFile) to beginning of linked files
				auto file
				-- this is not a file, but rather an URL
			else if thePDFFile is not "failed" then
				-- only add it if no DOI link present (they are very probably the same)
				if (value of field "doi" = "") then
					make new linked URL with data (thePDFFile as string) at end of linked URLs
				end if
			end if
			-- add old annotated files
			repeat with annotatedFile in my findAnnotatedFiles(thePub)
				make new linked file with data annotatedFile at end of linked files
			end repeat
		end tell
	end tell
	
	-- growl
	my growlNotification("New publication added", "\"" & theTitle & "\" as " & myCiteKey)
	
end run

