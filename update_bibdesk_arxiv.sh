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
py="eJytO2l32ziS3/Ur0NKmSXUkOnbe9OSpIyfuJJ54Xw4/23kzPbJWA5GQhJgi2QBpRZvO/vatAkASPGQrhz7YPAqFQqHuAns/HWRSHMx5dMCiW5Js01Ucdbrdbufk5SVJY/I7n79k8oYMh2QhuJ/yOAqZlISvk1ikJF4QBEyyech9im/hVVSO67yIk63gy1VK3Bd9cvTo8JCQi4yTcyYYF5Q8FRn3En3zfLmmPPT8eH1MaBR0SMvvv+OIpisakUvu35CnH82thLvna+qrwZ3O1YpLkoh4KeiawOVCMEZkvEg3VLAR2cYZ8QGHYAGXqeDzLGWEpzjpQSzIOg74YtuBB1kUMEHSFSMpE2uJy8Wbf7z7QP7BIiZoSM7V0skb7rNIMkKlZoZcsYDMtx0EP8XZL83s5DQGrIpVA8I4vBfklgkJ9+RxPoHBNiCx6Lg0RYIFiRMc1AcqtySkaTnOay64XFcA+6FwruIElrECbLCwDQ9DMmckk2yRhYMOQJJ/nl29fv/hipy8+4P88+Ti4uTd1R+/ASSIBLxlt0zjgZ0POaCFxQgapVugufP21cWL1wB/8vvZm7OrP4Bscnp29e7V5SU5fX9BTsj5ycXV2YsPb04uyPmHi/P3l688Qi4ZEsQ6d7BzobYDuBawFGRDwlL/gM2TQFIYkBW9ZbCJPuO3QBAlPgjb/XvUoWEcLdXCALLkG1B0tiBRnA6IBMqertI0GR0cbDYbbxllXiyWB6HGIA+OgZDfqYRZYdtKVQlQVWiWxmuaAuVU6QuKQUVsB6RNbAfkJFtmMgUlefT3TucsSoDra7rFbYojlq9rEYdhvOHRctQZqpnpHLYaZiIJXTLy4eKNeT7ncz8OGNxR8S9+W4UrnvKARSlfcCaU1hu1lluZX8bFlWD5VcrXxTVIZUKFLN+xdbLgYXEvY/+GpZ381l/y/DITYcjnR9atRlSMzOawMz5aG9AqmXQWIl6T11dv35wjnMhtUPlEQ6zSdYiLSrcBWxSWKqJrdoQMSWIwUJ1OD0RqQbNQrwYlHGUNiADLEIayo+n2JEsNnAFzHz/qdzrwDPaGR25/pMwU8g7/KzqMpkq0J6CpWeSvFDAJ4zipgCd6IeOCi957NVQvx+1bQB4NgplG7DrDwBkQZzgM2DxbwiXIXTruqrvuIF/Y+JSGaEO0FI67EkSSzVKRse5uxJlGnCVgotiMik/81tkfo1k4QIiU+yE7ewlrM9Oof4BxKWFdCroHCgriKNgC7H8EG03U/rkaCw37oNDRgi+JkidFscAdHZPzcoxhEl/kk3uKDaPCe6gxE0ezagqDr4DenIA1rIonIdhtsczWIDWSDHPNkajUoJgJWm1lLUCt6pPZjEKzB5LnFovvk2NyWFLig8YvwWTgdgOYY+4LLjsbp18AozSChzC0oBFnEVAoYDZrglHFSfaIDBlL1NjDv4EVA/4FsBuwDuACGPBUWYYFyGEAFqQyFsXbU8Pdw7/1K69guVUmjhquORGgVKRrqO0WdNfIAwOGPhL4aVkoCQYyl7AKPA0kmDNgV24aPLjIIgn+J3VdB+0zcM2QBsCzNRciFs4UWAnW7uCBdMiDfBZ4hix2+t+6Nk0NLE1f1Fam6FMGGleGJqmUWms9sBh4X1osV00+Vn/7dWCtMq6e7zvI9oAFKfukSTc3dWzlGwwf3oHDGcGqKrSSBXhg1gzL9qDFouf05OzNh4tXo5YZf+o2BoIApzzK2G5yvVxDfhrnW72LF84D7pEHEsIGEDnQjTUjWkTc6OHhoBSUJvL+DozHx7lSt0s8A3O5DzUQdOSIGvQ0524wxQz1/DAGeSmsaxSLNdX+rNOkpkdeMoxqOcQWGwwLN8xRgRYNuQmPPHIFAr2MAQlX1nAJ9ppijKGD/Nwe4q9QViW0cFlaqcmjqVHTci16DxUmI26VZUIA4rFPoOZmMZrg+5RsbwXbrVwwSbAARw1MU7jBePIU/y24gNgMYrtVLAZFMKV2CUW4svU98uHqdPgELDY+LjXGbLzjfYQYxF3TxA3peh5Q8mlEPnka2nWydDF84vQHZIJkAsvPX566cOv89ddfzqBVt/b5ITKzlh+ASTNC7eyPwFaw8wcgM6o7mwHO2cztT8Hk64itEE0ezcCV5EI5yhUmBPHWrzDoppYYaP9vwFAAUQdVuGDCcpUFY2CNIBgfoICBBnGJw82ElrsWLM1EpAMB89ITjAa5wCMNVcen3Z6BNZSU0TvYjJgUkgwEAJQn/RUDIzceg8zZim8532dNBf4ub5tztuFs7/ESRjWAMqfhYVOxrcc5QRw5YLGoTHGfEiYWzE/DLdiqOMAFIF93xhKYdXgGKDcAOfNzePbJZ0mRo3ivr67OX+Fy64TUs6hn1VkxstuDq44CxBTT2Y+be3DU4qoiEvlqyKkGfnXu6oWlkFIAFzhwGMJsFHO91ELI7V+DqWaiBltL/LnCgCYJwWQCkSq6HfAqqE6N5LSO4HukFXLQIVa8QAVmf2ZMbL/a4GiOjuqbVNsgCMchxkhXsC5Hko2IayH3fjKGP2Mt0E/mtkpzKN9MFoI0aClyMFdA7Y9YCgbM1nt03wlNMHUuDYfKuZCXmK3y6CMoUuHdiWJPaSIQP8cExjkwTgwnUoZOcx6e9ydHo2l/8EPsyrfvVGWHDN1miwwDN0zXjyiJuM9aSinAIbN2xd2SpchgRS+kzlJTK202Z1gCyIRCqV/bVtBeY4lJZ7a4BS2cGO00ZU2GlnZ/B1PzHdNXiqv6ciHoElNgS4qb8WsxuZb6kpkYO2KlUcTZHPzlCtLzlqCzIcjmgbH4nY4fUikr+X08R5Es6yxvaQS7I5WZsGsHcYRVzxsjxmTN1rHYejYqlXhSHytKJihTXh2yTwpDVU2Diu0w5De4FIiNF9RnXlGwURcYRsxmPOIphBaShQvLp+Ot3shz4C+m+SYIUJoSq1iORbeu8/r921cY4DkoQHNdNrRSf4VnVsoWYFKbCOLprai4pSLwWJDdowuODyMgHMqGKNRyvoQNvm9IdoMjIBuB/GK5omuP+l52c98oJmMcBv+0B7sbWsV7gntZxIcrBoYonDOx9AK2z0AeUUkjT9y7eARe09i74ezWy+heRAGfYi/JfMij9oGPI29+L0cVP4EOYOTHZB/guQb2o73YkfmUekyAXQLW3DcCK9k4KuQJ95axxwNn2mmRXpA3LYIgry91XQa1SLp90PTXIH0q2wnymo20lKfAFrHNeR1XiSQEgUEzKUxFT/kg1N4WakyJzc0x4vj4lgkBolOSoDS5xFjTpRu2LSjRSPGJW1c5Djp/FgWQzo3J8NBWeKAeXq6Nzg8IDG8G8yX6Cbyf2uNlc/yA3NIwY632Q40HIhTEvmux7RMspGmfLDJL4Ih9SuuA4KUaDBmr0mZJQn94WEvZ21hoAwjKwTFepnFylmIdEyRmJ/8fjslhK3vV3JMauM3quszWlgaGfKTxjSpWv2ivZGEIM6nOZt4gsLwMVkR4KV3YacPeDPgbn5rSBAqhI61BOoEE0DWXEmNcits/VHsLkQYXnk1dfdWfu6X77o5UPa/mB7pNte+qiKcchf62BSqINxGq4iwJFgCFhfEWKClXM1zUbjwIAQC3d8Ho5sSIqBbCl+qG7dqpC0geqv0B4KSxFv+petv/DIgPuUaqAgEIv7CvugF582yW5tbt8xcrWtPDUBga2212DpuCkc6F7Kq5ep4WTl6916soyeq36chGgORWDWtphrF2H6JAqUTqTmxAAMR6qeCJ21dhD5JTPIH/VKQSDaPr9Jx+M6vAYHTsqFHYnGov2/bInAaQWQNda7D5oBppvXWQ/1qLtfi7AVsHbLdI08nC2Glmhoart+3UIBoVPNZfqBD9tpggjDfYP8N1uQ42qDCB3jLZxoYcr+oLfQ3eBYoyIo7iu/Aqid8XMdZqQNqY85XrN25DOY1O3YZol1iqXFMAm7pXXF+qmm+LLdTa4f7fgRXF9ltR5HrXItK1rldRVlcAA8TSs/Oo0haOH0hs4uo02LztETdkmNOpoxtoxSGNzYxdtiGJagKrExr6bEU5Rb9j204zS24oyfnLU/msY9tNA6EmU90tM6VCC8lGnMGCwHxQ2Ix1DIZmTf0V1txR0RcsxZslUq4Zy4I+TgIOBA+pqAQ1ik3SouuR4baTW2Scu7S9cAfswvaBFUjUkr/KG2ud8K5V3mx4e9V1XDlF++ApKXamluHTsUylhfE8ESAyIt0WolsmRXcEN3buVKSUv/P5Ffs02pHFqQx4hwK80A5CIwDNB7uqfAN6IZQb88Kuq9nDTYOgWXksar4hiIMdjBYjHGKqLJPSzhf+QUNN+/mb5nB9MRHMk4wKH9zA88nJ8N/Th9efnbxxYdyE2x9Nq8FYuk2Y2eOiMabueLSIi/gTyw/w2jXIKiFvujsEdQb5wpznDnlYzgjXzufiiZl4CvcT54Ecm24dH5CPmhF4hbwoCPMwypZY80dMX5ySoIJUvd2G4PYd16c4rM6OLoi1pDmVgA24YvHaffZ0/D/P++6z86e4smPN+v5nfGAWdnx9+VABIOnHA+9h/8t/lTtT7odBrJ2mO7iW15uH13J8LfsALbyliLPEdRBJpeKuNwqpdicunxyOpiBuSUh9hq5XVcNy4QE+5pdVzv4vPJIwdHSEGj85wgvgbn1DCyJwqVjaKB6YpeIzJKjQR9CcV6r+iedOiiuzIQlA2JBWP6+87O9W5l/wmAn8++Vmg1fWNpfDvWoZpyr9oJI3tUhRyyhdol461acQws4gKG/4evVSHUXizGCrvitUteLT1auiFtn2UvXxWgjRXTmsF+1K7DVDkGLXUc9ADiqnafpeLVpYg5deh3dFCPqYHZhIK51S+fhbGPr2DRkegzfmSo8gRMwPO6L9LFBYZ+02j9VROxx74EOaAzyAEQfzLQ2TFfXwdFcrFZvHyJCvQ1SyT6+yqcFPgRvHfe+h+2z89EBdO4OGJd88zhsdAxz/8v3VyZs3faMBVjW1Ign508KgaxImo+HhNNf166geWEodR+vXg1r83OPLSB2WzGuwn3QFASIHrGk6Hx4dHf366/DRo8ePnziVkZgKDItUABS+pZnUA3w0YD7HQwWwpxipafQDfXYO9njV7NTkq57IyaNpbmSmqoKcomkpnqGBGpDDXxvGJcdQM+b3Ou5TiKZUI1VZb3WEdhPZBwhVuV3Z+gUeyiW1ozE2rkaXTGnVAmbQFXcr11IdDZ2Q7XT54Mj1aUP75AE2gPLTiKXQVJtEEGWoHtGAMCEa6WAlXLunKfhAqrkCYEyKbhWr+TaYLtdUzDRMaZ/HSCw32agd3d/s7VZPFymTO6oVMzRkaZLtaRw9s1MEABpDc5cKK6sjNbcEnuQ4pv3msNzI1izCZ20NvqAhsNCr8GPiqEGALlf+0uN+Nh63ePBFP2hOXFpxWgn7KKz0rgrvVxGqJ7EpNUZFCa7Tt2pqK3gSspmScXCARu/gakBomgrbvfZyt2VvFEBW8tuV0JPYvrNl2ywPmPveIl0GM2SflWkO3uWSy92te/KeXiaJQ6DMp1GER8r1ESZZdAZLAVT5e31lfL3ca2k4+UMTmmkWQlokfMcK0H7uPX7yG/oaZVXdx0+syK5X1YVWUqjTsA7AeLZQ6mJN3LQPCEVqxKmRe1KX/1RrERD5S24O//4p3eaJFkTd133I1mpQEUEi4QqsvTSCoMiXmQpB7wEudkKbAQU5sYZP0VcZdqKvQiJbEenGe0BT+h3zlsNb560rIoIbJcTLlsL9/ZIH48rdhDBjgMmmbdznbMmjCMvVePQjV0XlJ+3pFKLcSKHcnRhQp2XyUimtM9hG7TAcKz19bcX6OD/wwiwbD/Pvu2wsKAI4bkz1G4DmDvlAWRVmgrfTBqDNSqMCfr9+gK8yqv0kaE8VgEzkt6sUWskidhRpfeqvdPy9u/xihZ/q3gT27SVYw7E95vZzfEWg186zb+Pbbt6pdQN/Vuq0aixu8BBuUf6jcmj1aXbR4PyMtQa12IfE+c2pimSRtEDyINWpGiSwLpv49tsks4UbGBMrFE2uFPOaE6F3JGSnSqoASPsiwxJTPcSFUPWZTiwwU8MqbtmBuhJcH8iPRcCsAHNI8vpk7hTveEUy3eeKVBumqHi6WCTNK4XkZ1IWAvsWMnPMDIwTxn7WCxYyPxUxMIp8hGA+giwErWgrB2zVaQkL8zKUPtFexgDGmtuFzkILyhM6BebWwmj7TDgmh8MZCyDcUdwCNP8uXtQkyEIiE+9cfzmiKu+6GpYPgRhvxcJw3N7Eq4hdCvlhOkZsZ+ev7oWFoD+HxXIRjq2cVMVfrxCBSoBuxOHOCF0fdLVD8nxU1YT0MAUrKuD2GzywPS6+O/PWN3jpqgKghztSR4MHGzGcVukWhsEkYrXPGlrPRCrWA0JsWcwhkFddFPeOFK/mAfY+7dcjQbZeb5sfkNSpKIhw1ADbf+dbgEYgiH31bZPah0LWAEdL8Jd3jIJFp4X9PMq7GFpvayDYskBeYg8Edf3y8rX5NBg73orX6CT0h8JqD9T3lwCN9vunmsNE8ou+QosatvcfsNGOytb8pgB/XyUr+PPX6rgj4Ad9ew4583U3jTOwrmXPCwf+RjZ4uHL4vvacXF93H0j4c9116p0Zq2eysz8yqNYILKqOFFl+QoZ/aspGtZlNsfzrZ0TBaEY8ue2BqSumpm5OGibDj9dr9G54huduvEc/EvG3CD/+2hTAtBkrti13UHcat96uQ9NNq1fgq5o9069s6fqquiHXh0/ajFB7v//p6vD4KVV5xbh70D1W5COadm4U01u1hToK1/uFismnf031CXYsNyDCtjhOeVd/VJ4+vmd6lYRUZ68MH3fzySBcajtnXvK6mXjiuImaYTQ8uju3zVOy9gn0iV/z2TfYOsM0fxVLhl9/Fx+I1A4D1/bGrXZki2JsafXwk9Ba7FFt4uqqo5n/TkO4mzmtJ4k1SlMqOux/3SnihgzsXsB3E3pHg/ubadYH57Umg0lphflqx4K/vSOKUjghicBcHVH22+OM/PetBhB/lhFse707IbMGF6fDFQubwXvFmjLz8E5rarf4jdUsxk0bh16K4L7T4dggxCB5NlM1itkMP8efzUyNQn/I3/l/O26Nvg=="
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
    osascript scpt.scpt `python py.py ${bibcode}`
done

#clean up
cd - > /dev/null
rm -rf $tmpdir
