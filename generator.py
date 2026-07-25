# generator.py
import os
import time
import itertools

def make_leet(x, config_leet):
    """convert string to leet"""
    for letter, leetletter in config_leet.items():
        x = x.replace(letter, leetletter)
    return x

def stream_processor(stream, min_len, max_len, leetmode, config_leet):
    """ Process items on the fly: deduplicate, length check, and leetmode convert """
    seen = set()
    for item in stream:
        # Check explicit Minimum and Maximum length limits strictly
        if min_len <= len(item) <= max_len:
            if item not in seen:
                seen.add(item)
                yield item
            
            if leetmode == "y":
                leeted = make_leet(item, config_leet)
                if leeted not in seen and min_len <= len(leeted) <= max_len:
                    seen.add(leeted)
                    yield leeted

def print_to_file(filename, iterable_stream, target_volume=0):
    print(f"\r\n[+] Saving dictionary to \033[1;31m{filename}\033[1;m. Processing stream...")
    lines = 0
    start_time = time.time()
    
    with open(filename, "w", encoding="utf-8") as f:
        for word in iterable_stream:
            f.write(word + "\n")
            lines += 1
            # Strictly break when EXACT target volume is reached
            if target_volume > 0 and lines >= target_volume:
                break

    end_time = time.time()
    print(f"[+] Finished! Generated EXACTLY \033[1;32m{lines}\033[1;m pro-level passwords in {round(end_time - start_time, 2)} seconds.")
    
    inspect = input("> Hyperspeed Print? (Y/n) : ").lower()
    if inspect == "y":
        try:
            with open(filename, "r", encoding="utf-8") as wlist:
                for line in wlist:
                    print("\033[1;32m[" + filename + "] \033[1;33m" + line.strip())
                    time.sleep(0.001)
        except Exception as e:
            print("[ERROR]: " + str(e))

    print("[+] Now load your pistolero with \033[1;31m" + filename + "\033[1;m and shoot! Good luck!")

def security_check(filepath):
    print("\n" + "="*55)
    print(" 🛡️  PUBLIC SECURITY CHECK (AWARENESS TOOL)  🛡️ ")
    print("="*55)
    print("Do you want to test if your actual password could be guessed based on the data you provided?")
    choice = input("> Run Security Check? Y/[N]: ").lower().strip()
    
    if choice == 'y':
        test_pw = input("> Enter your actual password to test: ").strip()
        if not test_pw:
            return
            
        print(f"\n[*] Scanning {os.path.basename(filepath)} for your password...")
        time.sleep(1)
        
        found = False
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.strip() == test_pw:
                    found = True
                    break
                    
        if found:
            print("\n\033[1;31m[!] 🚨 CRITICAL WARNING: YOUR PASSWORD WAS SUCCESSFULLY GUESSED! 🚨\033[1;m")
            print("Your password is too predictable and is based entirely on your public OSINT data.")
            print("Action Required: Please update your password immediately using random phrases.")
        else:
            print("\n\033[1;32m[+] ✅ SAFE: Your password was NOT found in the generated dictionary.\033[1;m")
            print("Good job! Your password does not rely purely on obvious personal information.")
    print("="*55 + "\n")

def interactive(config_global, config_leet):
    print("\r\n[+] Insert the information about the victim to make a dictionary")
    print("[+] If you don't know all the info, just hit enter when asked! ;)")

    profile = {}
    
    print("\n\033[1;36m--- Core Info ---\033[1;m")
    name = input("> First Name: ").lower().strip()
    while len(name) == 0:
        print("\r\n[-] You must enter a name at least!")
        name = input("> First Name: ").lower().strip()
    profile["name"] = name

    profile["surname"] = input("> Surname: ").lower().strip()
    profile["nick"] = input("> Nickname: ").lower().strip()
    birthdate = input("> Birthdate (DDMMYYYY): ").strip()
    while len(birthdate) != 0 and len(birthdate) != 8:
        print("\r\n[-] You must enter 8 digits for birthday!")
        birthdate = input("> Birthdate (DDMMYYYY): ").strip()
    profile["birthdate"] = birthdate

    print("\n\033[1;36m--- Digital Footprint [Optional] ---\033[1;m")
    profile["phone_no"] = input("> Victim's Phone Number (e.g., 9876543210): ").strip()
    profile["email"] = input("> Victim's Email ID (e.g., target@gmail.com): ").lower().strip()

    has_family = input("\n> Do you have Family information? Y/[N]: ").lower().strip()
    if has_family == 'y':
        print("\n\033[1;36m--- Family Info [Optional: Press Enter to skip] ---\033[1;m")
        profile["wife"] = input("> Partner's name: ").lower().strip()
        profile["wifen"] = input("> Partner's nickname: ").lower().strip()
        wifeb = input("> Partner's birthdate (DDMMYYYY): ").strip()
        while len(wifeb) != 0 and len(wifeb) != 8:
            print("\r\n[-] You must enter 8 digits for birthday!")
            wifeb = input("> Partner's birthdate (DDMMYYYY): ").strip()
        profile["wifeb"] = wifeb
        print("")
        profile["kid"] = input("> Child's name: ").lower().strip()
        profile["kidn"] = input("> Child's nickname: ").lower().strip()
        kidb = input("> Child's birthdate (DDMMYYYY): ").strip()
        while len(kidb) != 0 and len(kidb) != 8:
            print("\r\n[-] You must enter 8 digits for birthday!")
            kidb = input("> Child's birthdate (DDMMYYYY): ").strip()
        profile["kidb"] = kidb
    else:
        profile["wife"] = profile["wifen"] = profile["wifeb"] = ""
        profile["kid"] = profile["kidn"] = profile["kidb"] = ""

    print("\n\033[1;36m--- Pet/Work Info [Optional: Press Enter to skip] ---\033[1;m")
    profile["pet"] = input("> Pet's name: ").lower().strip()
    profile["company"] = input("> Company name: ").lower().strip()
    
    print("\n\033[1;36m--- 2026 Modern Lifestyle & Tech Info [Optional: Press Enter to skip] ---\033[1;m")
    profile["phone"] = input("> Smartphone/Gadget Model (e.g., iphone15, esp32): ").lower().strip()
    profile["vehicle"] = input("> Dream Bike/Car (e.g., ktm, tesla, thar): ").lower().strip()
    profile["game"] = input("> Favorite Game/Anime (e.g., valorant, naruto, gta6): ").lower().strip()
    profile["crypto"] = input("> Favorite Crypto/Tech (e.g., bitcoin, ai): ").lower().strip()
    profile["sports"] = input("> Favorite Sports Team/Player (e.g., rcb, virat, messi): ").lower().strip()
    profile["bestfriend"] = input("> Best Friend's Name: ").lower().strip()
    
    print("\n\033[1;36m--- Password Length & Advanced Modifiers ---\033[1;m")
    
    min_len = input("> Minimum password length [Default 8]: ").strip()
    profile["min_len"] = int(min_len) if min_len.isdigit() else 8
    
    max_len = input("> Maximum password length [Default 30]: ").strip()
    profile["max_len"] = int(max_len) if max_len.isdigit() else 30

    profile["words"] = []
    words1 = input("\n> Do you want to add custom keywords/numbers (Out of Syllabus)? Y/[N]: ").lower().strip()
    if words1 == "y":
        words2 = input("> Please enter words, separated by comma. [i.e. hacker,1433,KTM]: ").replace(" ", "")
        profile["words"] = [w for w in words2.split(",") if w]

    profile["spechars1"] = input("> Do you want to enable Pro-Level Special Chars combination? [Y]/n: ").lower().strip()
    
    target = input("> Target password volume (e.g., 1000000 for 1 Million) [Press Enter for Auto]: ").strip()
    profile["target_volume"] = int(target) if target.isdigit() else 0

    profile["leetmode"] = input("> Leet mode? (i.e. leet = 1337) Y/[N]: ").lower().strip()

    generate_wordlist_from_profile(profile, config_global, config_leet)


# PRO-LEVEL GENERATOR PIPELINES
def generate_wordlist_from_profile(profile, config_global, config_leet):
    print("\r\n[+] Compiling Pro-Level 3D/4D Generator Pipelines...")
    
    email_user = profile.get("email", "").split('@')[0] if "@" in profile.get("email", "") else profile.get("email", "")
    
    raw_words = [
        profile["name"], profile["surname"], profile["nick"], email_user,
        profile["wife"], profile["wifen"], profile["kid"], profile["kidn"],
        profile["pet"], profile["company"],
        profile.get("phone", ""), profile.get("vehicle", ""),
        profile.get("game", ""), profile.get("crypto", ""),
        profile.get("sports", ""), profile.get("bestfriend", "")
    ] + profile["words"]
    
    base_words = list(set([w for w in raw_words if w]))
    cap_words = [w.title() for w in base_words]
    all_words = list(set(base_words + cap_words))
    
    double_words = [f"{w1}{w2}" for w1 in all_words for w2 in all_words if w1 != w2]
    all_words.extend(double_words)

    numbers = set(config_global["years"])
    
    phone_no = profile.get("phone_no", "")
    if phone_no:
        numbers.add(phone_no)
        if len(phone_no) >= 10:
            numbers.update([phone_no[-4:], phone_no[-6:]])

    dates = [profile["birthdate"], profile["wifeb"], profile["kidb"]]
    for d in dates:
        if len(d) == 8:
            numbers.update([d[-2:], d[-4:], d[:2], d[2:4], d[:4], d[4:]])
            
    # --- DEEP SCALING MATRIX: Guaranteed Volume Hit ---
    target_vol = profile.get("target_volume", 0)
    if target_vol > 0:
        word_count = max(1, len(all_words))
        # Mathematically calculate how many numbers we need to generate to satisfy the target volume
        estimated_numbers_needed = int(target_vol / word_count) + 1000
        # Protect RAM by limiting the number array to max 500,000 (Provides up to ~10-20 Million combos)
        max_num = min(estimated_numbers_needed, 500000) 
        
        print(f"[*] Deep Scaling Matrix Active: Ramping up number sequences to guarantee exactly {target_vol} passwords...")
        numbers.update([str(i) for i in range(max_num)])
        numbers.update(["123", "1234", "12345", "123456", "1433", "007", "111", "999", "6969", "8055"])
    else:
        numfrom = config_global["numfrom"]
        numto = config_global["numto"]
        if numto > 0:
            numbers.update([str(i) for i in range(numfrom, numto + 1)])

    numbers = list(numbers)
    specials = config_global["chars"] if profile.get("spechars1", "y") != "n" else [""]
    
    def pro_generator():
        for w, n in itertools.product(all_words, numbers):
            yield f"{w}{n}"
            yield f"{n}{w}" 
            
        if specials != [""]:
            for w, s, n in itertools.product(all_words, specials, numbers):
                yield f"{w}{s}{n}"
                yield f"{n}{s}{w}"
                yield f"{s}{w}{s}{n}"
                yield f"{w}{n}{s}"

            for w, s in itertools.product(all_words, specials):
                yield f"{w}{s}"
                yield f"{s}{w}"
                yield f"{w}{s}{s}" 

    raw_stream = pro_generator()
    final_stream = stream_processor(
        raw_stream, 
        profile["min_len"], 
        profile["max_len"], 
        profile["leetmode"], 
        config_leet
    )

    filename = profile["name"] + ".txt"
    print_to_file(filename, final_stream, target_vol)
    security_check(filename)

def improve_dictionary(file_to_open, config_global, config_leet):
    if not os.path.isfile(file_to_open):
        print("Error: file " + file_to_open + " does not exist.")
        return

    with open(file_to_open, "r", encoding="utf-8", errors="ignore") as fajl:
        base_words = [line.strip() for line in fajl if line.strip()]

    print("\r\n[+] Pro-Level Dictionary Improvement Active...")
    specials = config_global["chars"]
    numbers = config_global["years"] + [str(i) for i in range(config_global["numfrom"], config_global["numto"] + 1)]
    leetmode = input("> Leet mode? (i.e. leet = 1337) Y/[N]: ").lower().strip()

    def improve_generator():
        for w in base_words:
            yield w
            for n in numbers:
                yield f"{w}{n}"
            for s in specials:
                yield f"{w}{s}"
                for n in numbers:
                    yield f"{w}{s}{n}"

    final_stream = stream_processor(improve_generator(), config_global["wcfrom"], config_global["wcto"], leetmode, config_leet)
    print_to_file(file_to_open + ".cupp.txt", final_stream, 0)