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

--http://foolsworkshop.com/applescript/2008/05/an-applescript-replace-text-method/
on replaceText(find, replace, subject)
	set prevTIDs to text item delimiters of AppleScript
	set text item delimiters of AppleScript to find
	set subject to text items of subject

	set text item delimiters of AppleScript to replace
	set subject to "" & subject
	set text item delimiters of AppleScript to prevTIDs

	return subject
end replaceText

--http://bylr.net/3/2011/09/applescript-and-growl/
on growlNotification(titlestr, descstr)
	-- this should work with Growl and GrowlHelperApp
	tell application "System Events" to set _growl to short name of every process whose creator type is "GRRR"
	if (count of _growl) > 0 then
		set osascript to "
property allNotifications :  {\"BibDesk notification\"}
property enabledNotifications :  {\"BibDesk notification\"}
property titlestr : \"" & my replaceText("\"", "\\\"", titlestr) & "\"
property descstr : \"" & my replaceText("\"", "\\\"", descstr) & "\"

tell application \"" & (first item of _growl) & "\"
    register as application \"BibDesk\" all notifications allNotifications default notifications enabledNotifications
    notify with name \"BibDesk notification\" title titlestr description descstr application name \"BibDesk\" priority 0 without sticky
end tell
"
		set shellScript to "osascript -e " & quoted form of osascript & " &> /dev/null &"
		ignoring application responses
			do shell script shellScript
		end ignoring
	end if
end growlNotification

-- check for PDF annotations produced using Preview or Acrobat
-- with some shell magic not fully tested
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

-- given a file (or folder) return a list containing
--   the path to its parent directory,
--   its name without its file extension, and
--   its file extension
-- http://www.alecjacobson.com/weblog/?p=229
on parse_file(this_file)
	set default_delimiters to AppleScript's text item delimiters
	-- if given file is a folder then strip terminal ":" so as to return
	-- folder name as file name and true parent directory
	if last item of (this_file as string) = ":" then
		set AppleScript's text item delimiters to ""
		set this_file to (items 1 through -2 of (this_file as string)) as string
	end if
	set AppleScript's text item delimiters to ":"
	set this_parent_dir to (text items 1 through -2 of (this_file as string)) as string
	set this_name to (text item -1 of (this_file as string)) as string
	-- default or no extension is empty string
	set this_extension to ""
	if this_name contains "." then
		set AppleScript's text item delimiters to "."
		set this_extension to the last text item of this_name
		set this_name to (text items 1 through -2 of this_name) as string
	end if
	set AppleScript's text item delimiters to default_delimiters
	return {this_parent_dir, this_name, this_extension}
end parse_file

on safeDelete(thePub)
	set keptPDFs to {}
	tell document 1 of application "BibDesk"
		tell thePub
			-- always keep PDFs marked notes
			repeat with theFile in (linked files whose POSIX path contains "_notes_" and POSIX path ends with ".pdf")
				set end of keptPDFs to POSIX path of theFile
			end repeat
			--remove PDFs
			repeat with theFile in (linked files whose POSIX path does not contain "_notes_" and POSIX path ends with ".pdf")
				-- keep backup with Skim notes
				if text Skim notes of theFile is not "" or my hasAnnotations(POSIX path of theFile) then
					tell application "Finder"
						set theSuffix to 1
						set {fPath, fName, fExt} to my parse_file(theFile)
						-- find a non-existing backup name
						repeat
							set backupName to fName & "_notes_" & theSuffix & ".pdf"
							if not ((fPath & ":" & backupName) exists) then exit repeat
							set theSuffix to theSuffix + 1
						end repeat
						-- change file name (BibDesk will properly reference it automatically)
						set name of file theFile to backupName
						set end of keptPDFs to POSIX path of (fPath & ":" & backupName)
						-- also try to move the .skim file
						set skimPath to fPath & ":" & fName & ".skim"
						if skimPath exists then
							set name of file skimPath to fName & "_notes_" & theSuffix & ".skim"
						end if
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
	return keptPDFs
end safeDelete

on run input
	set defaultDelimiters to AppleScript's text item delimiters
	set AppleScript's text item delimiters to " "
	set input to (input as text)
	set AppleScript's text item delimiters to "|||"
	set {thePDFFile, theTitle, theAuthor, theAbstract, theBibEntry} to text items of input
	set AppleScript's text item delimiters to defaultDelimiters

	tell document 1 of application "BibDesk"
		-- searchs for already existent publication with exactly the same title and first author
		set keptPDFs to {}
		if (count (search for theTitle)) > 0 then
			--delete old one
			repeat with thePub in (search for theTitle)
				if (count (authors of thePub)) > 0 and name of first author of thePub contains theAuthor then
					set keptPDFs to my safeDelete(thePub)
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
			repeat with keptPDF in keptPDFs
				add (POSIX file keptPDF) to end of linked files
			end repeat
		end tell
	end tell

	-- growl
	my growlNotification("New publication added", "\"" & theTitle & "\" as " & myCiteKey)

end run
