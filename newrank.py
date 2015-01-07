#! /usr/bin/python

import re
import string
import operator
import shutil
import xml.etree.ElementTree as ET
import namestoreplace
import sqlite3

shutil.copy ("/cygdrive/c/Users/dpalmer/Music/iTunes/iTunes Music Library.xml","/home/dpalmer/lib.xml")


# parse command line options (db write, db read, etc.)

# parse xml

tree = ET.parse('lib.xml')
root = tree.getroot()
#print root.tag

value=""
key=""
item={}
nextalbum=["","",""]
Cardinality={}
nextarray=[]

debug = 0
# add command line option for this
doVarious=0

def SetupDB(dbname):
    global con, curs

    con = sqlite3.connect(dbname)
    curs = con.cursor()
    curs.execute("""DROP TABLE IF EXISTS albums""")
    curs.execute("CREATE TABLE albums(artist TEXT, album TEXT, lastplay TEXT)")
    con.commit()


def CheckIfKey(node):
    if re.search(node.tag,"key"):
        return 1
    else:
        return 0

# given one of the three key-value pairs we are looking for,
# fill the list nextalbum with Artist, Album, Play Date
# then put it in the database

def FillLists(left,right):
    global albumcount, con, curs

    if re.search(left,"Artist"):
        nextalbum[0]=namestoreplace.ReplaceArtistStrings(right)
    elif re.search(left,"Album"):
         nextalbum[1]=namestoreplace.ReplaceAlbumStrings(right)
         if doVarious == 1:
             nextalbum[0]=namestoreplace.ReplaceVarious(nextalbum[0],nextalbum[1])
    elif re.search(left,"Play Date"):
        nextalbum[2]=right
	# here need to check if this album already exists in DB
        if debug ==1 :
            print "looking in db for ",nextalbum[0],nextalbum[1]
	curs.execute("SELECT artist, album FROM albums WHERE artist=? AND album=?",(nextalbum[0],nextalbum[1]))
	allrows=curs.fetchall()
        if debug ==1 :
            print "found: ",allrows

	# if so, ignore, else write it to db
	if len(allrows)==0:
            if debug ==1 :
                print "inserting: ",nextalbum[0], nextalbum[1],nextalbum[2]
                print nextalbum
            curs.execute("INSERT into albums VALUES(?,?,?)",(nextalbum[0], nextalbum[1], nextalbum[2]))
            con.commit()



## MAIN ##

# set up db

SetupDB("albums.db")

# songs in the itunes XML structure are several layers down
# loop through all XML tags, look for these three key-value pairs:
# <key>Artist</key><string>Madness</string>
# <key>Album</key><string>Total Madness</string>
# <key>Play Date</key><integer>3482746034</integer>

for child in root.findall("./dict/dict/dict/"):

    if CheckIfKey(child) == 1:
        FillLists(key,value)
        key = unicode(child.text)
    else:
        value = unicode(child.text)

# Now the database contains table albums with four columns
# albumindex artist album lastplay
# retrieve the list and sort by artist and lastplay
curs.execute("SELECT * FROM albums ORDER BY artist, lastplay")
AlbumsSortedByArtist = curs.fetchall()
NumberOfAlbums = len(AlbumsSortedByArtist)

# determine cardinality of each album, save in a dictionary
curs.execute("SELECT * FROM albums ORDER BY lastplay")
AlbumsSortedByLastplay = curs.fetchall()
i=0
for nextalbum in AlbumsSortedByLastplay:
   Cardinality[nextalbum[0]+nextalbum[1]]=i
   i+=1


# now go through the list of albums and calculate
# which albums to play next
lastartist=""
lastalbum=""
firstalbum=""
lastcard=0
countforartist=1

for nextalbum in AlbumsSortedByArtist:
    if debug == 1 :
        print nextalbum, Cardinality[nextalbum[0]+nextalbum[1]]
    if nextalbum[0] == lastartist:
        # same artist, compile statistics
        countforartist+=1
    else:
        # diff artist, flush and reset statistics
        average = int(NumberOfAlbums/countforartist)
        next = lastcard + average - NumberOfAlbums
        if countforartist == 1:
            next = next - 5
        if lastartist is not "":
            nextarray.append((lastartist,firstalbum,countforartist,lastcard,average,next))
        countforartist=1
        firstalbum=nextalbum[1]
    lastartist=nextalbum[0]
    lastcard = Cardinality[nextalbum[0]+nextalbum[1]]

# flush final album
average = int(NumberOfAlbums/countforartist)
next = lastcard + average - NumberOfAlbums
# boost singletons a little
if countforartist == 1:
    next = next - 5
nextarray.append((lastartist,firstalbum,countforartist,lastcard,average,next))

sortednext = sorted(nextarray, key=(operator.itemgetter(5)) )

con.close()

j=1
for i in sortednext:
    print j,i
    j=j+1    


# web interface to replace itunes play? view list, modify / mark as listened
