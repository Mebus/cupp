#!/usr/bin/python3
#
#  [Program]
#
#  CUPP 3.2.2-alpha
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
import configparser
import urllib.request, urllib.parse, urllib.error
import gzip
import csv


# Reading configuration file...
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "cupp.cfg"))

years = config.get("years", "years").split(",")
chars = config.get("specialchars", "chars").split(",")

numfrom = config.getint("nums", "from")
numto = config.getint("nums", "to")

wcfrom = config.getint("nums", "wcfrom")
wcto = config.getint("nums", "wcto")

threshold = config.getint("nums", "threshold")

# 1337 mode configs, well you can add more lines if you add it to config file too.
# You will need to add more lines in two places in cupp.py code as well...
a = config.get("leet", "a")
i = config.get("leet", "i")
e = config.get("leet", "e")
t = config.get("leet", "t")
o = config.get("leet", "o")
s = config.get("leet", "s")
g = config.get("leet", "g")
z = config.get("leet", "z")


# for concatenations...


def concats(seq, start, stop):
    for mystr in seq:
        for num in range(start, stop):
            yield mystr + str(num)


# for sorting and making combinations...


def komb(seq, start, special=""):
    for mystr in seq:
        for mystr1 in start:
            yield mystr + special + mystr1


# print list to file counting words


def print_to_file(filename, unique_list_finished):
    f = open(filename, "w")
    unique_list_finished.sort()
    f.write(os.linesep.join(unique_list_finished))
    f = open(filename, "r")
    lines = 0
    for line in f:
        lines += 1
    f.close()
    print(
        "[+] Saving dictionary to \033[1;31m"
        + filename
        + "\033[1;m, counting \033[1;31m"
        + str(lines)
        + " words.\033[1;m"
    )
    print(
        "[+] Now load your pistolero with \033[1;31m"
        + filename
        + "\033[1;m and shoot! Good luck!"
    )


if len(sys.argv) < 2 or sys.argv[1] == "-h":
    print(" ___________ ")
    print(" \033[07m  cupp.py! \033[27m                # Common")
    print("      \                     # User")
    print("       \   \033[1;31m,__,\033[1;m             # Passwords")
    print("        \  \033[1;31m(\033[1;moo\033[1;31m)____\033[1;m         # Profiler")
    print("           \033[1;31m(__)    )\ \033[1;m  ")
    print(
        "           \033[1;31m   ||--|| \033[1;m\033[05m*\033[25m\033[1;m      [ Muris Kurgas | j0rgan@remote-exploit.org ]\r\n\r\n"
    )

    print("	[ Options ]\r\n")
    print("	-h	You are looking at it baby! :)")
    print(" 		 For more help take a look in docs/README")
    print("		 Global configuration file is cupp.cfg\n")

    print("	-i	Interactive questions for user password profiling\r\n")

    print("	-w	Use this option to improve existing dictionary,")
    print("		 or WyD.pl output to make some pwnsauce\r\n")

    print("	-l	Download huge wordlists from repository\r\n")
    print("	-a	Parse default usernames and passwords directly from Alecto DB.")
    print("		 Project Alecto uses purified databases of Phenoelit and CIRT")
    print("		 which where merged and enhanced.\r\n")
    print("	-v	Version of the program\r\n")
    exit()

elif sys.argv[1] == "-v":
    print("\r\n	\033[1;31m[ cupp.py ]  v3.2.2-alpha\033[1;m\r\n")
    print("	* Hacked up by j0rgan - j0rgan@remote-exploit.org")
    print("	* http://www.remote-exploit.org\r\n")
    print("	Take a look ./README.md file for more info about the program\r\n")
    exit()


elif sys.argv[1] == "-w":
    if len(sys.argv) < 3:
        print("\r\n[Usage]:	" + sys.argv[0] + "  -w  [FILENAME]\r\n")
        exit()
    fajl = open(sys.argv[2], "r")
    listic = fajl.readlines()
    linije = 0
    for line in listic:
        linije += 1

    listica = []
    for x in listic:
        listica += x.split()

    print("\r\n      *************************************************")
    print("      *                    \033[1;31mWARNING!!!\033[1;m                 *")
    print("      *         Using large wordlists in some         *")
    print("      *       options bellow is NOT recommended!      *")
    print("      *************************************************\r\n")

    conts = input(
        "> Do you want to concatenate all words from wordlist? Y/[N]: "
    ).lower()

    if conts == "y" and linije > threshold:
        print("\r\n[-] Maximum number of words for concatenation is " + str(threshold))
        print("[-] Check configuration file for increasing this number.\r\n")
        conts = input(
            "> Do you want to concatenate all words from wordlist? Y/[N]: "
        ).lower()
    conts = conts
    cont = [""]
    if conts == "y":
        for cont1 in listica:
            for cont2 in listica:
                if listica.index(cont1) != listica.index(cont2):
                    cont.append(cont1 + cont2)

    spechars = [""]
    spechars1 = input(
        "> Do you want to add special chars at the end of words? Y/[N]: "
    ).lower()
    if spechars1 == "y":
        for spec1 in chars:
            spechars.append(spec1)
            for spec2 in chars:
                spechars.append(spec1 + spec2)
                for spec3 in chars:
                    spechars.append(spec1 + spec2 + spec3)

    randnum = input(
        "> Do you want to add some random numbers at the end of words? Y/[N]:"
    ).lower()
    leetmode = input("> Leet mode? (i.e. leet = 1337) Y/[N]: ").lower()

    kombinacija1 = list(komb(listica, years))
    kombinacija2 = [""]
    if conts == "y":
        kombinacija2 = list(komb(cont, years))
    kombinacija3 = [""]
    kombinacija4 = [""]
    if spechars1 == "y":
        kombinacija3 = list(komb(listica, spechars))
        if conts == "y":
            kombinacija4 = list(komb(cont, spechars))
    kombinacija5 = [""]
    kombinacija6 = [""]
    if randnum == "y":
        kombinacija5 = list(concats(listica, numfrom, numto))
        if conts == "y":
            kombinacija6 = list(concats(cont, numfrom, numto))

    print("\r\n[+] Now making a dictionary...")

    print("[+] Sorting list and removing duplicates...")

    komb_unique1 = list(dict.fromkeys(kombinacija1).keys())
    komb_unique2 = list(dict.fromkeys(kombinacija2).keys())
    komb_unique3 = list(dict.fromkeys(kombinacija3).keys())
    komb_unique4 = list(dict.fromkeys(kombinacija4).keys())
    komb_unique5 = list(dict.fromkeys(kombinacija5).keys())
    komb_unique6 = list(dict.fromkeys(kombinacija6).keys())
    komb_unique7 = list(dict.fromkeys(listica).keys())
    komb_unique8 = list(dict.fromkeys(cont).keys())

    uniqlist = (
        komb_unique1
        + komb_unique2
        + komb_unique3
        + komb_unique4
        + komb_unique5
        + komb_unique6
        + komb_unique7
        + komb_unique8
    )

    unique_lista = list(dict.fromkeys(uniqlist).keys())
    unique_leet = []
    if leetmode == "y":
        for (
            x
        ) in (
            unique_lista
        ):  # if you want to add more leet chars, you will need to add more lines in cupp.cfg too...
            x = x.replace("a", a)
            x = x.replace("i", i)
            x = x.replace("e", e)
            x = x.replace("t", t)
            x = x.replace("o", o)
            x = x.replace("s", s)
            x = x.replace("g", g)
            x = x.replace("z", z)
            unique_leet.append(x)

    unique_list = unique_lista + unique_leet

    unique_list_finished = []

    unique_list_finished = [x for x in unique_list if len(x) > wcfrom and len(x) < wcto]

    print_to_file(sys.argv[2] + ".cupp.txt", unique_list_finished)

    fajl.close()
    exit()


elif sys.argv[1] == "-i":
    print("\r\n[+] Insert the information about the victim to make a dictionary")
    print("[+] If you don't know all the info, just hit enter when asked! ;)\r\n")

    # We need some information first!

    name = input("> First Name: ").lower()
    while len(name) == 0 or name == " " or name == "  " or name == "   ":
        print("\r\n[-] You must enter a name at least!")
        name = input("> Name: ").lower()
    name = str(name)

    surname = input("> Surname: ").lower()
    nick = input("> Nickname: ").lower()
    birthdate = input("> Birthdate (DDMMYYYY): ")
    while len(birthdate) != 0 and len(birthdate) != 8:
        print("\r\n[-] You must enter 8 digits for birthday!")
        birthdate = input("> Birthdate (DDMMYYYY): ")
    birthdate = str(birthdate)

    print("\r\n")

    wife = input("> Partners) name: ").lower()
    wifen = input("> Partners) nickname: ").lower()
    wifeb = input("> Partners) birthdate (DDMMYYYY): ")
    while len(wifeb) != 0 and len(wifeb) != 8:
        print("\r\n[-] You must enter 8 digits for birthday!")
        wifeb = input("> Partners birthdate (DDMMYYYY): ")
    wifeb = str(wifeb)
    print("\r\n")

    kid = input("> Child's name: ").lower()
    kidn = input("> Child's nickname: ").lower()
    kidb = input("> Child's birthdate (DDMMYYYY): ")
    while len(kidb) != 0 and len(kidb) != 8:
        print("\r\n[-] You must enter 8 digits for birthday!")
        kidb = input("> Child's birthdate (DDMMYYYY): ")
    kidb = str(kidb)
    print("\r\n")

    pet = input("> Pet's name: ").lower()
    company = input("> Company name: ").lower()
    print("\r\n")

    words = [""]
    words1 = input(
        "> Do you want to add some key words about the victim? Y/[N]: "
    ).lower()
    words2 = ""
    if words1 == "y":
        words2 = input(
            "> Please enter the words, separated by comma. [i.e. hacker,juice,black], spaces will be removed: "
        ).replace(" ", "")
    words = words2.split(",")

    spechars = [""]
    spechars1 = input(
        "> Do you want to add special chars at the end of words? Y/[N]: "
    ).lower()
    if spechars1 == "y":
        for spec1 in chars:
            spechars.append(spec1)
            for spec2 in chars:
                spechars.append(spec1 + spec2)
                for spec3 in chars:
                    spechars.append(spec1 + spec2 + spec3)

    randnum = input(
        "> Do you want to add some random numbers at the end of words? Y/[N]:"
    ).lower()
    leetmode = input("> Leet mode? (i.e. leet = 1337) Y/[N]: ").lower()

    print("\r\n[+] Now making a dictionary...")

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
    wordsup = list(map(str.title, words))

    word = words + wordsup

    # reverse a name

    rev_name = name[::-1]
    rev_nameup = nameup[::-1]
    rev_nick = nick[::-1]
    rev_nickup = nickup[::-1]
    rev_wife = wife[::-1]
    rev_wifeup = wifeup[::-1]
    rev_kid = kid[::-1]
    rev_kidup = kidup[::-1]

    reverse = [
        rev_name,
        rev_nameup,
        rev_nick,
        rev_nickup,
        rev_wife,
        rev_wifeup,
        rev_kid,
        rev_kidup,
    ]
    rev_n = [rev_name, rev_nameup, rev_nick, rev_nickup]
    rev_w = [rev_wife, rev_wifeup]
    rev_k = [rev_kid, rev_kidup]
    # Let's do some serious work! This will be a mess of code, but... who cares? :)

    # Birthdays combinations

    bds = [
        birthdate_yy,
        birthdate_yyy,
        birthdate_yyyy,
        birthdate_xd,
        birthdate_xm,
        birthdate_dd,
        birthdate_mm,
    ]

    bdss = []

    for bds1 in bds:
        bdss.append(bds1)
        for bds2 in bds:
            if bds.index(bds1) != bds.index(bds2):
                bdss.append(bds1 + bds2)
                for bds3 in bds:
                    if (
                        bds.index(bds1) != bds.index(bds2)
                        and bds.index(bds2) != bds.index(bds3)
                        and bds.index(bds1) != bds.index(bds3)
                    ):
                        bdss.append(bds1 + bds2 + bds3)

                # For a woman...
    wbds = [wifeb_yy, wifeb_yyy, wifeb_yyyy, wifeb_xd, wifeb_xm, wifeb_dd, wifeb_mm]

    wbdss = []

    for wbds1 in wbds:
        wbdss.append(wbds1)
        for wbds2 in wbds:
            if wbds.index(wbds1) != wbds.index(wbds2):
                wbdss.append(wbds1 + wbds2)
                for wbds3 in wbds:
                    if (
                        wbds.index(wbds1) != wbds.index(wbds2)
                        and wbds.index(wbds2) != wbds.index(wbds3)
                        and wbds.index(wbds1) != wbds.index(wbds3)
                    ):
                        wbdss.append(wbds1 + wbds2 + wbds3)

                # and a child...
    kbds = [kidb_yy, kidb_yyy, kidb_yyyy, kidb_xd, kidb_xm, kidb_dd, kidb_mm]

    kbdss = []

    for kbds1 in kbds:
        kbdss.append(kbds1)
        for kbds2 in kbds:
            if kbds.index(kbds1) != kbds.index(kbds2):
                kbdss.append(kbds1 + kbds2)
                for kbds3 in kbds:
                    if (
                        kbds.index(kbds1) != kbds.index(kbds2)
                        and kbds.index(kbds2) != kbds.index(kbds3)
                        and kbds.index(kbds1) != kbds.index(kbds3)
                    ):
                        kbdss.append(kbds1 + kbds2 + kbds3)

                # string combinations....

    kombinaac = [pet, petup, company, companyup]

    kombina = [name, surname, nick, nameup, surnameup, nickup]

    kombinaw = [wife, wifen, wifeup, wifenup, surname, surnameup]

    kombinak = [kid, kidn, kidup, kidnup, surname, surnameup]

    kombinaa = []
    for kombina1 in kombina:
        kombinaa.append(kombina1)
        for kombina2 in kombina:
            if kombina.index(kombina1) != kombina.index(kombina2) and kombina.index(
                kombina1.title()
            ) != kombina.index(kombina2.title()):
                kombinaa.append(kombina1 + kombina2)

    kombinaaw = []
    for kombina1 in kombinaw:
        kombinaaw.append(kombina1)
        for kombina2 in kombinaw:
            if kombinaw.index(kombina1) != kombinaw.index(kombina2) and kombinaw.index(
                kombina1.title()
            ) != kombinaw.index(kombina2.title()):
                kombinaaw.append(kombina1 + kombina2)

    kombinaak = []
    for kombina1 in kombinak:
        kombinaak.append(kombina1)
        for kombina2 in kombinak:
            if kombinak.index(kombina1) != kombinak.index(kombina2) and kombinak.index(
                kombina1.title()
            ) != kombinak.index(kombina2.title()):
                kombinaak.append(kombina1 + kombina2)

    komb1 = list(komb(kombinaa, bdss))
    komb1 += list(komb(kombinaa, bdss, "_"))
    komb2 = list(komb(kombinaaw, wbdss))
    komb2 += list(komb(kombinaaw, wbdss, "_"))
    komb3 = list(komb(kombinaak, kbdss))
    komb3 += list(komb(kombinaak, kbdss, "_"))
    komb4 = list(komb(kombinaa, years))
    komb4 += list(komb(kombinaa, years, "_"))
    komb5 = list(komb(kombinaac, years))
    komb5 += list(komb(kombinaac, years, "_"))
    komb6 = list(komb(kombinaaw, years))
    komb6 += list(komb(kombinaaw, years, "_"))
    komb7 = list(komb(kombinaak, years))
    komb7 += list(komb(kombinaak, years, "_"))
    komb8 = list(komb(word, bdss))
    komb8 += list(komb(word, bdss, "_"))
    komb9 = list(komb(word, wbdss))
    komb9 += list(komb(word, wbdss, "_"))
    komb10 = list(komb(word, kbdss))
    komb10 += list(komb(word, kbdss, "_"))
    komb11 = list(komb(word, years))
    komb11 += list(komb(word, years, "_"))
    komb12 = [""]
    komb13 = [""]
    komb14 = [""]
    komb15 = [""]
    komb16 = [""]
    komb21 = [""]
    if randnum == "y":
        komb12 = list(concats(word, numfrom, numto))
        komb13 = list(concats(kombinaa, numfrom, numto))
        komb14 = list(concats(kombinaac, numfrom, numto))
        komb15 = list(concats(kombinaaw, numfrom, numto))
        komb16 = list(concats(kombinaak, numfrom, numto))
        komb21 = list(concats(reverse, numfrom, numto))
    komb17 = list(komb(reverse, years))
    komb17 += list(komb(reverse, years, "_"))
    komb18 = list(komb(rev_w, wbdss))
    komb18 += list(komb(rev_w, wbdss, "_"))
    komb19 = list(komb(rev_k, kbdss))
    komb19 += list(komb(rev_k, kbdss, "_"))
    komb20 = list(komb(rev_n, bdss))
    komb20 += list(komb(rev_n, bdss, "_"))
    komb001 = [""]
    komb002 = [""]
    komb003 = [""]
    komb004 = [""]
    komb005 = [""]
    komb006 = [""]
    if spechars1 == "y":
        komb001 = list(komb(kombinaa, spechars))
        komb002 = list(komb(kombinaac, spechars))
        komb003 = list(komb(kombinaaw, spechars))
        komb004 = list(komb(kombinaak, spechars))
        komb005 = list(komb(word, spechars))
        komb006 = list(komb(reverse, spechars))

    print("[+] Sorting list and removing duplicates...")

    komb_unique1 = list(dict.fromkeys(komb1).keys())
    komb_unique2 = list(dict.fromkeys(komb2).keys())
    komb_unique3 = list(dict.fromkeys(komb3).keys())
    komb_unique4 = list(dict.fromkeys(komb4).keys())
    komb_unique5 = list(dict.fromkeys(komb5).keys())
    komb_unique6 = list(dict.fromkeys(komb6).keys())
    komb_unique7 = list(dict.fromkeys(komb7).keys())
    komb_unique8 = list(dict.fromkeys(komb8).keys())
    komb_unique9 = list(dict.fromkeys(komb9).keys())
    komb_unique10 = list(dict.fromkeys(komb10).keys())
    komb_unique11 = list(dict.fromkeys(komb11).keys())
    komb_unique12 = list(dict.fromkeys(komb12).keys())
    komb_unique13 = list(dict.fromkeys(komb13).keys())
    komb_unique14 = list(dict.fromkeys(komb14).keys())
    komb_unique15 = list(dict.fromkeys(komb15).keys())
    komb_unique16 = list(dict.fromkeys(komb16).keys())
    komb_unique17 = list(dict.fromkeys(komb17).keys())
    komb_unique18 = list(dict.fromkeys(komb18).keys())
    komb_unique19 = list(dict.fromkeys(komb19).keys())
    komb_unique20 = list(dict.fromkeys(komb20).keys())
    komb_unique21 = list(dict.fromkeys(komb21).keys())
    komb_unique01 = list(dict.fromkeys(kombinaa).keys())
    komb_unique02 = list(dict.fromkeys(kombinaac).keys())
    komb_unique03 = list(dict.fromkeys(kombinaaw).keys())
    komb_unique04 = list(dict.fromkeys(kombinaak).keys())
    komb_unique05 = list(dict.fromkeys(word).keys())
    komb_unique07 = list(dict.fromkeys(komb001).keys())
    komb_unique08 = list(dict.fromkeys(komb002).keys())
    komb_unique09 = list(dict.fromkeys(komb003).keys())
    komb_unique010 = list(dict.fromkeys(komb004).keys())
    komb_unique011 = list(dict.fromkeys(komb005).keys())
    komb_unique012 = list(dict.fromkeys(komb006).keys())

    uniqlist = (
        bdss
        + wbdss
        + kbdss
        + reverse
        + komb_unique01
        + komb_unique02
        + komb_unique03
        + komb_unique04
        + komb_unique05
        + komb_unique1
        + komb_unique2
        + komb_unique3
        + komb_unique4
        + komb_unique5
        + komb_unique6
        + komb_unique7
        + komb_unique8
        + komb_unique9
        + komb_unique10
        + komb_unique11
        + komb_unique12
        + komb_unique13
        + komb_unique14
        + komb_unique15
        + komb_unique16
        + komb_unique17
        + komb_unique18
        + komb_unique19
        + komb_unique20
        + komb_unique21
        + komb_unique07
        + komb_unique08
        + komb_unique09
        + komb_unique010
        + komb_unique011
        + komb_unique012
    )

    unique_lista = list(dict.fromkeys(uniqlist).keys())
    unique_leet = []
    if leetmode == "y":
        for (
            x
        ) in (
            unique_lista
        ):  # if you want to add more leet chars, you will need to add more lines in cupp.cfg too...
            x = x.replace("a", a)
            x = x.replace("i", i)
            x = x.replace("e", e)
            x = x.replace("t", t)
            x = x.replace("o", o)
            x = x.replace("s", s)
            x = x.replace("g", g)
            x = x.replace("z", z)
            unique_leet.append(x)

    unique_list = unique_lista + unique_leet

    unique_list_finished = []
    unique_list_finished = [x for x in unique_list if len(x) < wcto and len(x) > wcfrom]

    print_to_file(name + ".txt", unique_list_finished)
    exit()


elif sys.argv[1] == "-a":
    url = config.get("alecto", "alectourl")

    print("\r\n[+] Checking if alectodb is not present...")
    if os.path.isfile("alectodb.csv.gz") == 0:
        print("[+] Downloading alectodb.csv.gz...")
        webFile = urllib.request.urlopen(url)
        localFile = open(url.split("/")[-1], "wb")
        localFile.write(webFile.read())
        webFile.close()
        localFile.close()

    f = gzip.open("alectodb.csv.gz", "rt")

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

    print(
        "\r\n[+] Exporting to alectodb-usernames.txt and alectodb-passwords.txt\r\n[+] Done."
    )
    f = open("alectodb-usernames.txt", "w")
    f.write(os.linesep.join(gus))
    f.close()

    f = open("alectodb-passwords.txt", "w")
    f.write(os.linesep.join(gpa))
    f.close()

    f.close()
    sys.exit()


elif sys.argv[1] == "-l":

    ftpname = config.get("downloader", "ftpname")
    ftpurl = config.get("downloader", "ftpurl")
    ftppath = config.get("downloader", "ftppath")
    ftpuser = config.get("downloader", "ftpuser")
    ftppass = config.get("downloader", "ftppass")

    if os.path.isdir("dictionaries") == 0:
        os.mkdir("dictionaries")

    print("	\r\n	Choose the section you want to download:\r\n")

    print("     1   Moby            14      french          27      places")
    print("     2   afrikaans       15      german          28      polish")
    print("     3   american        16      hindi           29      random")
    print("     4   aussie          17      hungarian       30      religion")
    print("     5   chinese         18      italian         31      russian")
    print("     6   computer        19      japanese        32      science")
    print("     7   croatian        20      latin           33      spanish")
    print("     8   czech           21      literature      34      swahili")
    print("     9   danish          22      movieTV         35      swedish")
    print("    10   databases       23      music           36      turkish")
    print("    11   dictionaries    24      names           37      yiddish")
    print("    12   dutch           25      net             38      exit program")
    print("    13   finnish         26      norwegian       \r\n")
    print("	\r\n	Files will be downloaded from " + ftpname + " repository")
    print(
        "	\r\n	Tip: After downloading wordlist, you can improve it with -w option\r\n"
    )

    filedown = input("> Enter number: ")
    filedown.isdigit()
    while filedown.isdigit() == 0:
        print("\r\n[-] Wrong choice. ")
        filedown = input("> Enter number: ")
    filedown = str(filedown)
    while int(filedown) > 38:
        print("\r\n[-] Wrong choice. ")
        filedown = input("> Enter number: ")
    filedown = str(filedown)

    def downloader():
        ftp.login(ftpuser, ftppass)
        ftp.cwd(ftppath)

    # retrieve a file from FTP
    def retr_binary_file(ftp, dire, filename):
        def handleDownload(block):
            f.write(block)
            print(".", end="")

        f = open(dire + filename, "wb")
        print("\r\n[+] downloading " + filename + "...")
        # ftp.retrbinary("RETR " + filename, f.write)
        ftp.retrbinary("RETR " + filename, handleDownload)
        f.close()
        print(" done.")

    # retrieve a list of files
    def retr_file_list(ftp, dire, file_list):
        for f in file_list:
            retr_binary_file(ftp, dire, f)

    if filedown == "1":
        print("\r\n[+] connecting...\r\n")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("Moby")
        if os.path.isdir("dictionaries/Moby/") == 0:
            os.mkdir("dictionaries/Moby/")
        dire = "dictionaries/Moby/"

        files_to_download = {
            "mhyph.tar.gz",
            "mlang.tar.gz",
            "moby.tar.gz",
            "mpos.tar.gz",
            "mpron.tar.gz",
            "mthes.tar.gz",
            "mwords.tar.gz",
        }

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "2":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("afrikaans")
        if os.path.isdir("dictionaries/afrikaans/") == 0:
            os.mkdir("dictionaries/afrikaans/")
        dire = "dictionaries/afrikaans/"

        retr_binary_file(ftp, dire, "afr_dbf.zip")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "3":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("american")
        if os.path.isdir("dictionaries/american/") == 0:
            os.mkdir("dictionaries/american/")
        dire = "dictionaries/american/"

        retr_binary_file(ftp, dire, "dic-0294.tar.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "4":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("aussie")
        if os.path.isdir("dictionaries/aussie/") == 0:
            os.mkdir("dictionaries/aussie/")
        dire = "dictionaries/aussie/"

        retr_binary_file(ftp, dire, "oz.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "5":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("chinese")
        if os.path.isdir("dictionaries/chinese/") == 0:
            os.mkdir("dictionaries/chinese/")
        dire = "dictionaries/chinese/"

        retr_binary_file(ftp, dire, "chinese.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "6":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("computer")
        if os.path.isdir("dictionaries/computer/") == 0:
            os.mkdir("dictionaries/computer/")
        dire = "dictionaries/computer/"

        files_to_download = {
            "Domains.gz",
            "Dosref.gz",
            "Ftpsites.gz",
            "Jargon.gz",
            "common-passwords.txt.gz",
            "etc-hosts.gz",
            "foldoc.gz",
            "language-list.gz",
            "unix.gz",
        }

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "7":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("croatian")
        if os.path.isdir("dictionaries/croatian/") == 0:
            os.mkdir("dictionaries/croatian/")
        dire = "dictionaries/croatian/"

        retr_binary_file(ftp, dire, "croatian.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "8":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("czech")
        if os.path.isdir("dictionaries/czech/") == 0:
            os.mkdir("dictionaries/czech/")
        dire = "dictionaries/czech/"

        retr_binary_file(ftp, dire, "czech-wordlist-ascii-cstug-novak.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "9":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("danish")
        if os.path.isdir("dictionaries/danish/") == 0:
            os.mkdir("dictionaries/danish/")
        dire = "dictionaries/danish/"

        retr_binary_file(ftp, dire, "danish.words.gz")
        retr_binary_file(ftp, dire, "dansk.zip")

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "10":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("databases")
        if os.path.isdir("dictionaries/databases/") == 0:
            os.mkdir("dictionaries/databases/")
        dire = "dictionaries/databases/"

        files_to_download = {
            "acronyms.gz",
            "att800.gz",
            "computer-companies.gz",
            "world_heritage.gz",
        }

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "11":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("dictionaries")
        if os.path.isdir("dictionaries/dictionaries/") == 0:
            os.mkdir("dictionaries/dictionaries/")
        dire = "dictionaries/dictionaries/"

        files_to_download = {
            "Antworth.gz",
            "CRL.words.gz",
            "Roget.words.gz",
            "Unabr.dict.gz",
            "Unix.dict.gz",
            "englex-dict.gz",
            "knuth_britsh.gz",
            "knuth_words.gz",
            "pocket-dic.gz",
            "shakesp-glossary.gz",
            "special.eng.gz",
            "words-english.gz",
        }

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "12":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("dutch")
        if os.path.isdir("dictionaries/dutch/") == 0:
            os.mkdir("dictionaries/dutch/")
        dire = "dictionaries/dutch/"

        retr_binary_file(ftp, dire, "words.dutch.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "13":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("finnish")
        if os.path.isdir("dictionaries/finnish/") == 0:
            os.mkdir("dictionaries/finnish/")
        dire = "dictionaries/finnish/"

        files_to_download = {
            "finnish.gz",
            "firstnames.finnish.gz",
            "words.finnish.FAQ.gz",
        }

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "14":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("french")
        if os.path.isdir("dictionaries/french/") == 0:
            os.mkdir("dictionaries/french/")
        dire = "dictionaries/french/"

        retr_binary_file(ftp, dire, "dico.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "15":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("german")
        if os.path.isdir("dictionaries/german/") == 0:
            os.mkdir("dictionaries/german/")
        dire = "dictionaries/german/"

        files_to_download = {"deutsch.dic.gz", "germanl.gz", "words.german.gz"}

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "16":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("hindi")
        if os.path.isdir("dictionaries/hindi/") == 0:
            os.mkdir("dictionaries/hindi/")
        dire = "dictionaries/hindi/"

        retr_binary_file(ftp, dire, "hindu-names.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "17":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("hungarian")
        if os.path.isdir("dictionaries/hungarian/") == 0:
            os.mkdir("dictionaries/hungarian/")
        dire = "dictionaries/hungarian/"

        retr_binary_file(ftp, dire, "hungarian.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "18":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("italian")
        if os.path.isdir("dictionaries/italian/") == 0:
            os.mkdir("dictionaries/italian/")
        dire = "dictionaries/italian/"

        retr_binary_file(ftp, dire, "words.italian.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "19":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("japanese")
        if os.path.isdir("dictionaries/japanese/") == 0:
            os.mkdir("dictionaries/japanese/")
        dire = "dictionaries/japanese/"

        retr_binary_file(ftp, dire, "words.japanese.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "20":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("latin")
        if os.path.isdir("dictionaries/latin/") == 0:
            os.mkdir("dictionaries/latin/")
        dire = "dictionaries/latin/"

        retr_binary_file(ftp, dire, "wordlist.aug.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "21":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("literature")
        if os.path.isdir("dictionaries/literature/") == 0:
            os.mkdir("dictionaries/literature/")
        dire = "dictionaries/literature/"

        files_to_download = {
            "LCarrol.gz",
            "Paradise.Lost.gz",
            "aeneid.gz",
            "arthur.gz",
            "cartoon.gz",
            "cartoons-olivier.gz",
            "charlemagne.gz",
            "fable.gz",
            "iliad.gz",
            "myths-legends.gz",
            "odyssey.gz",
            "sf.gz",
            "shakespeare.gz",
            "tolkien.words.gz",
        }

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "22":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("movieTV")
        if os.path.isdir("dictionaries/movieTV/") == 0:
            os.mkdir("dictionaries/movieTV/")
        dire = "dictionaries/movieTV/"

        files_to_download = {"Movies.gz", "Python.gz", "Trek.gz"}

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "23":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("music")
        if os.path.isdir("dictionaries/music/") == 0:
            os.mkdir("dictionaries/music/")
        dire = "dictionaries/music/"

        files_to_download = {
            "music-classical.gz",
            "music-country.gz",
            "music-jazz.gz",
            "music-other.gz",
            "music-rock.gz",
            "music-shows.gz",
            "rock-groups.gz",
        }

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "24":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("names")
        if os.path.isdir("dictionaries/names/") == 0:
            os.mkdir("dictionaries/names/")
        dire = "dictionaries/names/"

        files_to_download = {
            "ASSurnames.gz",
            "Congress.gz",
            "Family-Names.gz",
            "Given-Names.gz",
            "actor-givenname.gz",
            "actor-surname.gz",
            "cis-givenname.gz",
            "cis-surname.gz",
            "crl-names.gz",
            "famous.gz",
            "fast-names.gz",
            "female-names-kantr.gz",
            "female-names.gz",
            "givennames-ol.gz",
            "male-names-kantr.gz",
            "male-names.gz",
            "movie-characters.gz",
            "names.french.gz",
            "names.hp.gz",
            "other-names.gz",
            "shakesp-names.gz",
            "surnames-ol.gz",
            "surnames.finnish.gz",
            "usenet-names.gz",
        }

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "25":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("net")
        if os.path.isdir("dictionaries/net/") == 0:
            os.mkdir("dictionaries/net/")
        dire = "dictionaries/net/"

        files_to_download = {
            "hosts-txt.gz",
            "inet-machines.gz",
            "usenet-loginids.gz",
            "usenet-machines.gz",
            "uunet-sites.gz",
        }

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "26":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("norwegian")
        if os.path.isdir("dictionaries/norwegian/") == 0:
            os.mkdir("dictionaries/norwegian/")
        dire = "dictionaries/norwegian/"

        retr_binary_file(ftp, dire, "words.norwegian.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "27":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("places")
        if os.path.isdir("dictionaries/places/") == 0:
            os.mkdir("dictionaries/places/")
        dire = "dictionaries/places/"

        files_to_download = {
            "Colleges.gz",
            "US-counties.gz",
            "World.factbook.gz",
            "Zipcodes.gz",
            "places.gz",
        }

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "28":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("polish")
        if os.path.isdir("dictionaries/polish/") == 0:
            os.mkdir("dictionaries/polish/")
        dire = "dictionaries/polish/"

        retr_binary_file(ftp, dire, "words.polish.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "29":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("random")
        if os.path.isdir("dictionaries/random/") == 0:
            os.mkdir("dictionaries/random/")
        dire = "dictionaries/random/"

        files_to_download = {
            "Ethnologue.gz",
            "abbr.gz",
            "chars.gz",
            "dogs.gz",
            "drugs.gz",
            "junk.gz",
            "numbers.gz",
            "phrases.gz",
            "sports.gz",
            "statistics.gz",
        }

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "30":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("religion")
        if os.path.isdir("dictionaries/religion/") == 0:
            os.mkdir("dictionaries/religion/")
        dire = "dictionaries/religion/"

        files_to_download = {"Koran.gz", "kjbible.gz", "norse.gz"}

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "31":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("russian")
        if os.path.isdir("dictionaries/russian/") == 0:
            os.mkdir("dictionaries/russian/")
        dire = "dictionaries/russian/"

        retr_binary_file(ftp, dire, "russian.lst.gz")
        retr_binary_file(ftp, dire, "russian_words.koi8.gz")

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "32":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("science")
        if os.path.isdir("dictionaries/science/") == 0:
            os.mkdir("dictionaries/science/")
        dire = "dictionaries/science/"

        files_to_download = {
            "Acr-diagnosis.gz",
            "Algae.gz",
            "Bacteria.gz",
            "Fungi.gz",
            "Microalgae.gz",
            "Viruses.gz",
            "asteroids.gz",
            "biology.gz",
            "tech.gz",
        }

        # download the files
        retr_file_list(ftp, dire, files_to_download)

        print("[+] files saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "33":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("spanish")
        if os.path.isdir("dictionaries/spanish/") == 0:
            os.mkdir("dictionaries/spanish/")
        dire = "dictionaries/spanish/"

        retr_binary_file(ftp, dire, "words.spanish.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "34":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("swahili")
        if os.path.isdir("dictionaries/swahili/") == 0:
            os.mkdir("dictionaries/swahili/")
        dire = "dictionaries/swahili/"

        retr_binary_file(ftp, dire, "swahili.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "35":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("swedish")
        if os.path.isdir("dictionaries/swedish/") == 0:
            os.mkdir("dictionaries/swedish/")
        dire = "dictionaries/swedish/"

        retr_binary_file(ftp, dire, "words.swedish.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "36":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("turkish")
        if os.path.isdir("dictionaries/turkish/") == 0:
            os.mkdir("dictionaries/turkish/")
        dire = "dictionaries/turkish/"

        retr_binary_file(ftp, dire, "turkish.dict.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    elif filedown == "37":
        print("[+] connecting...")
        ftp = ftplib.FTP(ftpurl)
        downloader()
        ftp.cwd("yiddish")
        if os.path.isdir("dictionaries/yiddish/") == 0:
            os.mkdir("dictionaries/yiddish/")
        dire = "dictionaries/yiddish/"

        retr_binary_file(ftp, dire, "yiddish.gz")

        print("[+] file saved to " + dire)
        ftp.quit()
        exit()

    else:
        print("[-] leaving.")
        exit()


else:
    print("\r\n[Usage]:	" + sys.argv[0] + "  [OPTIONS] \r\n")
    print("[Help]:		" + sys.argv[0] + "  -h\r\n")
    exit()
