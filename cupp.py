import argparse
import wordlist_generator

def main():
    parser = argparse.ArgumentParser(description='Cupp: A wordlist generator')
    parser.add_argument('-i', action='store_true', help='Interactive mode')
    parser.add_argument('--custom-charset', help='Custom character set')
    args = parser.parse_args()

    if args.i:
        # Interactive mode
        print("Interactive mode")
        custom_charset = input("Enter a custom character set (leave blank for default): ")
        if custom_charset:
            wordlist = wordlist_generator.generate_wordlist(custom_charset)
        else:
            wordlist = wordlist_generator.generate_wordlist()
    elif args.custom_charset:
        # Custom character set
        wordlist = wordlist_generator.generate_wordlist(args.custom_charset)
    else:
        # Default character set
        wordlist = wordlist_generator.generate_wordlist()

    print("Generated wordlist:")
    for word in wordlist:
        print(word)

if __name__ == "__main__":
    main()