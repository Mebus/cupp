#!/usr/bin/env python3
#
#  [Program]
#
#  CUPP - Common User Passwords Profiler
#
#  [Author]
#
#  Mebus, https://github.com/Mebus/
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

import os
import unittest

from cupp import *


class TestCupp(unittest.TestCase):
    def setUp(self):

        read_config()

    def test_config(self):

        self.assertIn("2018", CONFIG["global"]["years"], "2018 is in years")

    def test_generate_wordlist_from_profile(self):
        profile = {
            "name": "владимир",
            "surname": "путин",
            "nick": "putin",
            "birthdate": "07101952",
            "wife": "людмила",
            "wifen": "ljudmila",
            "wifeb": "06011958",
            "kid": "екатерина",
            "kidn": "katerina",
            "kidb": "31081986",
            "pet": "werny",
            "company": "russian federation",
            "words": ["Крим"],
            "spechars1": "y",
            "randnum": "y",
            "leetmode": "y",
            "spechars": [],
        }
        read_config()
        generate_wordlist_from_profile(profile)
        pass

    def test_parser(self):
        """ downloads a file and checks if it exists """

        download_wordlist_ftp("31")

        filename = "dictionaries/russian/russian.lst.gz"

        self.assertTrue(os.path.isfile(filename), "file " + filename + "exists")


if __name__ == "__main__":
    unittest.main()
