import os

class Generator():

    # print list to file counting words
    def print_to_file(self, filename, unique_list_finished):
        f = open(filename, "w")
        f.write(os.linesep.join(unique_list_finished))
        f.close()
        lines = len(unique_list_finished)
        # f = open(filename, "r")
        # lines = 0
        # for line in f:
        #     lines += 1
        # f.close()
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

    def make_leet(self, x, CONFIG):
        """convert string to leet"""
        for letter, leetletter in CONFIG["LEET"].items():
            x = x.replace(letter, leetletter)
        return x

    # for concatenations...
    def concats(self, seq, start, stop):
        final= []
        for array in seq:
            for word in array:
                for num in range(start, stop):
                    final.append(word + str(num))
        return final

    def reduce_array(self, array):
        return list(set(array))

    def compare_and_reduce(self, array1, array2):
        inter = set(array1).intersection(array2)
        for i in inter:
            array1.remove(i)
        return array1

    def birthdays_combinations(self, array):
        new_array = []
        for bds1 in array:
            new_array.append(bds1)
        for bds2 in array:
            if array.index(bds1) != array.index(bds2):
                new_array.append(bds1 + bds2)
                for bds3 in array:
                    if (
                        array.index(bds1) != array.index(bds2)
                        and array.index(bds2) != array.index(bds3)
                        and array.index(bds1) != array.index(bds3)
                    ):
                        new_array.append(bds1 + bds2 + bds3)
        return new_array

    def combine(self, first, second):
        all = []
        for word1 in first:
            for word2 in second:
                all.append(word1+word2)
                all.append(word1+"_"+word2)
        return all

    def names_combinations(self, names):
        combinations = []
        for kombina1 in names:
            combinations.append(kombina1)
            for kombina2 in names:
                if names.index(kombina1) != names.index(kombina2) and names.index(
                    kombina1.title()
                ) != names.index(kombina2.title()):
                    combinations.append(kombina1 + kombina2)
        return combinations

    def generate_wordlist_from_profile(self, profile, CONFIG):
        """ Generates a wordlist from a given profile """

        chars = CONFIG["global"]["chars"]
        years = CONFIG["global"]["years"]
        numfrom = CONFIG["global"]["numfrom"]
        numto = CONFIG["global"]["numto"]

        profile["spechars"] = []

        if profile["spechars1"] == "y":
            for spec1 in chars:
                profile["spechars"].append(spec1)
                for spec2 in chars:
                    profile["spechars"].append(spec1 + spec2)
                    for spec3 in chars:
                        profile["spechars"].append(spec1 + spec2 + spec3)

        print("\r\n[+] Now making a dictionary...")

        # Now me must do some string modifications...

        # Some array definitions

        # Birthdays first
        bds = [
            profile["birthdate"][-2:],
            profile["birthdate"][-3:],
            profile["birthdate"][-4:],
            profile["birthdate"][1:2],
            profile["birthdate"][3:4],
            profile["birthdate"][:2],
            profile["birthdate"][2:4]
        ]

        wbds = [
            profile["wifeb"][-2:],
            profile["wifeb"][-3:],
            profile["wifeb"][-4:],
            profile["wifeb"][1:2],
            profile["wifeb"][3:4],
            profile["wifeb"][:2],
            profile["wifeb"][2:4]
        ]

        kbds = [
            profile["kidb"][-2:],
            profile["kidb"][-3:],
            profile["kidb"][-4:],
            profile["kidb"][1:2],
            profile["kidb"][3:4],
            profile["kidb"][:2],
            profile["kidb"][2:4]
        ]

        # Convert first letters to uppercase...

        nameup = profile["name"].title()
        surnameup = profile["surname"].title()
        nickup = profile["nick"].title()
        wifeup = profile["wife"].title()
        wifenup = profile["wifen"].title()
        kidup = profile["kid"].title()
        kidnup = profile["kidn"].title()


        # reverse a name
        reverse_names = [
            profile["name"][::-1],
            nameup[::-1],
            profile["nick"][::-1],
            nickup[::-1],
            profile["wife"][::-1],
            wifeup[::-1],
            profile["kid"][::-1],
            kidup[::-1],
        ]

        # string combinations....

        names_comp_pet = [
            profile["pet"],
            profile["pet"].title(),
            profile["company"],
            profile["company"].title()
        ]

        kombina = [
            profile["name"],
            profile["surname"],
            profile["nick"],
            nameup,
            surnameup,
            nickup,
        ]

        kombinaw = [
            profile["wife"],
            profile["wifen"],
            wifeup,
            wifenup,
            profile["surname"],
            surnameup,
        ]

        kombinak = [
            profile["kid"],
            profile["kidn"],
            kidup,
            kidnup,
            profile["surname"],
            surnameup,
        ]

        wordsup = []
        wordsup = list(map(str.title, profile["words"]))
        additional_words = profile["words"] + wordsup

        # Birthdays combinations
        birthdays = self.birthdays_combinations(bds)
        wbirthdays = self.birthdays_combinations(wbds) # For a woman...
        kbirthdays = self.birthdays_combinations(kbds) # and a child...

        # Names combinations
        names = self.names_combinations(kombina)
        names_wife = self.names_combinations(kombinaw)
        names_kid = self.names_combinations(kombinak)

        # Let's do some serious work! This will be a mess of code, but... who cares? :)
        first = []
        first += names
        first += names_wife
        first += names_kid
        first += names_comp_pet
        first += additional_words
        first += reverse_names
        if profile["randnum"] == "y":
            first += self.concats(first, numfrom, numto)

        second = []
        second += birthdays
        second += wbirthdays
        second += kbirthdays
        second += years
        if len(profile["spechars"]) > 0:
            second += self.combine(second, profile["spechars"])

        print("[+] Sorting list and removing duplicates...")

        first = self.reduce_array(first)
        second = self.reduce_array(second)
        first = self.compare_and_reduce(first, second)
        # first = first.sort()
        # second = second.sort()

        print("[+] Combining...")
        combinations = []
        combinations = self.combine(first, second)
        combinations += first
        combinations += second

        leet = []
        if profile["leetmode"] == "y":
            for word in combinations:  # if you want to add more leet chars, you will need to add more lines in cupp.cfg too...
                leet_word = self.make_leet(word, CONFIG)  # convert to leet
                leet.append(leet_word)

        combinations += leet

        unique_list = []
        unique_list = [
            x
            for x in combinations
            if len(x) < CONFIG["global"]["wcto"] and len(x) > CONFIG["global"]["wcfrom"]
        ]
        return unique_list

    def __init__(self, profile, CONFIG):
        self.print_to_file(profile["name"] + ".txt", self.generate_wordlist_from_profile(profile, CONFIG))