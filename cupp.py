#!/usr/bin/python
#
#  [Program]
#
#  CUPP 3.0
#  Common User Passwords Profiler
#
#
#
#  [Author]
#
#  Muris Kurgas aka j0rgan
#  j0rgan [at] remote-exploit [dot] org
#  http://www.remote-exploit.org
#  http://www.azuzi.me
#
#
#
#  [License]
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#  See 'docs/LICENSE' for more information.

import sys
import os
import ftplib
import ConfigParser
import urllib
import gzip
import csv


# Reading configuration file...
config = ConfigParser.ConfigParser()
config.read('cupp.cfg')

years = config.get('years', 'years').split(',')
chars = config.get('specialchars', 'chars').split(',')

numfrom = config.getint('nums','from')
numto = config.getint('nums','to')

wcfrom = config.getint('nums','wcfrom')
wcto = config.getint('nums','wcto')

threshold = config.getint('nums','threshold')

# 1337 mode configs, well you can add more lines if you add it to config file too.
# You will need to add more lines in two places in cupp.py code as well...
a = config.get('leet','a')
i = config.get('leet','i')
e = config.get('leet','e')
t = config.get('leet','t')
o = config.get('leet','o')
s = config.get('leet','s')
g = config.get('leet','g')
z = config.get('leet','z')


# for concatenations...

def concats(seq, start, stop):
    for mystr in seq:
        for num in xrange(start, stop):
            yield mystr + str(num)


# for sorting and making combinations...

def komb(seq, start):
    for mystr in seq:
        for mystr1 in start:
            yield mystr + mystr1

if len(sys.argv) < 2 or sys.argv[1] == '-h':
	print " ___________ "
	print " \033[07m  cupp.py! \033[27m                # Common"            
	print "      \                     # User"
	print "       \   \033[1;31m,__,\033[1;m             # Passwords" 
	print "        \  \033[1;31m(\033[1;moo\033[1;31m)____\033[1;m         # Profiler"
	print "           \033[1;31m(__)    )\ \033[1;m  "
	print "           \033[1;31m   ||--|| \033[1;m\033[05m*\033[25m\033[1;m      [ Muris Kurgas | j0rgan@remote-exploit.org ]\r\n\r\n"
	
	print "	[ Options ]\r\n"
	print "	-h	You are looking at it baby! :)"
	print " 		 For more help take a look in docs/README"
	print "		 Global configuration file is cupp.cfg\n"	

	print "	-i	Interactive questions for user password profiling\r\n"
	
	print "	-w	Use this option to improve existing dictionary,"
	print "		 or WyD.pl output to make some pwnsauce\r\n"
	
	print "	-l	Download huge wordlists from repository\r\n"
	print "	-a	Parse default usernames and passwords directly from Alecto DB."
	print "		 Project Alecto uses purified databases of Phenoelit and CIRT"
	print "		 which where merged and enhanced.\r\n"	
	print "	-v	Version of the program\r\n"
	exit()

elif sys.argv[1] == '-v':
	print "\r\n	\033[1;31m[ cupp.py ]  v3.0\033[1;m\r\n"
	print "	* Hacked up by j0rgan - j0rgan@remote-exploit.org"
	print "	* http://www.remote-exploit.org\r\n"
	print "	Take a look docs/README file for more info about the program\r\n"
	exit()


elif sys.argv[1] == '-w':
	if len(sys.argv) < 3:
		print "\r\n[Usage]:	"+sys.argv[0]+"  -w  [FILENAME]\r\n"
		exit()
	fajl = open(sys.argv[2], "r")
	listic = fajl.readlines()
	linije = 0
	for line in listic:
		linije += 1
		
	listica = []
	for x in listic:
		listica += x.split()
	
	print "\r\n      *************************************************"	
	print "      *                    \033[1;31mWARNING!!!\033[1;m                 *"
	print "      *         Using large wordlists in some         *"
	print "      *       options bellow is NOT recommended!      *"
	print "      *************************************************\r\n"
	
	conts = raw_input("> Do you want to concatenate all words from wordlist? Y/[N]: ").lower()
	
	
		
	if conts == "y" and linije > threshold:
		print "\r\n[-] Maximum number of words for concatenation is "+str(threshold)
		print "[-] Check configuration file for increasing this number.\r\n"
		conts = raw_input("> Do you want to concatenate all words from wordlist? Y/[N]: ").lower()
	conts = conts
	cont = ['']
	if conts == "y":
		for cont1 in listica:
			for cont2 in listica:
				if listica.index(cont1) != listica.index(cont2):
					cont.append(cont1+cont2)

	spechars = ['']
	spechars1 = raw_input("> Do you want to add special chars at the end of words? Y/[N]: ").lower()
	if spechars1 == "y":
		for spec1 in chars:
			spechars.append(spec1)
			for spec2 in chars:
				spechars.append(spec1+spec2)
				for spec3 in chars:
					spechars.append(spec1+spec2+spec3)
	
	randnum = raw_input("> Do you want to add some random numbers at the end of words? Y/[N]").lower()
	leetmode = raw_input("> Leet mode? (i.e. leet = 1337) Y/[N]: ").lower()

	
	kombinacija1 = list(komb(listica, years))
	kombinacija2 = ['']
	if conts == "y":
		kombinacija2 = list(komb(cont, years))
	kombinacija3 = ['']
	kombinacija4 = ['']
	if spechars1 == "y":
		kombinacija3 = list(komb(listica, spechars))
		if conts == "y":
			kombinacija4 = list(komb(cont, spechars))
	kombinacija5 = ['']
	kombinacija6 = ['']
	if randnum == "y":
		kombinacija5 = list(concats(listica, numfrom, numto))
		if conts == "y":
			kombinacija6 = list(concats(cont, numfrom, numto))
		
	print "\r\n[+] Now making a dictionary..."
	
	print "[+] Sorting list and removing duplicates..."
	
	komb_unique1 = dict.fromkeys(kombinacija1).keys()	
	komb_unique2 = dict.fromkeys(kombinacija2).keys()
	komb_unique3 = dict.fromkeys(kombinacija3).keys()
	komb_unique4 = dict.fromkeys(kombinacija4).keys()
	komb_unique5 = dict.fromkeys(kombinacija5).keys()
	komb_unique6 = dict.fromkeys(kombinacija6).keys()
	komb_unique7 = dict.fromkeys(listica).keys()
	komb_unique8 = dict.fromkeys(cont).keys()
	
	uniqlist = komb_unique1+komb_unique2+komb_unique3+komb_unique4+komb_unique5+komb_unique6+komb_unique7+komb_unique8
	
	unique_lista = dict.fromkeys(uniqlist).keys()
	unique_leet = []
	if leetmode == "y":
		for x in unique_lista: # if you want to add more leet chars, you will need to add more lines in cupp.cfg too...
			x = x.replace('a',a)
			x = x.replace('i',i)
			x = x.replace('e',e)
			x = x.replace('t',t)
			x = x.replace('o',o)
			x = x.replace('s',s)
			x = x.replace('g',g)
			x = x.replace('z',z)
			unique_leet.append(x)
	
	unique_list = unique_lista + unique_leet

	unique_list_finished = []
	for x in unique_list:
		if len(x) > wcfrom and len(x) < wcto:
			unique_list_finished.append(x)

	f = open ( sys.argv[2]+'.cupp.txt', 'w' )
	unique_list_finished.sort()
	f.write (os.linesep.join(unique_list_finished))
	f = open ( sys.argv[2]+'.cupp.txt', 'r' )
	lines = 0
	for line in f:
		lines += 1
	f.close()
	
	
	print "[+] Saving dictionary to \033[1;31m"+sys.argv[2]+".cupp.txt\033[1;m, counting \033[1;31m"+str(lines)+" words.\033[1;m"
	print "[+] Now load your pistolero with \033[1;31m"+sys.argv[2]+".cupp.txt\033[1;m and shoot! Good luck!"
	fajl.close()
	exit()



elif sys.argv[1] == '-i':
	print "\r\n[+] Insert the informations about the victim to make a dictionary"
	print "[+] If you don't know all the info, just hit enter when asked! ;)\r\n"

# We need some informations first!

	name = raw_input("> First Name: ").lower()
	while len(name) == 0 or name == " " or name == "  " or name == "   ":
		print "\r\n[-] You must enter a name at least!"
		name = raw_input("> Name: ").lower()
	name = str(name)

	surname = raw_input("> Surname: ").lower()
	nick = raw_input("> Nickname: ").lower()
	birthdate = raw_input("> Birthdate (DDMMYYYY): ")
	while len(birthdate) != 0 and len(birthdate) != 8:
		print "\r\n[-] You must enter 8 digits for birthday!"
		birthdate = raw_input("> Birthdate (DDMMYYYY): ")
	birthdate = str(birthdate)

	print "\r\n"

	wife = raw_input("> Partners) name: ").lower()
	wifen = raw_input("> Partners) nickname: ").lower()
	wifeb = raw_input("> Partners) birthdate (DDMMYYYY): ")
	while len(wifeb) != 0 and len(wifeb) != 8:
		print "\r\n[-] You must enter 8 digits for birthday!"
		wifeb = raw_input("> Partners birthdate (DDMMYYYY): ")
	wifeb = str(wifeb)
	print "\r\n"

	kid = raw_input("> Child's name: ").lower()
	kidn = raw_input("> Child's nickname: ").lower()
	kidb = raw_input("> Child's birthdate (DDMMYYYY): ")
	while len(kidb) != 0 and len(kidb) != 8:
		print "\r\n[-] You must enter 8 digits for birthday!"
		kidb = raw_input("> Child's birthdate (DDMMYYYY): ")
	kidb = str(kidb)
	print "\r\n"

	pet = raw_input("> Pet's name: ").lower()
	company = raw_input("> Company name: ").lower()
	print "\r\n"

	words = ['']
	words1 = raw_input("> Do you want to add some key words about the victim? Y/[N]: ").lower()
	words2 = ""
	if words1 == "y":
		words2 = raw_input("> Please enter the words, separated by comma. [i.e. hacker,juice,black], spaces will be removed: ").replace(" ","")
	words = words2.split(",")

	spechars = ['']
	spechars1 = raw_input("> Do you want to add special chars at the end of words? Y/[N]: ").lower()
	if spechars1 == "y":
		for spec1 in chars:
			spechars.append(spec1)
			for spec2 in chars:
				spechars.append(spec1+spec2)
				for spec3 in chars:
					spechars.append(spec1+spec2+spec3)

	randnum = raw_input("> Do you want to add some random numbers at the end of words? Y/[N]").lower()
	leetmode = raw_input("> Leet mode? (i.e. leet = 1337) Y/[N]: ").lower()


	print "\r\n[+] Now making a dictionary..."


# Now me must do some string modifications...

# Birthdays first

	birthdate_yy = birthdate[-2:]
	birthdate_yyy = birthdate[-3:]
	birthdate_yyyy = birthdate[-4:]
	birthdate_xd = birthdate[1:2]
	birthdate_xm = birthdate[3:4]
	birthdate_dd = birthdate[:2]
	birthdate_mm = birthdate[2:4]

	wifeb_yy = wifeb[-2:]
	wifeb_yyy = wifeb[-3:]
	wifeb_yyyy = wifeb[-4:]
	wifeb_xd = wifeb[1:2]
	wifeb_xm = wifeb[3:4]
	wifeb_dd = wifeb[:2]
	wifeb_mm = wifeb[2:4]

	kidb_yy = kidb[-2:]
	kidb_yyy = kidb[-3:]
	kidb_yyyy = kidb[-4:]
	kidb_xd = kidb[1:2]
	kidb_xm = kidb[3:4]
	kidb_dd = kidb[:2]
	kidb_mm = kidb[2:4]
	
	
	# Convert first letters to uppercase...
	
	nameup = name.title()
	surnameup = surname.title()
	nickup = nick.title()
	wifeup = wife.title()
	wifenup = wifen.title()
	kidup = kid.title()
	kidnup = kidn.title()
	petup = pet.title()
	companyup = company.title()
	wordsup = []
	for words1 in words:
		wordsup.append(words1.title())
	
	word = words+wordsup
	
	# reverse a name
	
	rev_name = name[::-1]
	rev_nameup = nameup[::-1]
	rev_nick = nick[::-1]
	rev_nickup = nickup[::-1]
	rev_wife = wife[::-1]
	rev_wifeup = wifeup[::-1]
	rev_kid = kid[::-1]
	rev_kidup = kidup[::-1]
	
	reverse = [rev_name, rev_nameup, rev_nick, rev_nickup, rev_wife, rev_wifeup, rev_kid, rev_kidup]
	rev_n = [rev_name, rev_nameup, rev_nick, rev_nickup]
	rev_w = [rev_wife, rev_wifeup]
	rev_k = [rev_kid, rev_kidup]
	# Let's do some serious work! This will be a mess of code, but... who cares? :)
	
	# Birthdays combinations
	
	bds = [birthdate_yy, birthdate_yyy, birthdate_yyyy, birthdate_xd, birthdate_xm, birthdate_dd, birthdate_mm]
	
	bdss = []
	
	for bds1 in bds:
		bdss.append(bds1)
		for bds2 in bds:
			if bds.index(bds1) != bds.index(bds2):
				bdss.append(bds1+bds2)
				for bds3 in bds:
					if bds.index(bds1) != bds.index(bds2) and bds.index(bds2) != bds.index(bds3) and bds.index(bds1) != bds.index(bds3):
						bdss.append(bds1+bds2+bds3)
	
	
	
	# For a woman...
	wbds = [wifeb_yy, wifeb_yyy, wifeb_yyyy, wifeb_xd, wifeb_xm, wifeb_dd, wifeb_mm]
	
	wbdss = []
	
	for wbds1 in wbds:
		wbdss.append(wbds1)
		for wbds2 in wbds:
			if wbds.index(wbds1) != wbds.index(wbds2):
				wbdss.append(wbds1+wbds2)
				for wbds3 in wbds:
					if wbds.index(wbds1) != wbds.index(wbds2) and wbds.index(wbds2) != wbds.index(wbds3) and wbds.index(wbds1) != wbds.index(wbds3):
						wbdss.append(wbds1+wbds2+wbds3)
	
	
	
	# and a child...
	kbds = [kidb_yy, kidb_yyy, kidb_yyyy, kidb_xd, kidb_xm, kidb_dd, kidb_mm]
	
	kbdss = []
	
	for kbds1 in kbds:
		kbdss.append(kbds1)
		for kbds2 in kbds:
			if kbds.index(kbds1) != kbds.index(kbds2):
				kbdss.append(kbds1+kbds2)
				for kbds3 in kbds:
					if kbds.index(kbds1) != kbds.index(kbds2) and kbds.index(kbds2) != kbds.index(kbds3) and kbds.index(kbds1) != kbds.index(kbds3):
						kbdss.append(kbds1+kbds2+kbds3)
	
	# string combinations....
	
	kombinaac = [pet, petup, company, companyup]
	
	kombina = [name, surname, nick, nameup, surnameup, nickup]
	
	kombinaw = [wife, wifen, wifeup, wifenup, surname, surnameup]
	
	kombinak = [kid, kidn, kidup, kidnup, surname, surnameup]
	
	kombinaa = []
	for kombina1 in kombina:
		kombinaa.append(kombina1)
		for kombina2 in kombina:
			if kombina.index(kombina1) != kombina.index(kombina2) and kombina.index(kombina1.title()) != kombina.index(kombina2.title()):
				kombinaa.append(kombina1+kombina2)
	
	kombinaaw = []
	for kombina1 in kombinaw:
		kombinaaw.append(kombina1)
		for kombina2 in kombinaw:
			if kombinaw.index(kombina1) != kombinaw.index(kombina2) and kombinaw.index(kombina1.title()) != kombinaw.index(kombina2.title()):
				kombinaaw.append(kombina1+kombina2)
	
	kombinaak = []
	for kombina1 in kombinak:
		kombinaak.append(kombina1)
		for kombina2 in kombinak:
			if kombinak.index(kombina1) != kombinak.index(kombina2) and kombinak.index(kombina1.title()) != kombinak.index(kombina2.title()):
				kombinaak.append(kombina1+kombina2)
	
	
	
	komb1 = list(komb(kombinaa, bdss))
	komb2 = list(komb(kombinaaw, wbdss))
	komb3 = list(komb(kombinaak, kbdss))
	komb4 = list(komb(kombinaa, years))
	komb5 = list(komb(kombinaac, years))
	komb6 = list(komb(kombinaaw, years))
	komb7 = list(komb(kombinaak, years))
	komb8 = list(komb(word, bdss))
	komb9 = list(komb(word, wbdss))
	komb10 = list(komb(word, kbdss))
	komb11 = list(komb(word, years))
	komb12 = ['']
	komb13 = ['']
	komb14 = ['']
	komb15 = ['']
	komb16 = ['']
	komb21 = ['']
	if randnum == "y":
		komb12 = list(concats(word, numfrom, numto))
		komb13 = list(concats(kombinaa, numfrom, numto))
		komb14 = list(concats(kombinaac, numfrom, numto))
		komb15 = list(concats(kombinaaw, numfrom, numto))
		komb16 = list(concats(kombinaak, numfrom, numto))
		komb21 = list(concats(reverse, numfrom, numto))
	komb17 = list(komb(reverse, years))
	komb18 = list(komb(rev_w, wbdss))
	komb19 = list(komb(rev_k, kbdss))
	komb20 = list(komb(rev_n, bdss))
	komb001 = ['']
	komb002 = ['']
	komb003 = ['']
	komb004 = ['']
	komb005 = ['']
	komb006 = ['']
	if spechars1 == "y":
		komb001 = list(komb(kombinaa, spechars))
		komb002 = list(komb(kombinaac, spechars))
		komb003 = list(komb(kombinaaw , spechars))
		komb004 = list(komb(kombinaak , spechars))
		komb005 = list(komb(word, spechars))
		komb006 = list(komb(reverse, spechars))
	
	print "[+] Sorting list and removing duplicates..."
	
	komb_unique1 = dict.fromkeys(komb1).keys()
	komb_unique2 = dict.fromkeys(komb2).keys()
	komb_unique3 = dict.fromkeys(komb3).keys()
	komb_unique4 = dict.fromkeys(komb4).keys()
	komb_unique5 = dict.fromkeys(komb5).keys()
	komb_unique6 = dict.fromkeys(komb6).keys()
	komb_unique7 = dict.fromkeys(komb7).keys()
	komb_unique8 = dict.fromkeys(komb8).keys()
	komb_unique9 = dict.fromkeys(komb9).keys()
	komb_unique10 = dict.fromkeys(komb10).keys()
	komb_unique11 = dict.fromkeys(komb11).keys()
	komb_unique12 = dict.fromkeys(komb12).keys()
	komb_unique13 = dict.fromkeys(komb13).keys()
	komb_unique14 = dict.fromkeys(komb14).keys()
	komb_unique15 = dict.fromkeys(komb15).keys()
	komb_unique16 = dict.fromkeys(komb16).keys()
	komb_unique17 = dict.fromkeys(komb17).keys()
	komb_unique18 = dict.fromkeys(komb18).keys()
	komb_unique19 = dict.fromkeys(komb19).keys()
	komb_unique20 = dict.fromkeys(komb20).keys()
	komb_unique21 = dict.fromkeys(komb21).keys()
	komb_unique01 = dict.fromkeys(kombinaa).keys()
	komb_unique02 = dict.fromkeys(kombinaac).keys()
	komb_unique03 = dict.fromkeys(kombinaaw).keys()
	komb_unique04 = dict.fromkeys(kombinaak).keys()
	komb_unique05 = dict.fromkeys(word).keys()
	komb_unique07 = dict.fromkeys(komb001).keys()
	komb_unique08 = dict.fromkeys(komb002).keys()
	komb_unique09 = dict.fromkeys(komb003).keys()
	komb_unique010 = dict.fromkeys(komb004).keys()
	komb_unique011 = dict.fromkeys(komb005).keys()
	komb_unique012 = dict.fromkeys(komb006).keys()
	
	uniqlist = bdss+wbdss+kbdss+reverse+komb_unique01+komb_unique02+komb_unique03+komb_unique04+komb_unique05+komb_unique1+komb_unique2+komb_unique3+komb_unique4+komb_unique5+komb_unique6+komb_unique7+komb_unique8+komb_unique9+komb_unique10+komb_unique11+komb_unique12+komb_unique13+komb_unique14+komb_unique15+komb_unique16+komb_unique17+komb_unique18+komb_unique19+komb_unique20+komb_unique21+komb_unique07+komb_unique08+komb_unique09+komb_unique010+komb_unique011+komb_unique012
	
	unique_lista = dict.fromkeys(uniqlist).keys()
	unique_leet = []
	if leetmode == "y":
		for x in unique_lista: # if you want to add more leet chars, you will need to add more lines in cupp.cfg too...
			x = x.replace('a',a)
			x = x.replace('i',i)
			x = x.replace('e',e)
			x = x.replace('t',t)
			x = x.replace('o',o)
			x = x.replace('s',s)
			x = x.replace('g',g)
			x = x.replace('z',z)
			unique_leet.append(x)
	
	unique_list = unique_lista + unique_leet
	
	unique_list_finished = []
	for x in unique_list:
		if len(x) > wcfrom and len(x) < wcto:
			unique_list_finished.append(x)

	unique_list_finished.sort()
	f = open ( name+'.txt', 'w' )
	f.write (os.linesep.join(unique_list_finished))
	f = open ( name+'.txt', 'r' )
	lines = 0
	for line in f:
		lines += 1
	f.close()
	
	print "[+] Saving dictionary to \033[1;31m"+name+".txt\033[1;m, counting \033[1;31m"+str(lines)+"\033[1;m words."
	print "[+] Now load your pistolero with \033[1;31m"+name+".txt\033[1;m and shoot! Good luck!"
	exit()

	
	
elif sys.argv[1] == '-a':
	url = config.get('alecto','alectourl')
	
	print "\r\n[+] Checking if alectodb is not present..."
	if os.path.isfile('alectodb.csv.gz') == 0:
		print "[+] Downloading alectodb.csv.gz..."
		webFile = urllib.urlopen(url)
		localFile = open(url.split('/')[-1], 'w')
		localFile.write(webFile.read())
		webFile.close()
		localFile.close()
	
	
	f = gzip.open('alectodb.csv.gz', 'rb')
	
	data = csv.reader(f)
	
	usernames = []
	passwords = []
	for row in data:
		usernames.append(row[5])
		passwords.append(row[6])
	gus = list(set(usernames))
	gpa = list(set(passwords))
	gus.sort()
	gpa.sort()
	
	print "\r\n[+] Exporting to alectodb-usernames.txt and alectodb-passwords.txt\r\n[+] Done."
	f = open ( 'alectodb-usernames.txt', 'w' )
	f.write (os.linesep.join(gus))
	f.close()
		
	f = open ( 'alectodb-passwords.txt', 'w' )
	f.write (os.linesep.join(gpa))
	f.close()
	
	
	f.close()
	sys.exit()



elif sys.argv[1] == '-l':
	
	ftpname = config.get('downloader','ftpname')
	ftpurl = config.get('downloader','ftpurl')
	ftppath = config.get('downloader','ftppath')
	ftpuser = config.get('downloader','ftpuser')
	ftppass = config.get('downloader','ftppass')
	
	
	if os.path.isdir('dictionaries') == 0:
		os.mkdir('dictionaries')
	
	print "	\r\n	Choose the section you want to download:\r\n"
	
	print "     1   Moby            14      french          27      places"
	print "     2   afrikaans       15      german          28      polish"
	print "     3   american        16      hindi           39      random"
	print "     4   aussie          17      hungarian       30      religion"
	print "     5   chinese         18      italian         31      russian"
	print "     6   computer        19      japanese        32      science"
	print "     7   croatian        20      latin           33      spanish"
	print "     8   czech           21      literature      34      swahili"
	print "     9   danish          22      movieTV         35      swedish"
	print "    10   databases       23      music           36      turkish"
	print "    11   dictionaries    24      names           37      yiddish"
	print "    12   dutch           25      net             38      exit program"
	print "    13   finnish         26      norwegian       \r\n"
	print "	\r\n	Files will be downloaded from "+ftpname+" repository"
	print "	\r\n	Tip: After downloading wordlist, you can improve it with -w option\r\n"
	
	filedown = raw_input("> Enter number: ")
	filedown.isdigit()
	while filedown.isdigit() == 0:
		print "\r\n[-] Wrong choice. "
		filedown = raw_input("> Enter number: ")
	filedown = str(filedown)
	while int(filedown) > 38:
		print "\r\n[-] Wrong choice. "
		filedown = raw_input("> Enter number: ")
	filedown = str(filedown)
	
	
	def handleDownload(block):
		file.write(block)
		print ".",
	
	def downloader():
		ftp.login(ftpuser, ftppass)
		ftp.cwd(ftppath)
	
	def filequitter():
		file.close()
		print ' done.'
	
	
	if filedown == "1":
		print "\r\n[+] connecting...\r\n"
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('Moby')
		if os.path.isdir('dictionaries/Moby/') == 0:
			os.mkdir('dictionaries/Moby/')
		dire = 'dictionaries/Moby/'
		file = open(dire+'mhyph.tar.gz', 'wb')
		print "\r\n[+] downloading mhyph.tar.gz..."
		ftp.retrbinary('RETR ' + 'mhyph.tar.gz', handleDownload)
		filequitter()
		
		file = open(dire+'mlang.tar.gz', 'wb')
		print "\r\n[+] downloading mlang.tar.gz..."
		ftp.retrbinary('RETR ' + 'mlang.tar.gz', handleDownload)
		filequitter()
		
		file = open(dire+'moby.tar.gz', 'wb')
		print "\r\n[+] downloading moby.tar.gz..."
		ftp.retrbinary('RETR ' + 'moby.tar.gz', handleDownload)
		filequitter()
		
		file = open(dire+'mpos.tar.gz', 'wb')
		print "\r\n[+] downloading mpos.tar.gz..."
		ftp.retrbinary('RETR ' + 'mpos.tar.gz', handleDownload)
		filequitter()
		
		file = open(dire+'mpron.tar.gz', 'wb')
		print "\r\n[+] downloading mpron.tar.gz..."
		ftp.retrbinary('RETR ' + 'mpron.tar.gz', handleDownload)
		filequitter()
		
		file = open(dire+'mthes.tar.gz', 'wb')
		print "\r\n[+] downloading mthes.tar.gz..."
		ftp.retrbinary('RETR ' + 'mthes.tar.gz', handleDownload)
		filequitter()
		
		file = open(dire+'mwords.tar.gz', 'wb')
		print "\r\n[+] downloading mwords.tar.gz..."
		ftp.retrbinary('RETR ' + 'mwords.tar.gz', handleDownload)
		filequitter()
	
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "2":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('afrikaans')
		if os.path.isdir('dictionaries/afrikaans/') == 0:
			os.mkdir('dictionaries/afrikaans/')
		dire = 'dictionaries/afrikaans/'
		
		file = open(dire+'afr_dbf.zip', 'wb')
		print "\r\n[+] downloading afr_dbf.zip..."
		ftp.retrbinary('RETR ' + 'afr_dbf.zip', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
		
	if filedown == "3":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('american')
		if os.path.isdir('dictionaries/american/') == 0:
			os.mkdir('dictionaries/american/')
		dire = 'dictionaries/american/'
		
		file = open(dire+'dic-0294.tar.gz', 'wb')
		print "\r\n[+] downloading dic-0294.tar.gz..."
		ftp.retrbinary('RETR ' + 'dic-0294.tar.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "4":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('aussie')
		if os.path.isdir('dictionaries/aussie/') == 0:
			os.mkdir('dictionaries/aussie/')
		dire = 'dictionaries/aussie/'
		
		file = open(dire+'oz.gz', 'wb')
		print "\r\n[+] downloading oz.gz..."
		ftp.retrbinary('RETR ' + 'oz.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
		
		
	if filedown == "5":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('chinese')
		if os.path.isdir('dictionaries/chinese/') == 0:
			os.mkdir('dictionaries/chinese/')
		dire = 'dictionaries/chinese/'
		
		file = open(dire+'chinese.gz', 'wb')
		print "\r\n[+] downloading chinese.gz..."
		ftp.retrbinary('RETR ' + 'chinese.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "6":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('computer')
		if os.path.isdir('dictionaries/computer/') == 0:
			os.mkdir('dictionaries/computer/')
		dire = 'dictionaries/computer/'
		
		file = open(dire+'Domains.gz', 'wb')
		print "\r\n[+] downloading Domains.gz..."
		ftp.retrbinary('RETR ' + 'Domains.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Dosref.gz', 'wb')
		print "\r\n[+] downloading Dosref.gz..."
		ftp.retrbinary('RETR ' + 'Dosref.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Ftpsites.gz', 'wb')
		print "\r\n[+] downloading Ftpsites.gz..."
		ftp.retrbinary('RETR ' + 'Ftpsites.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Jargon.gz', 'wb')
		print "\r\n[+] downloading Jargon.gz..."
		ftp.retrbinary('RETR ' + 'Jargon.gz', handleDownload)
		filequitter()
			
		file = open(dire+'common-passwords.txt.gz', 'wb')
		print "\r\n[+] downloading common-passwords.txt.gz..."
		ftp.retrbinary('RETR ' + 'common-passwords.txt.gz', handleDownload)
		filequitter()
			
		file = open(dire+'etc-hosts.gz', 'wb')
		print "\r\n[+] downloading etc-hosts.gz..."
		ftp.retrbinary('RETR ' + 'etc-hosts.gz', handleDownload)
		filequitter()
			
		file = open(dire+'foldoc.gz', 'wb')
		print "\r\n[+] downloading foldoc.gz..."
		ftp.retrbinary('RETR ' + 'foldoc.gz', handleDownload)
		filequitter()
			
		file = open(dire+'language-list.gz', 'wb')
		print "\r\n[+] downloading language-list.gz..."
		ftp.retrbinary('RETR ' + 'language-list.gz', handleDownload)
		filequitter()
			
		file = open(dire+'unix.gz', 'wb')
		print "\r\n[+] downloading unix.gz..."
		ftp.retrbinary('RETR ' + 'unix.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "7":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('croatian')
		if os.path.isdir('dictionaries/croatian/') == 0:
			os.mkdir('dictionaries/croatian/')
		dire = 'dictionaries/croatian/'
		
		file = open(dire+'croatian.gz', 'wb')
		print "\r\n[+] downloading croatian.gz..."
		ftp.retrbinary('RETR ' + 'croatian.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
		
	if filedown == "8":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('czech')
		if os.path.isdir('dictionaries/czech/') == 0:
			os.mkdir('dictionaries/czech/')
		dire = 'dictionaries/czech/'
		
		file = open(dire+'czech-wordlist-ascii-cstug-novak.gz', 'wb')
		print "\r\n[+] downloading czech-wordlist-ascii-cstug-novak.gz..."
		ftp.retrbinary('RETR ' + 'czech-wordlist-ascii-cstug-novak.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	
	if filedown == "9":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('danish')
		if os.path.isdir('dictionaries/danish/') == 0:
			os.mkdir('dictionaries/danish/')
		dire = 'dictionaries/danish/'
		
		file = open(dire+'danish.words.gz', 'wb')
		print "\r\n[+] downloading danish.words.gz..."
		ftp.retrbinary('RETR ' + 'danish.words.gz', handleDownload)
		filequitter()
			
		file = open(dire+'dansk.zip', 'wb')
		print "\r\n[+] downloading dansk.zip..."
		ftp.retrbinary('RETR ' + 'dansk.zip', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "10":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('databases')
		if os.path.isdir('dictionaries/databases/') == 0:
			os.mkdir('dictionaries/databases/')
		dire = 'dictionaries/databases/'
		
		file = open(dire+'acronyms.gz', 'wb')
		print "\r\n[+] downloading acronyms.gz..."
		ftp.retrbinary('RETR ' + 'acronyms.gz', handleDownload)
		filequitter()
			
		file = open(dire+'att800.gz', 'wb')
		print "\r\n[+] downloading att800.gz..."
		ftp.retrbinary('RETR ' + 'att800.gz', handleDownload)
		filequitter()
			
		file = open(dire+'computer-companies.gz', 'wb')
		print "\r\n[+] downloading computer-companies.gz..."
		ftp.retrbinary('RETR ' + 'computer-companies.gz', handleDownload)
		filequitter()
			
		file = open(dire+'world_heritage.gz', 'wb')
		print "\r\n[+] downloading world_heritage.gz..."
		ftp.retrbinary('RETR ' + 'world_heritage.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "11":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('dictionaries')
		if os.path.isdir('dictionaries/dictionaries/') == 0:
			os.mkdir('dictionaries/dictionaries/')
		dire = 'dictionaries/dictionaries/'
		
		file = open(dire+'Antworth.gz', 'wb')
		print "\r\n[+] downloading Antworth.gz..."
		ftp.retrbinary('RETR ' + 'Antworth.gz', handleDownload)
		filequitter()
			
		file = open(dire+'CRL.words.gz', 'wb')
		print "\r\n[+] downloading CRL.words.gz..."
		ftp.retrbinary('RETR ' + 'CRL.words.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Roget.words.gz', 'wb')
		print "\r\n[+] downloading Roget.words.gz..."
		ftp.retrbinary('RETR ' + 'Roget.words.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Unabr.dict.gz', 'wb')
		print "\r\n[+] downloading Unabr.dict.gz..."
		ftp.retrbinary('RETR ' + 'Unabr.dict.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Unix.dict.gz', 'wb')
		print "\r\n[+] downloading Unix.dict.gz..."
		ftp.retrbinary('RETR ' + 'Unix.dict.gz', handleDownload)
		filequitter()
			
		file = open(dire+'englex-dict.gz', 'wb')
		print "\r\n[+] downloading englex-dict.gz..."
		ftp.retrbinary('RETR ' + 'englex-dict.gz', handleDownload)
		filequitter()
			
		file = open(dire+'knuth_britsh.gz', 'wb')
		print "\r\n[+] downloading knuth_britsh.gz..."
		ftp.retrbinary('RETR ' + 'knuth_britsh.gz', handleDownload)
		filequitter()
			
		file = open(dire+'knuth_words.gz', 'wb')
		print "\r\n[+] downloading knuth_words.gz..."
		ftp.retrbinary('RETR ' + 'knuth_words.gz', handleDownload)
		filequitter()
			
		file = open(dire+'pocket-dic.gz', 'wb')
		print "\r\n[+] downloading pocket-dic.gz..."
		ftp.retrbinary('RETR ' + 'pocket-dic.gz', handleDownload)
		filequitter()
			
		file = open(dire+'shakesp-glossary.gz', 'wb')
		print "\r\n[+] downloading shakesp-glossary.gz..."
		ftp.retrbinary('RETR ' + 'shakesp-glossary.gz', handleDownload)
		filequitter()
			
		file = open(dire+'special.eng.gz', 'wb')
		print "\r\n[+] downloading special.eng.gz..."
		ftp.retrbinary('RETR ' + 'special.eng.gz', handleDownload)
		filequitter()
			
		file = open(dire+'words-english.gz', 'wb')
		print "\r\n[+] downloading words-english.gz..."
		ftp.retrbinary('RETR ' + 'words-english.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "12":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('dutch')
		if os.path.isdir('dictionaries/dutch/') == 0:
			os.mkdir('dictionaries/dutch/')
		dire = 'dictionaries/dutch/'
		
		file = open(dire+'words.dutch.gz', 'wb')
		print "\r\n[+] downloading words.dutch.gz..."
		ftp.retrbinary('RETR ' + 'words.dutch.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "13":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('finnish')
		if os.path.isdir('dictionaries/finnish/') == 0:
			os.mkdir('dictionaries/finnish/')
		dire = 'dictionaries/finnish/'
		
		file = open(dire+'finnish.gz', 'wb')
		print "\r\n[+] downloading finnish.gz..."
		ftp.retrbinary('RETR ' + 'finnish.gz', handleDownload)
		filequitter()
			
		file = open(dire+'firstnames.finnish.gz', 'wb')
		print "\r\n[+] downloading firstnames.finnish.gz..."
		ftp.retrbinary('RETR ' + 'firstnames.finnish.gz', handleDownload)
		filequitter()
			
		file = open(dire+'words.finnish.FAQ.gz', 'wb')
		print "\r\n[+] downloading words.finnish.FAQ.gz..."
		ftp.retrbinary('RETR ' + 'words.finnish.FAQ.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "14":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('french')
		if os.path.isdir('dictionaries/french/') == 0:
			os.mkdir('dictionaries/french/')
		dire = 'dictionaries/french/'
		
		file = open(dire+'dico.gz', 'wb')
		print "\r\n[+] downloading dico.gz..."
		ftp.retrbinary('RETR ' + 'dico.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "15":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('german')
		if os.path.isdir('dictionaries/german/') == 0:
			os.mkdir('dictionaries/german/')
		dire = 'dictionaries/german/'
		
		file = open(dire+'deutsch.dic.gz', 'wb')
		print "\r\n[+] downloading deutsch.dic.gz..."
		ftp.retrbinary('RETR ' + 'deutsch.dic.gz', handleDownload)
		filequitter()
			
		file = open(dire+'germanl.gz', 'wb')
		print "\r\n[+] downloading germanl.gz..."
		ftp.retrbinary('RETR ' + 'germanl.gz', handleDownload)
		filequitter()
			
		file = open(dire+'words.german.gz', 'wb')
		print "\r\n[+] downloading words.german.gz..."
		ftp.retrbinary('RETR ' + 'words.german.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "16":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('hindi')
		if os.path.isdir('dictionaries/hindi/') == 0:
			os.mkdir('dictionaries/hindi/')
		dire = 'dictionaries/hindi/'
		
		file = open(dire+'hindu-names.gz', 'wb')
		print "\r\n[+] downloading hindu-names.gz..."
		ftp.retrbinary('RETR ' + 'hindu-names.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "17":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('hungarian')
		if os.path.isdir('dictionaries/hungarian/') == 0:
			os.mkdir('dictionaries/hungarian/')
		dire = 'dictionaries/hungarian/'
		
		file = open(dire+'hungarian.gz', 'wb')
		print "\r\n[+] downloading hungarian.gz..."
		ftp.retrbinary('RETR ' + 'hungarian.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "18":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('italian')
		if os.path.isdir('dictionaries/italian/') == 0:
			os.mkdir('dictionaries/italian/')
		dire = 'dictionaries/italian/'
		
		file = open(dire+'words.italian.gz', 'wb')
		print "\r\n[+] downloading words.italian.gz..."
		ftp.retrbinary('RETR ' + 'words.italian.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "19":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('japanese')
		if os.path.isdir('dictionaries/japanese/') == 0:
			os.mkdir('dictionaries/japanese/')
		dire = 'dictionaries/japanese/'
		
		file = open(dire+'words.japanese.gz', 'wb')
		print "\r\n[+] downloading words.japanese.gz..."
		ftp.retrbinary('RETR ' + 'words.japanese.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "20":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('latin')
		if os.path.isdir('dictionaries/latin/') == 0:
			os.mkdir('dictionaries/latin/')
		dire = 'dictionaries/latin/'
		
		file = open(dire+'wordlist.aug.gz', 'wb')
		print "\r\n[+] downloading wordlist.aug.gz..."
		ftp.retrbinary('RETR ' + 'wordlist.aug.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "21":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('literature')
		if os.path.isdir('dictionaries/literature/') == 0:
			os.mkdir('dictionaries/literature/')
		dire = 'dictionaries/literature/'
		
		file = open(dire+'LCarrol.gz', 'wb')
		print "\r\n[+] downloading LCarrol.gz..."
		ftp.retrbinary('RETR ' + 'LCarrol.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Paradise.Lost.gz', 'wb')
		print "\r\n[+] downloading Paradise.Lost.gz..."
		ftp.retrbinary('RETR ' + 'Paradise.Lost.gz', handleDownload)
		filequitter()
			
		file = open(dire+'aeneid.gz', 'wb')
		print "\r\n[+] downloading aeneid.gz..."
		ftp.retrbinary('RETR ' + 'aeneid.gz', handleDownload)
		filequitter()
			
		file = open(dire+'arthur.gz', 'wb')
		print "\r\n[+] downloading arthur.gz..."
		ftp.retrbinary('RETR ' + 'arthur.gz', handleDownload)
		filequitter()
			
		file = open(dire+'cartoon.gz', 'wb')
		print "\r\n[+] downloading cartoon.gz..."
		ftp.retrbinary('RETR ' + 'cartoon.gz', handleDownload)
		filequitter()
			
		file = open(dire+'cartoons-olivier.gz', 'wb')
		print "\r\n[+] downloading cartoons-olivier.gz..."
		ftp.retrbinary('RETR ' + 'cartoons-olivier.gz', handleDownload)
		filequitter()
			
		file = open(dire+'charlemagne.gz', 'wb')
		print "\r\n[+] downloading charlemagne.gz..."
		ftp.retrbinary('RETR ' + 'charlemagne.gz', handleDownload)
		filequitter()
			
		file = open(dire+'fable.gz', 'wb')
		print "\r\n[+] downloading fable.gz..."
		ftp.retrbinary('RETR ' + 'fable.gz', handleDownload)
		filequitter()
			
		file = open(dire+'iliad.gz', 'wb')
		print "\r\n[+] downloading iliad.gz..."
		ftp.retrbinary('RETR ' + 'iliad.gz', handleDownload)
		filequitter()
			
		file = open(dire+'myths-legends.gz', 'wb')
		print "\r\n[+] downloading myths-legends.gz..."
		ftp.retrbinary('RETR ' + 'myths-legends.gz', handleDownload)
		filequitter()
			
		file = open(dire+'odyssey.gz', 'wb')
		print "\r\n[+] downloading odyssey.gz..."
		ftp.retrbinary('RETR ' + 'odyssey.gz', handleDownload)
		filequitter()
			
		file = open(dire+'sf.gz', 'wb')
		print "\r\n[+] downloading sf.gz..."
		ftp.retrbinary('RETR ' + 'sf.gz', handleDownload)
		filequitter()
			
		file = open(dire+'shakespeare.gz', 'wb')
		print "\r\n[+] downloading shakespeare.gz..."
		ftp.retrbinary('RETR ' + 'shakespeare.gz', handleDownload)
		filequitter()
			
		file = open(dire+'tolkien.words.gz', 'wb')
		print "\r\n[+] downloading tolkien.words.gz..."
		ftp.retrbinary('RETR ' + 'tolkien.words.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "22":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('movieTV')
		if os.path.isdir('dictionaries/movieTV/') == 0:
			os.mkdir('dictionaries/movieTV/')
		dire = 'dictionaries/movieTV/'
		
		file = open(dire+'Movies.gz', 'wb')
		print "\r\n[+] downloading Movies.gz..."
		ftp.retrbinary('RETR ' + 'Movies.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Python.gz', 'wb')
		print "\r\n[+] downloading Python.gz..."
		ftp.retrbinary('RETR ' + 'Python.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Trek.gz', 'wb')
		print "\r\n[+] downloading Trek.gz..."
		ftp.retrbinary('RETR ' + 'Trek.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "23":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('music')
		if os.path.isdir('dictionaries/music/') == 0:
			os.mkdir('dictionaries/music/')
		dire = 'dictionaries/music/'
		
		file = open(dire+'music-classical.gz', 'wb')
		print "\r\n[+] downloading music-classical.gz..."
		ftp.retrbinary('RETR ' + 'music-classical.gz', handleDownload)
		filequitter()
			
		file = open(dire+'music-country.gz', 'wb')
		print "\r\n[+] downloading music-country.gz..."
		ftp.retrbinary('RETR ' + 'music-country.gz', handleDownload)
		filequitter()
			
		file = open(dire+'music-jazz.gz', 'wb')
		print "\r\n[+] downloading music-jazz.gz..."
		ftp.retrbinary('RETR ' + 'music-jazz.gz', handleDownload)
		filequitter()
			
		file = open(dire+'music-other.gz', 'wb')
		print "\r\n[+] downloading music-other.gz..."
		ftp.retrbinary('RETR ' + 'music-other.gz', handleDownload)
		filequitter()
			
		file = open(dire+'music-rock.gz', 'wb')
		print "\r\n[+] downloading music-rock.gz..."
		ftp.retrbinary('RETR ' + 'music-rock.gz', handleDownload)
		filequitter()
			
		file = open(dire+'music-shows.gz', 'wb')
		print "\r\n[+] downloading music-shows.gz..."
		ftp.retrbinary('RETR ' + 'music-shows.gz', handleDownload)
		filequitter()
			
		file = open(dire+'rock-groups.gz', 'wb')
		print "\r\n[+] downloading rock-groups.gz..."
		ftp.retrbinary('RETR ' + 'rock-groups.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "24":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('names')
		if os.path.isdir('dictionaries/names/') == 0:
			os.mkdir('dictionaries/names/')
		dire = 'dictionaries/names/'
		
		file = open(dire+'ASSurnames.gz', 'wb')
		print "\r\n[+] downloading ASSurnames.gz..."
		ftp.retrbinary('RETR ' + 'ASSurnames.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Congress.gz', 'wb')
		print "\r\n[+] downloading Congress.gz..."
		ftp.retrbinary('RETR ' + 'Congress.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Family-Names.gz', 'wb')
		print "\r\n[+] downloading Family-Names.gz..."
		ftp.retrbinary('RETR ' + 'Family-Names.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Given-Names.gz', 'wb')
		print "\r\n[+] downloading Given-Names.gz..."
		ftp.retrbinary('RETR ' + 'Given-Names.gz', handleDownload)
		filequitter()
			
		file = open(dire+'actor-givenname.gz', 'wb')
		print "\r\n[+] downloading actor-givenname.gz..."
		ftp.retrbinary('RETR ' + 'actor-givenname.gz', handleDownload)
		filequitter()
			
		file = open(dire+'actor-surname.gz', 'wb')
		print "\r\n[+] downloading actor-surname.gz..."
		ftp.retrbinary('RETR ' + 'actor-surname.gz', handleDownload)
		filequitter()
			
		file = open(dire+'cis-givenname.gz', 'wb')
		print "\r\n[+] downloading cis-givenname.gz..."
		ftp.retrbinary('RETR ' + 'cis-givenname.gz', handleDownload)
		filequitter()
			
		file = open(dire+'cis-surname.gz', 'wb')
		print "\r\n[+] downloading cis-surname.gz..."
		ftp.retrbinary('RETR ' + 'cis-surname.gz', handleDownload)
		filequitter()
			
		file = open(dire+'crl-names.gz', 'wb')
		print "\r\n[+] downloading crl-names.gz..."
		ftp.retrbinary('RETR ' + 'crl-names.gz', handleDownload)
		filequitter()
			
		file = open(dire+'famous.gz', 'wb')
		print "\r\n[+] downloading famous.gz..."
		ftp.retrbinary('RETR ' + 'famous.gz', handleDownload)
		filequitter()
			
		file = open(dire+'fast-names.gz', 'wb')
		print "\r\n[+] downloading fast-names.gz..."
		ftp.retrbinary('RETR ' + 'fast-names.gz', handleDownload)
		filequitter()
			
		file = open(dire+'female-names-kantr.gz', 'wb')
		print "\r\n[+] downloading female-names-kantr.gz..."
		ftp.retrbinary('RETR ' + 'female-names-kantr.gz', handleDownload)
		filequitter()
			
		file = open(dire+'female-names.gz', 'wb')
		print "\r\n[+] downloading female-names.gz..."
		ftp.retrbinary('RETR ' + 'female-names.gz', handleDownload)
		filequitter()
			
		file = open(dire+'givennames-ol.gz', 'wb')
		print "\r\n[+] downloading givennames-ol.gz..."
		ftp.retrbinary('RETR ' + 'givennames-ol.gz', handleDownload)
		filequitter()
			
		file = open(dire+'male-names-kantr.gz', 'wb')
		print "\r\n[+] downloading male-names-kantr.gz..."
		ftp.retrbinary('RETR ' + 'male-names-kantr.gz', handleDownload)
		filequitter()
			
		file = open(dire+'male-names.gz', 'wb')
		print "\r\n[+] downloading male-names.gz..."
		ftp.retrbinary('RETR ' + 'male-names.gz', handleDownload)
		filequitter()
			
		file = open(dire+'movie-characters.gz', 'wb')
		print "\r\n[+] downloading movie-characters.gz..."
		ftp.retrbinary('RETR ' + 'movie-characters.gz', handleDownload)
		filequitter()
			
		file = open(dire+'names.french.gz', 'wb')
		print "\r\n[+] downloading names.french.gz..."
		ftp.retrbinary('RETR ' + 'names.french.gz', handleDownload)
		filequitter()
			
		file = open(dire+'names.hp.gz', 'wb')
		print "\r\n[+] downloading names.hp.gz..."
		ftp.retrbinary('RETR ' + 'names.hp.gz', handleDownload)
		filequitter()
			
		file = open(dire+'other-names.gz', 'wb')
		print "\r\n[+] downloading other-names.gz..."
		ftp.retrbinary('RETR ' + 'other-names.gz', handleDownload)
		filequitter()
			
		file = open(dire+'shakesp-names.gz', 'wb')
		print "\r\n[+] downloading shakesp-names.gz..."
		ftp.retrbinary('RETR ' + 'shakesp-names.gz', handleDownload)
		filequitter()
			
		file = open(dire+'surnames-ol.gz', 'wb')
		print "\r\n[+] downloading surnames-ol.gz..."
		ftp.retrbinary('RETR ' + 'surnames-ol.gz', handleDownload)
		filequitter()
			
		file = open(dire+'surnames.finnish.gz', 'wb')
		print "\r\n[+] downloading surnames.finnish.gz..."
		ftp.retrbinary('RETR ' + 'surnames.finnish.gz', handleDownload)
		filequitter()
			
		file = open(dire+'usenet-names.gz', 'wb')
		print "\r\n[+] downloading usenet-names.gz..."
		ftp.retrbinary('RETR ' + 'usenet-names.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	
	if filedown == "25":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('net')
		if os.path.isdir('dictionaries/net/') == 0:
			os.mkdir('dictionaries/net/')
		dire = 'dictionaries/net/'
		
		file = open(dire+'hosts-txt.gz', 'wb')
		print "\r\n[+] downloading hosts-txt.gz..."
		ftp.retrbinary('RETR ' + 'hosts-txt.gz', handleDownload)
		filequitter()
			
		file = open(dire+'inet-machines.gz', 'wb')
		print "\r\n[+] downloading inet-machines.gz..."
		ftp.retrbinary('RETR ' + 'inet-machines.gz', handleDownload)
		filequitter()
			
		file = open(dire+'usenet-loginids.gz', 'wb')
		print "\r\n[+] downloading usenet-loginids.gz..."
		ftp.retrbinary('RETR ' + 'usenet-loginids.gz', handleDownload)
		filequitter()
			
		file = open(dire+'usenet-machines.gz', 'wb')
		print "\r\n[+] downloading usenet-machines.gz..."
		ftp.retrbinary('RETR ' + 'usenet-machines.gz', handleDownload)
		filequitter()
			
		file = open(dire+'uunet-sites.gz', 'wb')
		print "\r\n[+] downloading uunet-sites.gz..."
		ftp.retrbinary('RETR ' + 'uunet-sites.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "26":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('norwegian')
		if os.path.isdir('dictionaries/norwegian/') == 0:
			os.mkdir('dictionaries/norwegian/')
		dire = 'dictionaries/norwegian/'
		
		file = open(dire+'words.norwegian.gz', 'wb')
		print "\r\n[+] downloading words.norwegian.gz..."
		ftp.retrbinary('RETR ' + 'words.norwegian.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "27":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('places')
		if os.path.isdir('dictionaries/places/') == 0:
			os.mkdir('dictionaries/places/')
		dire = 'dictionaries/places/'
		
		file = open(dire+'Colleges.gz', 'wb')
		print "\r\n[+] downloading Colleges.gz..."
		ftp.retrbinary('RETR ' + 'Colleges.gz', handleDownload)
		filequitter()
			
		file = open(dire+'US-counties.gz', 'wb')
		print "\r\n[+] downloading US-counties.gz..."
		ftp.retrbinary('RETR ' + 'US-counties.gz', handleDownload)
		filequitter()
			
		file = open(dire+'World.factbook.gz', 'wb')
		print "\r\n[+] downloading World.factbook.gz..."
		ftp.retrbinary('RETR ' + 'World.factbook.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Zipcodes.gz', 'wb')
		print "\r\n[+] downloading Zipcodes.gz..."
		ftp.retrbinary('RETR ' + 'Zipcodes.gz', handleDownload)
		filequitter()
			
		file = open(dire+'places.gz', 'wb')
		print "\r\n[+] downloading places.gz..."
		ftp.retrbinary('RETR ' + 'places.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "28":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('polish')
		if os.path.isdir('dictionaries/polish/') == 0:
			os.mkdir('dictionaries/polish/')
		dire = 'dictionaries/polish/'
		
		file = open(dire+'words.polish.gz', 'wb')
		print "\r\n[+] downloading words.polish.gz..."
		ftp.retrbinary('RETR ' + 'words.polish.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "29":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('random')
		if os.path.isdir('dictionaries/random/') == 0:
			os.mkdir('dictionaries/random/')
		dire = 'dictionaries/random/'
		
		file = open(dire+'Ethnologue.gz', 'wb')
		print "\r\n[+] downloading Ethnologue.gz..."
		ftp.retrbinary('RETR ' + 'Ethnologue.gz', handleDownload)
		filequitter()
			
		file = open(dire+'abbr.gz', 'wb')
		print "\r\n[+] downloading abbr.gz..."
		ftp.retrbinary('RETR ' + 'abbr.gz', handleDownload)
		filequitter()
			
		file = open(dire+'chars.gz', 'wb')
		print "\r\n[+] downloading chars.gz..."
		ftp.retrbinary('RETR ' + 'chars.gz', handleDownload)
		filequitter()
			
		file = open(dire+'dogs.gz', 'wb')
		print "\r\n[+] downloading dogs.gz..."
		ftp.retrbinary('RETR ' + 'dogs.gz', handleDownload)
		filequitter()
			
		file = open(dire+'drugs.gz', 'wb')
		print "\r\n[+] downloading drugs.gz..."
		ftp.retrbinary('RETR ' + 'drugs.gz', handleDownload)
		filequitter()
			
		file = open(dire+'junk.gz', 'wb')
		print "\r\n[+] downloading junk.gz..."
		ftp.retrbinary('RETR ' + 'junk.gz', handleDownload)
		filequitter()
			
		file = open(dire+'numbers.gz', 'wb')
		print "\r\n[+] downloading numbers.gz..."
		ftp.retrbinary('RETR ' + 'numbers.gz', handleDownload)
		filequitter()
			
		file = open(dire+'phrases.gz', 'wb')
		print "\r\n[+] downloading phrases.gz..."
		ftp.retrbinary('RETR ' + 'phrases.gz', handleDownload)
		filequitter()
			
		file = open(dire+'sports.gz', 'wb')
		print "\r\n[+] downloading sports.gz..."
		ftp.retrbinary('RETR ' + 'sports.gz', handleDownload)
		filequitter()
			
		file = open(dire+'statistics.gz', 'wb')
		print "\r\n[+] downloading statistics.gz..."
		ftp.retrbinary('RETR ' + 'statistics.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "30":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('religion')
		if os.path.isdir('dictionaries/religion/') == 0:
			os.mkdir('dictionaries/religion/')
		dire = 'dictionaries/religion/'
		
		file = open(dire+'Koran.gz', 'wb')
		print "\r\n[+] downloading Koran.gz..."
		ftp.retrbinary('RETR ' + 'Koran.gz', handleDownload)
		filequitter()
			
		file = open(dire+'kjbible.gz', 'wb')
		print "\r\n[+] downloading kjbible.gz..."
		ftp.retrbinary('RETR ' + 'kjbible.gz', handleDownload)
		filequitter()
			
		file = open(dire+'norse.gz', 'wb')
		print "\r\n[+] downloading norse.gz..."
		ftp.retrbinary('RETR ' + 'norse.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "31":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('russian')
		if os.path.isdir('dictionaries/russian/') == 0:
			os.mkdir('dictionaries/russian/')
		dire = 'dictionaries/russian/'
		
		file = open(dire+'russian.lst.gz', 'wb')
		print "\r\n[+] downloading russian.lst.gz..."
		ftp.retrbinary('RETR ' + 'russian.lst.gz', handleDownload)
		filequitter()
			
		file = open(dire+'russian_words.koi8.gz', 'wb')
		print "\r\n[+] downloading russian_words.koi8.gz..."
		ftp.retrbinary('RETR ' + 'russian_words.koi8.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "32":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('science')
		if os.path.isdir('dictionaries/science/') == 0:
			os.mkdir('dictionaries/science/')
		dire = 'dictionaries/science/'
		
		file = open(dire+'Acr-diagnosis.gz', 'wb')
		print "\r\n[+] downloading Acr-diagnosis.gz..."
		ftp.retrbinary('RETR ' + 'Acr-diagnosis.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Algae.gz', 'wb')
		print "\r\n[+] downloading Algae.gz..."
		ftp.retrbinary('RETR ' + 'Algae.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Bacteria.gz', 'wb')
		print "\r\n[+] downloading Bacteria.gz..."
		ftp.retrbinary('RETR ' + 'Bacteria.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Fungi.gz', 'wb')
		print "\r\n[+] downloading Fungi.gz..."
		ftp.retrbinary('RETR ' + 'Fungi.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Microalgae.gz', 'wb')
		print "\r\n[+] downloading Microalgae.gz..."
		ftp.retrbinary('RETR ' + 'Microalgae.gz', handleDownload)
		filequitter()
			
		file = open(dire+'Viruses.gz', 'wb')
		print "\r\n[+] downloading Viruses.gz..."
		ftp.retrbinary('RETR ' + 'Viruses.gz', handleDownload)
		filequitter()
			
		file = open(dire+'asteroids.gz', 'wb')
		print "\r\n[+] downloading asteroids.gz..."
		ftp.retrbinary('RETR ' + 'asteroids.gz', handleDownload)
		filequitter()
			
		file = open(dire+'biology.gz', 'wb')
		print "\r\n[+] downloading biology.gz..."
		ftp.retrbinary('RETR ' + 'biology.gz', handleDownload)
		filequitter()
			
		file = open(dire+'tech.gz', 'wb')
		print "\r\n[+] downloading tech.gz..."
		ftp.retrbinary('RETR ' + 'tech.gz', handleDownload)
		filequitter()
		
		print '[+] files saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "33":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('spanish')
		if os.path.isdir('dictionaries/spanish/') == 0:
			os.mkdir('dictionaries/spanish/')
		dire = 'dictionaries/spanish/'
		
		file = open(dire+'words.spanish.gz', 'wb')
		print "\r\n[+] downloading words.spanish.gz..."
		ftp.retrbinary('RETR ' + 'words.spanish.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "34":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('swahili')
		if os.path.isdir('dictionaries/swahili/') == 0:
			os.mkdir('dictionaries/swahili/')
		dire = 'dictionaries/swahili/'
		
		file = open(dire+'swahili.gz', 'wb')
		print "\r\n[+] downloading swahili.gz..."
		ftp.retrbinary('RETR ' + 'swahili.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "35":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('swedish')
		if os.path.isdir('dictionaries/swedish/') == 0:
			os.mkdir('dictionaries/swedish/')
		dire = 'dictionaries/swedish/'
		
		file = open(dire+'words.swedish.gz', 'wb')
		print "\r\n[+] downloading words.swedish.gz..."
		ftp.retrbinary('RETR ' + 'words.swedish.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "36":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('turkish')
		if os.path.isdir('dictionaries/turkish/') == 0:
			os.mkdir('dictionaries/turkish/')
		dire = 'dictionaries/turkish/'
		
		file = open(dire+'turkish.dict.gz', 'wb')
		print "\r\n[+] downloading turkish.dict.gz..."
		ftp.retrbinary('RETR ' + 'turkish.dict.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	if filedown == "37":
		print "[+] connecting..."
		ftp = ftplib.FTP(ftpurl)
		downloader()
		ftp.cwd('yiddish')
		if os.path.isdir('dictionaries/yiddish/') == 0:
			os.mkdir('dictionaries/yiddish/')
		dire = 'dictionaries/yiddish/'
		
		file = open(dire+'yiddish.gz', 'wb')
		print "\r\n[+] downloading yiddish.gz..."
		ftp.retrbinary('RETR ' + 'yiddish.gz', handleDownload)
		filequitter()
		
		print '[+] file saved to '+ dire
		ftp.quit()
		exit()
	
	
	
	else:
		print '[-] leaving.'	
		exit()


else:
	print "\r\n[Usage]:	"+sys.argv[0] +"  [OPTIONS] \r\n"
	print "[Help]:		"+sys.argv[0] +"  -h\r\n"
	exit()
