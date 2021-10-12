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
from unittest.mock import patch

from cupp import *


class TestCupp(unittest.TestCase):
    def setUp(self):

        read_config("cupp.cfg")

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
        read_config("cupp.cfg")
        generate_wordlist_from_profile(profile)

    def test_parser(self):
        """ downloads a file and checks if it exists """

        download_wordlist_http("16")

        filename = "dictionaries/hindi/hindu-names.gz"
        self.assertTrue(os.path.isfile(filename), "file " + filename + "exists")

    def test_print_cow(self):
        """ test the cow """
        print_cow()

    def test_alectodb_download(self):

        alectodb_download()

        self.assertTrue(
            os.path.isfile("alectodb-usernames.txt"),
            "file alectodb-usernames.txt exists",
        )
        self.assertTrue(
            os.path.isfile("alectodb-passwords.txt"),
            "file alectodb-passwords.txt exists",
        )

    def test_improve_dictionary(self):

        filename = "improveme.txt"
        open(filename, "a").write("password123\n2018password\npassword\n")

        __builtins__.input = lambda _: "Y"  # Mock
        improve_dictionary(filename)

    def test_download_wordlist(self):
        """ Download wordlists via menu """
        __builtins__.input = lambda _: "31"  # Mock
        download_wordlist()
        filename = "dictionaries/russian/russian.lst.gz"
        self.assertTrue(os.path.isfile(filename), "file " + filename + "exists")

    def test_interactive(self):
        """ Tests the interactive menu """

        expected_filename = "julian.txt"
        string_to_test = "Julian30771"

        # delete the file if it already exists
        if os.path.isfile(expected_filename):
            os.remove(expected_filename)

        user_input = [
            "Julian",  # First Name
            "Assange",  # Surname
            "Mendax",  # Nickname
            "03071971",  # Birthdate
            "",  # Partner
            "",  # Partner nick
            "",  # Partner birthdate
            "",  # Child name
            "",  # Child nick
            "",  # Child birthdate
            "",  # Pet's name
            "",  # Company name
            "N",  # keywords
            "Y",  # Special chars
            "N",  # Random
            "N",  # Leet mode
        ]

        test_ok = False

        with patch("builtins.input", side_effect=user_input):
            stacks = interactive()

        if os.path.isfile(expected_filename):
            if string_to_test in open(expected_filename).read():
                test_ok = True

        self.assertTrue(test_ok, "interactive generation works")

    def test_make_leet(self):
        """ test the make leet function """
        test_data = [
            ("", []),
            ("q", []),
            ("äö~#-_:_:", []),
            ("0123456789", []),
            ("!§$%&()=", []),
            ("²³`´énµ€@", []),
            ("a", ["4"]),
            ("aa", ["a4", "4a", "44"]),
            ("aaa", ["aa4", "a4a", "a44", "4aa", "4a4", "44a", "444"]),
            ("aietosgz", [
                "aietosg2", "aietos9z", "aietos92", "aieto5gz", "aieto5g2", "aieto59z", "aieto592", "aiet0sgz",
                "aiet0sg2", "aiet0s9z", "aiet0s92", "aiet05gz", "aiet05g2", "aiet059z", "aiet0592", "aie7osgz",
                "aie7osg2", "aie7os9z", "aie7os92", "aie7o5gz", "aie7o5g2", "aie7o59z", "aie7o592", "aie70sgz",
                "aie70sg2", "aie70s9z", "aie70s92", "aie705gz", "aie705g2", "aie7059z", "aie70592", "ai3tosgz",
                "ai3tosg2", "ai3tos9z", "ai3tos92", "ai3to5gz", "ai3to5g2", "ai3to59z", "ai3to592", "ai3t0sgz",
                "ai3t0sg2", "ai3t0s9z", "ai3t0s92", "ai3t05gz", "ai3t05g2", "ai3t059z", "ai3t0592", "ai37osgz",
                "ai37osg2", "ai37os9z", "ai37os92", "ai37o5gz", "ai37o5g2", "ai37o59z", "ai37o592", "ai370sgz",
                "ai370sg2", "ai370s9z", "ai370s92", "ai3705gz", "ai3705g2", "ai37059z", "ai370592", "a1etosgz",
                "a1etosg2", "a1etos9z", "a1etos92", "a1eto5gz", "a1eto5g2", "a1eto59z", "a1eto592", "a1et0sgz",
                "a1et0sg2", "a1et0s9z", "a1et0s92", "a1et05gz", "a1et05g2", "a1et059z", "a1et0592", "a1e7osgz",
                "a1e7osg2", "a1e7os9z", "a1e7os92", "a1e7o5gz", "a1e7o5g2", "a1e7o59z", "a1e7o592", "a1e70sgz",
                "a1e70sg2", "a1e70s9z", "a1e70s92", "a1e705gz", "a1e705g2", "a1e7059z", "a1e70592", "a13tosgz",
                "a13tosg2", "a13tos9z", "a13tos92", "a13to5gz", "a13to5g2", "a13to59z", "a13to592", "a13t0sgz",
                "a13t0sg2", "a13t0s9z", "a13t0s92", "a13t05gz", "a13t05g2", "a13t059z", "a13t0592", "a137osgz",
                "a137osg2", "a137os9z", "a137os92", "a137o5gz", "a137o5g2", "a137o59z", "a137o592", "a1370sgz",
                "a1370sg2", "a1370s9z", "a1370s92", "a13705gz", "a13705g2", "a137059z", "a1370592", "4ietosgz",
                "4ietosg2", "4ietos9z", "4ietos92", "4ieto5gz", "4ieto5g2", "4ieto59z", "4ieto592", "4iet0sgz",
                "4iet0sg2", "4iet0s9z", "4iet0s92", "4iet05gz", "4iet05g2", "4iet059z", "4iet0592", "4ie7osgz",
                "4ie7osg2", "4ie7os9z", "4ie7os92", "4ie7o5gz", "4ie7o5g2", "4ie7o59z", "4ie7o592", "4ie70sgz",
                "4ie70sg2", "4ie70s9z", "4ie70s92", "4ie705gz", "4ie705g2", "4ie7059z", "4ie70592", "4i3tosgz",
                "4i3tosg2", "4i3tos9z", "4i3tos92", "4i3to5gz", "4i3to5g2", "4i3to59z", "4i3to592", "4i3t0sgz",
                "4i3t0sg2", "4i3t0s9z", "4i3t0s92", "4i3t05gz", "4i3t05g2", "4i3t059z", "4i3t0592", "4i37osgz",
                "4i37osg2", "4i37os9z", "4i37os92", "4i37o5gz", "4i37o5g2", "4i37o59z", "4i37o592", "4i370sgz",
                "4i370sg2", "4i370s9z", "4i370s92", "4i3705gz", "4i3705g2", "4i37059z", "4i370592", "41etosgz",
                "41etosg2", "41etos9z", "41etos92", "41eto5gz", "41eto5g2", "41eto59z", "41eto592", "41et0sgz",
                "41et0sg2", "41et0s9z", "41et0s92", "41et05gz", "41et05g2", "41et059z", "41et0592", "41e7osgz",
                "41e7osg2", "41e7os9z", "41e7os92", "41e7o5gz", "41e7o5g2", "41e7o59z", "41e7o592", "41e70sgz",
                "41e70sg2", "41e70s9z", "41e70s92", "41e705gz", "41e705g2", "41e7059z", "41e70592", "413tosgz",
                "413tosg2", "413tos9z", "413tos92", "413to5gz", "413to5g2", "413to59z", "413to592", "413t0sgz",
                "413t0sg2", "413t0s9z", "413t0s92", "413t05gz", "413t05g2", "413t059z", "413t0592", "4137osgz",
                "4137osg2", "4137os9z", "4137os92", "4137o5gz", "4137o5g2", "4137o59z", "4137o592", "41370sgz",
                "41370sg2", "41370s9z", "41370s92", "413705gz", "413705g2", "4137059z", "41370592"
            ])
        ]
        for data_tuple in test_data:
            output_leet = make_leet(data_tuple[0])
            self.assertEqual(output_leet, data_tuple[1])

    def test_main(self):
        """ test run for the main function """
        main()


if __name__ == "__main__":
    unittest.main()
