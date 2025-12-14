import urllib.parse
import requests

# Define allowed schemes
ALLOWED_SCHEMES = ['http', 'https']

def validate_url_scheme(url):
    """
    Validate the URL scheme to prevent potential SSRF attacks.

    Args:
        url (str): The URL to validate.

    Raises:
        ValueError: If the URL scheme is not in the list of allowed schemes.
    """
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Invalid URL scheme: {parsed_url.scheme}")

def open_url(url):
    """
    Open the URL after validating the scheme.

    Args:
        url (str): The URL to open.

    Returns:
        requests.Response: The response from the URL.
    """
    validate_url_scheme(url)
    try:
        response = requests.get(url)
        return response
    except requests.RequestException as e:
        print(f"Error opening URL: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    url = "https://example.com"
    response = open_url(url)
    if response:
        print(f"URL opened successfully: {url}")
    else:
        print(f"Failed to open URL: {url}")