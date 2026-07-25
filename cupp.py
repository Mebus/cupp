#!/usr/bin/python3
#
#  [Program]
#
#  CUPP
#  Common User Passwords Profiler
#
#  [Author]
#
#  Muris Kurgas aka j0rgan
#  j0rgan [at] remote-exploit [dot] org
#  http://www.remote-exploit.org
#  http://www.azuzi.me
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
import os
import sys

# Importing our custom Modular Architecture files
import generator
import downloader

__author__ = "Mebus"
__license__ = "GPL"
__version__ = "3.4.1-Ultimate (Modular)"

def read_config(filename):
    """Read the given configuration file and return global configs."""
    config = configparser.ConfigParser()
    if os.path.isfile(filename):
        config.read(filename)
    else:
        print("[-] Configuration file " + filename + " not found! Using default safe values.")

    # Using fallback values so it NEVER crashes
    config_global = {
        "years": config.get("years", "years", fallback="2020,2021,2022,2023,2024,2025,2026").split(","),
        "chars": config.get("specialchars", "chars", raw=True, fallback="!,@,#,$,%,&,*,-,_,+,=").split(","),
        "numfrom": config.getint("nums", "from", fallback=0),
        "numto": config.getint("nums", "to", fallback=100),
        "wcfrom": config.getint("nums", "wcfrom", fallback=5),
        "wcto": config.getint("nums", "wcto", fallback=12),
        "threshold": config.getint("nums", "threshold", fallback=80000),
        "alectourl": config.get("alecto", "alectourl", fallback="https://raw.githubusercontent.com/Mebus/cupp/master/alectodb.csv.gz"),
        "dicturl": config.get("downloader", "dicturl", fallback="http://ftp.funet.fi/pub/doc/dictionaries/"),
    }

    # 1337 mode configs
    config_leet = {}
    letters = {"a", "i", "e", "t", "o", "s", "g", "z"}
    default_leet = {"a": "4", "i": "1", "e": "3", "t": "7", "o": "0", "s": "5", "g": "9", "z": "2"}

    for letter in letters:
        config_leet[letter] = config.get("leet", letter, fallback=default_leet[letter])

    return config_global, config_leet


def print_cow():
    print(" ___________ ")
    print(" \033[07m  cupp.py! \033[27m                # \033[07mC\033[27mommon")
    print("      \\                     # \033[07mU\033[27mser")
    print("       \\   \033[1;31m,__,\033[1;m             # \033[07mP\033[27masswords")
    print("        \\  \033[1;31m(\033[1;moo\033[1;31m)____\033[1;m         # \033[07mP\033[27mrofiler")
    print("           \033[1;31m(__)    )\\ \033[1;m  ")
    print("           \033[1;31m   ||--|| \033[1;m\033[05m*\033[25m\033[1;m       [ Muris Kurgas | j0rgan@remote-exploit.org ]")
    print("                            [ Mebus | https://github.com/Mebus/]\r\n")

def version():
    """Display version"""
    print("\r\n	\033[1;31m[ cupp.py ]  " + __version__ + "\033[1;m\r\n")
    print("	* Hacked up by j0rgan - j0rgan@remote-exploit.org")
    print("	* http://www.remote-exploit.org\r\n")
    print("	\033[1;32m[ Modern Enhancements ]\033[1;m")
    print("	* Modular Architecture (cupp, generator, downloader)")
    print("	* Generator-based O(1) Memory Optimization")
    print("	* Secure Networking & Fast I/O Streaming")
    print("	* Enhanced OSINT Interactive Profiling\r\n")
    print("	Take a look ./README.md file for more info about the program\r\n")

def get_parser():
    """Create and return a parser for main() to use"""
    parser = argparse.ArgumentParser(description="Common User Passwords Profiler (Modernized/Optimized Edition)")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-i", "--interactive", action="store_true", help="Interactive questions for user password profiling"
    )
    group.add_argument(
        "-w", dest="improve", metavar="FILENAME", help="Use this option to improve existing dictionary, or WyD.pl output to make some pwnsauce"
    )
    group.add_argument(
        "-l", dest="download_wordlist", action="store_true", help="Download huge wordlists from repository"
    )
    group.add_argument(
        "-a", dest="alecto", action="store_true", help="Parse default usernames and passwords directly from Alecto DB."
    )
    group.add_argument(
        "-v", "--version", action="store_true", help="Show the version of this program."
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Quiet mode (don't print banner)"
    )
    return parser

def main():
    """Command-line interface to the cupp utility"""
    parser = get_parser()
    args = parser.parse_args()

    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cupp.cfg")
    config_global, config_leet = read_config(config_path)

    if not args.quiet:
        print_cow()

    if args.version:
        version()
    elif args.interactive:
        generator.interactive(config_global, config_leet)
    elif args.download_wordlist:
        downloader.download_wordlist(config_global)
    elif args.alecto:
        downloader.alectodb_download(config_global)
    elif args.improve:
        generator.improve_dictionary(args.improve, config_global, config_leet)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()