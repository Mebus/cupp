#  [Program]
#
#  CUPP
#  Common User Passwords Profiler
#
#  [Author]
#
#  AndreasInfo
#  https://github.com/AndreasInfo
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
#  See 'LICENSE' for more information.

import argparse
import configparser
import csv
import gzip
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import time
import itertools

__author__ = "AndreasInfo"
__license__ = "GPL"
__version__ = "3.4.0"

CONFIG = {}


def read_config(filename: str):
    """Read the given configuration file and update global variable CONFIG to
    reflect changes."""

    if not os.path.isfile(filename):
        sys.exit(f"Configuration file {filename} not found!. Exiting.")

    config = configparser.ConfigParser()
    config.read(filename)

    CONFIG["global"] = {
        "years": config.get("years", "years").split(","),
        "spechars": config.get("specialchars", "specialchars").split(","),
        "numfrom": config.getint("nums", "from"),
        "numto": config.getint("nums", "to"),
        "wcfrom": config.getint("nums", "wcfrom"),
        "wcto": config.getint("nums", "wcto"),
        "threshold": config.getint("nums", "threshold"),
        "alectourl": config.get("alecto", "alectourl"),
        "dicturl": config.get("downloader", "dicturl"),
    }

    alphabet = config.get("leet", "alphabet")

    leet_dict = {}
    for pair in alphabet.split(","):
        item = pair.split("-")
        leet_dict[item[0]] = item[1]

    CONFIG["leet"] = leet_dict

    return True

def remove_words(input: list, lower: int, upper: int) -> list:
    """Removes words from input with wrong length."""
    return [x for x in input if len(x) < upper and len(x) > lower]


def make_leet(input: str):
    """Convert input to leet."""
    for letter, leetletter in CONFIG["leet"].items():
        input = input.replace(letter, leetletter)
    return input


def add_randnum(input: list, start: int, stop: int):
    """Adds numbers within range to items of input."""
    for str1 in input:
        for num in range(start, stop):
            yield str1 + str(num)


def calc_list_product(input: list, length: int) -> list:
    """Calculate cartesian product of input."""
    result = []
    for x in range(length):
        result += [
            "".join(combination)
            for combination in itertools.product(input, repeat=x + 1)
        ]
    result = list(set(result))
    result.sort()
    return result


def calc_list_permutation(input: list, length: int) -> list:
    """Calculate permutation of input."""
    result = []
    for x in range(length):
        result += [
            "".join(combination)
            for combination in itertools.permutations(input, r=x + 1)
        ]
    result = list(set(result))
    result.sort()
    return result


def combine_lists(input1: list, input2: list, separator: list = [""]):
    """Appends items of input2 to items of input1"""
    for sep in separator:
        for str1 in input1:
            for str2 in input2:
                yield str1 + sep + str2

def decompose_birthdates(birthdates: list) -> list:
    """Disassemble birthdates to get individual parts."""
    result = []

    for birthdate in birthdates:
        result.append(birthdate[-2:])  # yy
        result.append(birthdate[-3:])  # yyy
        result.append(birthdate[-4:])  # yyyy
        result.append(birthdate[1:2])  # xd
        result.append(birthdate[3:4])  # xm
        result.append(birthdate[:2])  # dd
        result.append(birthdate[2:4])  # mm

    return result

def transform_items(input: list) -> list:
    names = input
    up = [str(name).title() for name in input]
    rev = [str(name)[::-1] for name in input]
    rev_up = [str(name)[::-1] for name in up]
    return names + up + rev + rev_up

def validate_birthdates(dates: list) -> bool:
    for date in dates:
        if len(date) != 0 and len(date) != 8:
            return False
    return True

def print_to_file(filename, unique_list_finished):
    f = open(filename, "w")
    unique_list_finished.sort()
    f.write(os.linesep.join(unique_list_finished))
    f.close()
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
    inspect = input("> Hyperspeed print? (Y/n) : ").lower()
    if inspect == "y":
        try:
            with open(filename, "r+") as wlist:
                data = wlist.readlines()
                for line in data:
                    print("\033[1;32m[" + filename + "] \033[1;33m" + line)
                    time.sleep(0000.1)
                    os.system("clear")
        except Exception as e:
            print("[ERROR]: " + str(e))
    else:
        pass

    print(
        "[+] Now load your pistolero with \033[1;31m"
        + filename
        + "\033[1;m and shoot! Good luck!"
    )


def print_cow():
    print(" ___________ ")
    print(" \033[07m  cupp.py! \033[27m                # \033[07mC\033[27mommon")
    print("      \                     # \033[07mU\033[27mser")
    print("       \   \033[1;31m,__,\033[1;m             # \033[07mP\033[27masswords")
    print(
        "        \  \033[1;31m(\033[1;moo\033[1;31m)____\033[1;m         # \033[07mP\033[27mrofiler"
    )
    print("           \033[1;31m(__)    )\ \033[1;m  ")
    print(
        "           \033[1;31m   ||--|| \033[1;m\033[05m*\033[25m\033[1;m      [ Muris Kurgas | j0rgan@remote-exploit.org ]"
    )
    print(28 * " " + "[ Mebus | https://github.com/Mebus/]\r\n")


def version():
    """Display version"""

    print("\r\n	\033[1;31m[ cupp.py ]  " + __version__ + "\033[1;m\r\n")
    print("	* Hacked up by j0rgan - j0rgan@remote-exploit.org")
    print("	* http://www.remote-exploit.org\r\n")
    print("	Take a look ./README.md file for more info about the program\r\n")


def improve_dictionary(file_to_open):
    """Implementation of the -w option. Improve a dictionary by
    interactively questioning the user."""

    kombinacija = {}
    komb_unique = {}

    if not os.path.isfile(file_to_open):
        exit("Error: file " + file_to_open + " does not exist.")

    spechars = CONFIG["global"]["spechars"]
    years = CONFIG["global"]["years"]
    numfrom = CONFIG["global"]["numfrom"]
    numto = CONFIG["global"]["numto"]

    fajl = open(file_to_open, "r")
    listic = fajl.readlines()
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

    if conts == "y" and len(listic) > CONFIG["global"]["threshold"]:
        print(
            "\r\n[-] Maximum number of words for concatenation is "
            + str(CONFIG["global"]["threshold"])
        )
        print("[-] Check configuration file for increasing this number.\r\n")
        conts = input(
            "> Do you want to concatenate all words from wordlist? Y/[N]: "
        ).lower()

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
        for spec1 in spechars:
            spechars.append(spec1)
            for spec2 in spechars:
                spechars.append(spec1 + spec2)
                for spec3 in spechars:
                    spechars.append(spec1 + spec2 + spec3)

    randnum = input(
        "> Do you want to add some random numbers at the end of words? Y/[N]:"
    ).lower()
    leetmode = input("> Leet mode? (i.e. leet = 1337) Y/[N]: ").lower()

    # init
    for i in range(6):
        kombinacija[i] = [""]

    kombinacija[0] = list(combine_lists(listica, years))
    if conts == "y":
        kombinacija[1] = list(combine_lists(cont, years))
    if spechars1 == "y":
        kombinacija[2] = list(combine_lists(listica, spechars))
        if conts == "y":
            kombinacija[3] = list(combine_lists(cont, spechars))
    if randnum == "y":
        kombinacija[4] = list(add_randnum(listica, numfrom, numto))
        if conts == "y":
            kombinacija[5] = list(add_randnum(cont, numfrom, numto))

    print("\r\n[+] Now making a dictionary...")

    print("[+] Sorting list and removing duplicates...")

    for i in range(6):
        komb_unique[i] = list(dict.fromkeys(kombinacija[i]).keys())

    komb_unique[6] = list(dict.fromkeys(listica).keys())
    komb_unique[7] = list(dict.fromkeys(cont).keys())

    # join the lists
    uniqlist = []
    for i in range(8):
        uniqlist += komb_unique[i]

    unique_lista = list(dict.fromkeys(uniqlist).keys())
    unique_leet = []
    if leetmode == "y":
        for (
            x
        ) in (
            unique_lista
        ):  # if you want to add more leet chars, you will need to add more lines in cupp.cfg too...
            x = make_leet(x)  # convert to leet
            unique_leet.append(x)

    unique_list = unique_lista + unique_leet

    unique_list_finished = []

    unique_list_finished = [
        x
        for x in unique_list
        if len(x) > CONFIG["global"]["wcfrom"] and len(x) < CONFIG["global"]["wcto"]
    ]

    print_to_file(file_to_open + ".cupp.txt", unique_list_finished)

    fajl.close()


def interactive():
    """
    Implementation of the -i switch. Interactively question the user and
    create a password dictionary file based on the answer.
    """

    print("\r\n[+] Insert the information about the victim to make a dictionary")
    print("[+] If you don't know all the info, just hit enter when asked! ;)\r\n")

    profile = {}

    msg = "> Names (first-, last-, nick-...), comma-separated, spaces will be removed: "
    names = input(msg).lower().replace(" ", "").split(",")
    while len(names) == 0:
        print("\r\n[-] You must enter a name at least!")
        names = input("> Names: ").lower()
    profile["names"] = names

    msg = "> Birthdate (DDMMYYYY): "
    birthdate = input(msg).replace(" ", "").split(",")
    while not validate_birthdates(birthdate):
        print("\r\n[-] You must enter 8 digits for birthday!")
        birthdate = input("> Birthdate (DDMMYYYY): ")
    profile["birthdate"] = birthdate

    print("\r\n")

    msg = "> Partners' names (first-, last-, nick-...), comma-separated, spaces will be removed: "
    profile["wife_names"] = input(msg).lower().replace(" ", "").split(",")

    msg = "> Partner's birthdate (DDMMYYYY): "
    wife_birthdate = input(msg).replace(" ", "").split(",")
    while not validate_birthdates(wife_birthdate):
        print("\r\n[-] You must enter 8 digits for birthday!")
        wife_birthdate = input("> Partner's birthdate (DDMMYYYY): ")
    profile["wife_birthdate"] = wife_birthdate
    print("\r\n")

    msg = "> Childrens' names (first-, last-, nick-...), comma-separated, spaces will be removed: "
    profile["kids_names"] = input().lower().replace(" ", "").split(",")
    
    msg = "> Childrens' birthdates (DDMMYYYY), comma-separated, spaces will be removed: "
    kid_birthdates = input(msg).replace(" ", "").split(",")
    while not validate_birthdates(kid_birthdates):
        print("\r\n[-] You must enter 8 digits for birthday!")
        kid_birthdates = input("> Childrens' birthdates (DDMMYYYY): ")
    profile["kids_birthdates"] = kid_birthdates
    print("\r\n")

    msg = "> Pets' names, comma-separated, spaces will be removed: "
    profile["pets_names"] = input(msg).lower().replace(" ", "").split(",")

    msg = "> Companies' names, comma-separated, spaces will be removed: "
    profile["companies"] = input(msg).lower().replace(" ", "").split(",")
    print("\r\n")

    profile["words"] = [""]
    words1 = input(
        "> Do you want to add some key words about the victim? Y/[N]: "
    ).lower()
    words2 = ""
    if words1 == "y":
        words2 = input(
            "> Please enter the words, comma-separated, spaces will be removed: "
        ).replace(" ", "")
    profile["words"] = words2.split(",")

    profile["spechars_switch"] = input(
        "> Do you want to add special chars at the end of words? Y/[N]: "
    ).lower()

    profile["randnum_switch"] = input(
        "> Do you want to add some random numbers at the end of words? Y/[N]:"
    ).lower()
    profile["leetmode_switch"] = input("> Leet mode? (i.e. leet = 1337) Y/[N]: ").lower()

    generate_wordlist_from_profile(profile)


def generate_wordlist_from_profile(profile: dict):
    """
    Generates a wordlist from a given profile
    """

    spechars = CONFIG["global"]["spechars"]
    years = CONFIG["global"]["years"]
    numfrom = CONFIG["global"]["numfrom"]
    numto = CONFIG["global"]["numto"]

    profile["spechars"] = []
    if profile["spechars_switch"] == "y":
        profile["spechars"] = calc_list_product(spechars, 3)

    print("\r\n[+] Now making a dictionary...")

    target_bd = decompose_birthdates(profile["birthdate"])
    wife_bd = decompose_birthdates(profile["wife_birthdate"])
    kid_bd = decompose_birthdates(profile["kids_birthdates"])

    target = transform_items(profile["names"])
    wife = transform_items(profile["wife_names"])
    kids = transform_items(profile["kids_names"])
    pets = transform_items(profile["pets_names"])
    companies = transform_items(profile["companies"])
    words = transform_items(profile["words"])

    # Combinations
    target_kombi = calc_list_product(target, 2)
    wife_kombi = calc_list_product(wife, 2)
    kids_kombi = calc_list_product(kids, 2)
    all_kombi = target_kombi + wife_kombi + kids_kombi

    rest_kombi = pets + companies + words

    target_bd_kombi = calc_list_permutation(target_bd, 3)
    wife_bd_kombi = calc_list_permutation(wife_bd, 3)
    kids_bds_kombi = calc_list_permutation(kid_bd, 3)
    all_kombi_bds = target_bd_kombi + wife_bd_kombi + kids_bds_kombi

    kombi = []
    kombi += all_kombi
    kombi += rest_kombi
    kombi += all_kombi_bds
    # birthdate
    kombi += combine_lists(target_kombi, target_bd_kombi, ["", "_"])
    kombi += combine_lists(wife_kombi, wife_bd_kombi, ["", "_"])
    kombi += combine_lists(kids_kombi, kids_bds_kombi, ["", "_"])
    kombi += combine_lists(rest_kombi, all_kombi_bds, ["", "_"])
    # years
    kombi += combine_lists(all_kombi, years, ["", "_"])
    kombi += combine_lists(rest_kombi, years, ["", "_"])
    # random number
    if profile["randnum_switch"] == "y":
        kombi += add_randnum(all_kombi, numfrom, numto)
        kombi += add_randnum(rest_kombi, numfrom, numto)
    # special chars
    if len(profile["spechars"]) > 0:
        kombi += combine_lists(all_kombi, profile["spechars"])
        kombi += combine_lists(rest_kombi, profile["spechars"])

    print("[+] Sorting list and removing duplicates...")

    kombi = list(set(kombi))

    leet = []
    if profile["leetmode_switch"] == "y":
        for item in kombi:
            result = make_leet(item)
            if result != item:
                leet.append(result)

    unique_list = kombi + leet

    lower = CONFIG["global"]["wcfrom"]
    upper = CONFIG["global"]["wcto"]
    result = remove_words(unique_list, lower, upper)

    print_to_file(target[0] + ".txt", result)


def download_http(url, targetfile):
    print("[+] Downloading " + targetfile + " from " + url + " ... ")
    webFile = urllib.request.urlopen(url)
    localFile = open(targetfile, "wb")
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()


def alectodb_download():
    """Download csv from alectodb and save into local file as a list of
    usernames and passwords"""

    url = CONFIG["global"]["alectourl"]

    print("\r\n[+] Checking if alectodb is not present...")

    targetfile = "alectodb.csv.gz"

    if not os.path.isfile(targetfile):

        download_http(url, targetfile)

    f = gzip.open(targetfile, "rt")

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


def download_wordlist():
    """Implementation of -l switch. Download wordlists from http repository as
    defined in the configuration file."""

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
    print(
        "	\r\n	Files will be downloaded from "
        + CONFIG["global"]["dicturl"]
        + " repository"
    )
    print(
        "	\r\n	Tip: After downloading wordlist, you can improve it with -w option\r\n"
    )

    filedown = input("> Enter number: ")
    filedown.isdigit()
    while filedown.isdigit() == 0:
        print("\r\n[-] Wrong choice. ")
        filedown = input("> Enter number: ")
    filedown = str(filedown)
    while int(filedown) > 38 or int(filedown) < 0:
        print("\r\n[-] Wrong choice. ")
        filedown = input("> Enter number: ")
    filedown = str(filedown)

    download_wordlist_http(filedown)
    return filedown


def download_wordlist_http(filedown):
    """ do the HTTP download of a wordlist """

    mkdir_if_not_exists("dictionaries")

    # List of files to download:
    arguments = {
        1: (
            "Moby",
            (
                "mhyph.tar.gz",
                "mlang.tar.gz",
                "moby.tar.gz",
                "mpos.tar.gz",
                "mpron.tar.gz",
                "mthes.tar.gz",
                "mwords.tar.gz",
            ),
        ),
        2: ("afrikaans", ("afr_dbf.zip",)),
        3: ("american", ("dic-0294.tar.gz",)),
        4: ("aussie", ("oz.gz",)),
        5: ("chinese", ("chinese.gz",)),
        6: (
            "computer",
            (
                "Domains.gz",
                "Dosref.gz",
                "Ftpsites.gz",
                "Jargon.gz",
                "common-passwords.txt.gz",
                "etc-hosts.gz",
                "foldoc.gz",
                "language-list.gz",
                "unix.gz",
            ),
        ),
        7: ("croatian", ("croatian.gz",)),
        8: ("czech", ("czech-wordlist-ascii-cstug-novak.gz",)),
        9: ("danish", ("danish.words.gz", "dansk.zip")),
        10: (
            "databases",
            ("acronyms.gz", "att800.gz", "computer-companies.gz", "world_heritage.gz"),
        ),
        11: (
            "dictionaries",
            (
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
            ),
        ),
        12: ("dutch", ("words.dutch.gz",)),
        13: (
            "finnish",
            ("finnish.gz", "firstnames.finnish.gz", "words.finnish.FAQ.gz"),
        ),
        14: ("french", ("dico.gz",)),
        15: ("german", ("deutsch.dic.gz", "germanl.gz", "words.german.gz")),
        16: ("hindi", ("hindu-names.gz",)),
        17: ("hungarian", ("hungarian.gz",)),
        18: ("italian", ("words.italian.gz",)),
        19: ("japanese", ("words.japanese.gz",)),
        20: ("latin", ("wordlist.aug.gz",)),
        21: (
            "literature",
            (
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
            ),
        ),
        22: ("movieTV", ("Movies.gz", "Python.gz", "Trek.gz")),
        23: (
            "music",
            (
                "music-classical.gz",
                "music-country.gz",
                "music-jazz.gz",
                "music-other.gz",
                "music-rock.gz",
                "music-shows.gz",
                "rock-groups.gz",
            ),
        ),
        24: (
            "names",
            (
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
            ),
        ),
        25: (
            "net",
            (
                "hosts-txt.gz",
                "inet-machines.gz",
                "usenet-loginids.gz",
                "usenet-machines.gz",
                "uunet-sites.gz",
            ),
        ),
        26: ("norwegian", ("words.norwegian.gz",)),
        27: (
            "places",
            (
                "Colleges.gz",
                "US-counties.gz",
                "World.factbook.gz",
                "Zipcodes.gz",
                "places.gz",
            ),
        ),
        28: ("polish", ("words.polish.gz",)),
        29: (
            "random",
            (
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
            ),
        ),
        30: ("religion", ("Koran.gz", "kjbible.gz", "norse.gz")),
        31: ("russian", ("russian.lst.gz", "russian_words.koi8.gz")),
        32: (
            "science",
            (
                "Acr-diagnosis.gz",
                "Algae.gz",
                "Bacteria.gz",
                "Fungi.gz",
                "Microalgae.gz",
                "Viruses.gz",
                "asteroids.gz",
                "biology.gz",
                "tech.gz",
            ),
        ),
        33: ("spanish", ("words.spanish.gz",)),
        34: ("swahili", ("swahili.gz",)),
        35: ("swedish", ("words.swedish.gz",)),
        36: ("turkish", ("turkish.dict.gz",)),
        37: ("yiddish", ("yiddish.gz",)),
    }

    # download the files

    intfiledown = int(filedown)

    if intfiledown in arguments:

        dire = "dictionaries/" + arguments[intfiledown][0] + "/"
        mkdir_if_not_exists(dire)
        files_to_download = arguments[intfiledown][1]

        for fi in files_to_download:
            url = CONFIG["global"]["dicturl"] + arguments[intfiledown][0] + "/" + fi
            tgt = dire + fi
            download_http(url, tgt)

        print("[+] files saved to " + dire)

    else:
        print("[-] leaving.")


# create the directory if it doesn't exist
def mkdir_if_not_exists(dire):
    if not os.path.isdir(dire):
        os.mkdir(dire)


# the main function
def main():
    """Command-line interface to the cupp utility"""

    read_config(os.path.join(os.path.dirname(os.path.realpath(__file__)), "cupp.cfg"))

    parser = get_parser()
    args = parser.parse_args()

    if not args.quiet:
        print_cow()

    if args.version:
        version()
    elif args.interactive:
        interactive()
    elif args.download_wordlist:
        download_wordlist()
    elif args.alecto:
        alectodb_download()
    elif args.improve:
        improve_dictionary(args.improve)
    else:
        parser.print_help()


# Separate into a function for testing purposes
def get_parser():
    """Create and return a parser (argparse.ArgumentParser instance) for main()
    to use"""
    parser = argparse.ArgumentParser(description="Common User Passwords Profiler")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Interactive questions for user password profiling",
    )
    group.add_argument(
        "-w",
        dest="improve",
        metavar="FILENAME",
        help="Use this option to improve existing dictionary,"
        " or WyD.pl output to make some pwnsauce",
    )
    group.add_argument(
        "-l",
        dest="download_wordlist",
        action="store_true",
        help="Download huge wordlists from repository",
    )
    group.add_argument(
        "-a",
        dest="alecto",
        action="store_true",
        help="Parse default usernames and passwords directly"
        " from Alecto DB. Project Alecto uses purified"
        " databases of Phenoelit and CIRT which were merged"
        " and enhanced",
    )
    group.add_argument(
        "-v", "--version", action="store_true", help="Show the version of this program."
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Quiet mode (don't print banner)"
    )

    return parser


if __name__ == "__main__":
    main()
