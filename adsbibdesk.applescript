-- Rui Pereira <rui.pereira@gmail.com>
-- November 2009
--
-- based on:
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

on run {input, parameters}
	
	set AppleScript's text item delimiters to "|||"
	set thePDFFile to (text item 1 of text item 1 of input)
	set theTitle to (text item 2 of text item 1 of input)
	set theAuthor to (text item 3 of text item 1 of input)
	set theAbstract to (text item 4 of text item 1 of input)
	set theBibEntry to (text item 5 of text item 1 of input)
	set AppleScript's text item delimiters to ""
	
	tell application "BibDesk"
		tell document 1
			--searchs for already existent publication with exactly the same title and first author
			if (count (search for theTitle)) > 0 then
				--delete old one
				repeat with thePub in (search for theTitle)
					if (count (authors of thePub)) > 0 and name of first author of thePub is theAuthor then
						tell thePub
							--remove PDFs
							repeat with theFile in linked files
								if (theFile as string) ends with ".pdf" then
									tell application "Finder"
										delete file theFile
									end tell
								end if
							end repeat
						end tell
						delete thePub
						my growlNotification("Duplicate publication removed", "\"" & theTitle & "\"")
					end if
				end repeat
			end if
			
			--add new publication
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
				--file found?
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
			end tell
		end tell
	end tell
	
	--growl
	my growlNotification("New publication added", "\"" & theTitle & "\" as " & myCiteKey)
	
end run

