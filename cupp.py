import urllib.parse
import sys

# Define allowed schemes
ALLOWED_SCHEMES = ['http', 'https']

def validate_url_scheme(url):
    """
    Validate the URL scheme to prevent potential security vulnerabilities.

    Args:
        url (str): The input URL to validate.

    Returns:
        bool: True if the URL scheme is valid, False otherwise.
    """
    try:
        # Parse the URL and extract the scheme
        parsed_url = urllib.parse.urlparse(url)
        scheme = parsed_url.scheme

        # Check if the scheme is in the list of allowed schemes
        if scheme not in ALLOWED_SCHEMES:
            print(f"Error: Invalid URL scheme '{scheme}' in URL '{url}'. Only {ALLOWED_SCHEMES} schemes are allowed.")
            return False
        return True
    except ValueError as e:
        print(f"Error: Failed to parse URL '{url}': {e}")
        return False

def main():
    # Example usage:
    url = "http://example.com"
    if validate_url_scheme(url):
        print(f"URL '{url}' has a valid scheme.")
    else:
        print(f"URL '{url}' has an invalid scheme.")

    # Test with an invalid scheme
    url = "file:///etc/passwd"
    if validate_url_scheme(url):
        print(f"URL '{url}' has a valid scheme.")
    else:
        print(f"URL '{url}' has an invalid scheme.")

if __name__ == "__main__":
    main()