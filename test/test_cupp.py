from unittest.mock import patch
import subprocess


def test_main_interactive():
    file = "julian.txt"
    prompts = [
        "Julian",  # First name
        "Assange",  # Surname
        "Mendax",  # Nickname
        "03071971",  # Birthdate
        "",  # Partner's name
        "",  # Partner's nickname
        "",  # Partner's birthdate
        "",  # Child's name
        "",  # Child's nickname
        "",  # Child's birthdate
        "",  # Pet's name
        "",  # Company name
        "N",  # Keywords
        "Y",  # Special chars
        "N",  # Random
        "N",  # Leet mode
        "N",  # Hyperspeed Print
    ]
    targets = ["Julian30771"]

    try:
        proc = subprocess.Popen(
            ["python", "cupp.py", "-i"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
        proc.communicate(input="\n".join(prompts))
    except Exception as e:
        assert False, f"Exception {e}"

    with open(file) as f:
        dictionary = f.read().split("\n")

        for target in targets:
            assert (
                target in dictionary
            ), f"Target '{target}' not found in the dictionary."

    assert True, "Test interactive ok."



