#!/bin/sh
#
# Rui Pereira (rui.pereira@gmail.com)
#

# ugliest hack in the world - harcoded/compressed strings of both applescript and python scripts as in the automator actions
py="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"
scpt="eJyVVlFvHDUQLrzd8idGfig5KZemBYSooDQlDS2gNGqKxAMvvt3ZO5Nde7G9SU6kEj+dGdt7671eIUj74LW/GX+e+Wbsvz99d/rZgweLBbztFVygRWUlfGt7ddTFn+erVqrmqDTts4Jg5+Ya2yVaeHJ8/A1N8NxSOqzA6Kf8Aydd1+BlaVXnwRsojb5G66EyN7oxsiLkC7X0eAtSVyCXzltZelC6NraVXhnNVpJBp+iuALW3m6Pg+SejpV9LDZeqvDqEP9Kvo7/nrSyZ4yGc9Kveeab3dVGQs5U1N8258apWZXB/4JVvkLY9hApdSYN5MfPYNCCJeQKBuNw4jy28vCYCThSz2WLxI7sC5cD2Wiu9oklVw0Fpeu3B0AjppBvorCnRObhZG4egZYtsI4L1K2worhQiMZ/DMzgGv0ZNfvYQ2MEzaGZxpYiWBemm4BQtAZLc6Oy0Dv4aFifz4j2dvpZ94+8JD/uHqQ3cKL+OB9sPhhBiGAId4sx6YKop5hP6E1eCAqiMVX5D4eGdTO/BeUryhjkgqYaDVcShqotxigcf5DuogDJGEut6X8yKmUOfq/RzR9a3JEHOd4WNamlkHctQgIjwYMszB3Eko838fzm7u7tL7ijrF6dnZ4qDRD5Hi8eso7DFfIt8F4M5wT3ZgzvpKVZ2B/jFPuBQdFPol3uglJOXXIA70K92ofeMgODwfyj1IfNFqoPKlH1LdQePOeOLhUNpy7UDahEkcIuy2gDeciUQpuuXW09BmHhLZ2s2TB8cKyuqkdtNrSz1BhkCxa7H8j2Ie4QthpjvlCgRoeOgRzANtztMJdmh9HFnTmu/pMDsdxfw+Z6RiONgRtO0I1MNNUELOeURyG3VS0X1miV+4JmiGJFphshbbKl5AwnPDZM75IMgiX2j9BVytKh8B2jgPWBI/iQhaoFz6s+Viw7EUVfVIqext6+dKV2hFSNklqJah3KIO4yrWb2PE1z14188RbEXn3xPYtFu9twK4rSPJHGiqBi0ShyC+F0IeDgW5MMwk5KakZoyGheilGVFqcWbfA9eGJoCZZbqJOY8FBBfK6rtDN2gtTVtXpPz7b2RnS45gpKs4QpD4a5Qo6WDVePsNoFbo3bzAy3+HC0GXJJ9ELwrpdbkQ1rqxYMwVD1pKM7T6iCHtffd00ePckW08grD8ZPCfn37SwRX0ssgr62rTGKkUA4jhWI0i9tj45JUhnPLrLftdVfspGuxCLqrqSKr77MzDf35X/TNuTy4eHP5+retdpPVnLdf0mUd3gkZ86ykqKRN+C9SfZI9vRPoo7uUHkC8dAhLumwod2u+8zUffHtumPJMdqKm1xrpNaPJ+dPUD5mu8mymDZy+eR040WWLjtsoB58wFmF4xCzlMuuiWfe6lk2fehOSMERllIDvqLvP8+L/71wP1O+V6t0Si8Od10AcjqOCDh9KvfhI0Z9PS5Fj9PFiZ6I8uy0Vikl4c9Droij+/OToHygckz0="
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
    sleep 300
done

#clean up
cd -
rm -rf $tmpdir


