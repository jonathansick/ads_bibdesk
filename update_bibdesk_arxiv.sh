#!/bin/sh
#
# Rui Pereira (rui.pereira@gmail.com)
#

# ugliest hack in the world - harcoded/compressed strings of both applescript and python scripts as in the automator actions
py="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"
scpt="eJyVVlFvHDUQLryd0P6HkR9KTsqlaQEhKihNSUMLKI2aIvHAi2939s5k115sb5ITqcRPZ8b23nqvVwjSPnjtb8afZ74Z++9P351+9uDBYgFvewUXaFFZCd/aXh118ef5qpWqOSpN+6wg2Lm5xnaJFp4cH39DEzy3lA4rMPop/8BJ1zV4WVrVefAGSqOv0XqozI1ujKwI+UItPd6C1BXIpfNWlh6Uro1tpVdGs5Vk0Cm6K0Dt7eYoeP7JaOnXUsOlKq8O4Y/06+jveStL5ngIJ/2qd57pfV0U5GxlzU1zbryqVRncH3jlG6RtD6FCV9JgXsw8Ng1IYp5AIC43zmMLL6+JgBPFbLZY/MiuQDmwvdZKr2hS1XBQml57MDRCOukGOmtKdA5u1sYhaNki24hg/QobiiuFSMzn8AyOwa9Rk589BHbwDJpZXCmiZUG6KThFS4AkNzo7rYO/hsXJvHhPp69l3/h7wsP+YWoDN8qv48H2gyGEGIZAhzizHphqivmE/sSVoAAqY5XfUHh4J9N7cJ6SvGEOSKrhYBVxqOpinOLBB/kOKqCMkcS63hezYubQ5yr93JH1LUmQ811ho1oaWccyFCAiPNjyzEEcyWgz/1/O7u7ukjvK+sXp2ZniIJHP0eIx6yhsMd8i38VgTnBP9uBOeoqV3QF+sQ84FN0U+uUeKOXkJRfgDvSrXeg9IyA4/B9Kfch8keqgMmXfUt3BY874YuFQ2nLtgFoECdyirDaAt1wJhOn65dZTECbe0tmaDdMHx8qKauR2UytLvUGGQLHrsXwP4h5hiyHmOyVKROg46BFMw+0OU0l2KH3cmdPaLykw+90FfL5nJOI4mNE07chUQ03QQk55BHJb9VJRvWaJH3imKEZkmiHyFltq3kDCc8PkDvkgSGLfKH2FHC0q3wEaeA8Ykj9JiFrgnPpz5aIDcdRVtchp7O1rZ0pXaMUImaWo1qEc4g7jalbv4wRX/fgXT1HsxSffk1i0mz23gjjtI0mcKCoGrRKHIH4XAh6OBfkwzKSkZqSmjMaFKGVZUWrxJt+DF4amQJmlOok5DwXE14pqO0M3aG1Nm9fkfHtvZKdLjqAka7jCULgr1GjpYNU4u03g1qjd/ECLP0eLAZdkHwTvSqk1+ZCWevEgDFVPGorztDrIYe199/TRo1wRrbzCcPyksF/f/hLBlfQyyGvrKpMYKZTDSKEYzeL22LgkleHcMutte90VO+laLILuaqrI6vvsTEN//hd9cy4PLt5cvv5tq91kNeftl3RZh3dCxjwrKSppE/6LVJ9kT+8E+ugupQcQLx3Cki4byt2a73zNB9+eG6Y8k52o6bVGes1ocv409UOmqzybaQOnb14HTnTZouM2ysEnjEUYHjFLucy6aNa9rmXTp96EJAxRGSXgO+ru87z4/zvXA/V7pXq3xOJw5zUQh+OooMOHUi8+UvTn01LkGH282Jkoz25LhWIS3hz0uiiKPz85+gdcTJQ8"
tmpdir=$(python -c "import tempfile; print tempfile.mkdtemp()")
python -c "import binascii,zlib,cPickle;\
           out=open('${tmpdir}/py.py', 'w'); print >> out, cPickle.loads(zlib.decompress(binascii.a2b_base64('${py}'))); \
           out=open('${tmpdir}/scpt.scpt', 'w'); print >> out, cPickle.loads(zlib.decompress(binascii.a2b_base64('${scpt}')))"

# go the tmp directory
cd $tmpdir

# fetch arXiv bibcodes from BibDesk using an applescript
bibcodes=$(cat << EOF | osascript -
tell application "BibDesk"
    tell document 1
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
end tell
set AppleScript's text item delimiters to " "
return bibcodes as text
EOF
)

# check for changed bibcodes
python -c "print 'Checking %i ArXiv entries for changes...' % (len('${bibcodes}'.strip().split()))"
python py.py $bibcodes

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

# update bibcodes
for bibcode in `cat changed_arxiv`; do
    echo "Updating $bibcode..."
    # delete previous arXiv version explicitely
    # the automated same author/title check fails a lot
    cat << EOF | osascript -
tell application "BibDesk"
    tell document 1
        set pub2delete to {}
        repeat with thePub in publications
            if (count (every field of thePub whose name is "Adsurl" and (value contains "${bibcode}"))) > 0 then
                set AppleScript's text item delimiters to {"{","}"}
                set theTitle to (title of thePub)
                set end of pub2delete to every text item of theTitle
            end if
        end repeat
        set AppleScript's text item delimiters to ""
        repeat with theTitle in pub2delete
            set theTitle to theTitle as text
            repeat with thePub in (search for theTitle)
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
            end repeat
        end repeat
    end tell
end tell
EOF
    osascript scpt.scpt `python py.py ${bibcode}`
done

#clean up
cd -
rm -rf $tmpdir

