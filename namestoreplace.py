import re
import string

def ReplaceAlbumStrings(album):
    if re.search(u"Jesus Christ Superstar", album):
        album = string.replace(album,u"(CD1)","")
        album = string.replace(album,u"(CD2)","")
    if re.search(u"The Wall", album):
        album = string.replace(album,u"(CD1)","")
        album = string.replace(album,u"(CD2)","")
    if re.search(u"101", album):
        album = string.replace(album,u"(CD 1)","")
        album = string.replace(album,u"(CD 2)","")
    if re.search(u"Bring on the Night", album):
        album = string.replace(album,u"CD1","")
        album = string.replace(album,u"CD2","")
    if re.search(u"\xc4rzte", album):
        album = string.replace(album,u"\xc4rzte","Arzte")
    if re.search(u"\xdcbersee", album):
        album = string.replace(album,u"\xdcbersee","Ubersee")
    if re.search(u"\xa1", album):
        album = string.replace(album,u"\xa1","")
    return album

def ReplaceArtistStrings(artist):
    # combine certain solo artists with their bands
    if  re.search(u"Bryan Ferry", artist):
        artist = u"Bryan Ferry - Roxy Music"
    if  (re.search(u"Midge", artist) or re.search(u"Ultravox", artist)):
        artist = u"Midge Ure - Ultravox"
    if  (re.search(u"Annie Lennox", artist) or re.search(u"Eurythmics", artist)):
        artist = u"Annie Lennox - Eurythmics"
    if  (re.search(u"The Alarm", artist) or re.search(u"Mike Peters", artist)):
        artist = u"Alarm - Mike Peters"
    if  (re.search(u"Bob Mould", artist) or artist == u"Sugar" or artist == u"H\xfcsker D\xfc"):
        artist = u"Bob Mould - Sugar - Husker Du"
    if  (artist == u"Die \xc4rzte"):
        artist = u"Die Artzte"
#	 if  (re.search(u"Bunnymen", artist) or re.search(u"Ian McCulloch", artist)):
#			artist = "Echo and the Bunnymen - McCulloch"
    if  (re.search(u"Steve Taylor", artist) or re.search(u"Chagall", artist)):
        artist = u"Steve Taylor - Chagall"
    if  (re.search(u"Phil Collins", artist) or re.search(u"Genesis", artist)):
        artist = u"Phil Collins - Genesis"
    if  (re.search(u"The Smiths", artist) or re.search(u"Morrissey", artist)):
        artist = u"The Smiths - Morrissey"
    if  (re.search(u"Merchant", artist) or re.search(u"Maniacs", artist)):
        artist = u"10,000 Maniacs - Merchant"
    if  (re.search(u"Westerberg", artist) or re.search(u"Replacements", artist)):
        artist = u"Replacements - Westerburg"
    if  (re.search(u"Aimee Mann", artist) or re.search(u"Til Tuesday", artist)):
        artist = u"Aimee Mann - Til Tuesday"
    if  (re.search(u"Amanda Palmer", artist) or re.search(u"Dresden Dolls", artist)):
        artist = u"Dresden Dolls - Amanda Palmer"
    if  (artist == u"Juli" or re.search(u"Wir Sind", artist) or re.search(u"Herbert", artist)):
        artist = "Wir Sind Herbert Juli"
    if  (artist == "Brandon Flowers" or re.search(u"The Killers", artist)):
        artist = u"Killers Flowers"
    if  (artist == "Tracey Thorn" or re.search(u"Everything But", artist)):
        artist = u"Everything But The Girl- Tracey Thorn"
    if  re.search(u"Wynton Marsalis", artist):
        artist = u"Wynton Marsalis et al."
    if  (re.search(u"Addiction", artist) or re.search(u"Porno", artist)):
        artist = u"Jane's Addiction - Porno for Pyros"
    if  (re.search(u"Holst", artist) or re.search(u"LaBrass", artist)):
        artist = u"LaBrassBanda - Holst"

    return artist

def ReplaceVarious(artist, album):
    if (artist == u"Various"):
        return artist + " - " + album[0:9]
    else:
        return artist

