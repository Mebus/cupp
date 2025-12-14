import re
import itertools

def parse_charset(charset_str):
    # Use a regular expression to extract the individual characters from the input string
    chars = re.findall(r'[^,]+', charset_str)
    return chars

def generate_word(charset):
    # Generate a word using the character
    # For simplicity, let's assume a word is just a single character
    return charset

def generate_wordlist(charset=None):
    if charset is None:
        # Default character set
        charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    elif isinstance(charset, str):
        # Custom character set
        charset = parse_charset(charset)
    else:
        raise ValueError("Invalid character set")

    # Generate the wordlist using the custom character set
    wordlist = []
    for r in range(1, 4):  # Generate words of length 1 to 3
        for combination in itertools.product(charset, repeat=r):
            word = ''.join(combination)
            wordlist.append(word)
    return wordlist