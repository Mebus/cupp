from unittest.mock import patch
import subprocess
import os

def test_main_interactive():
    file = "julian.txt"

    if os.path.exists(file):
        os.remove(file)

    prompts = [
        "Julian,Assange,Mendax",  # Names
        "03071971",  # Birthdate
        "Mother,Teresa,Unknown",  # Partner's names
        "26081910",  # Partner's birthdate
        "Wladimir,Wladi,Putin,Benjamin,Netanjahu",  # Child's names
        "07101952,21101949",  # Child's birthdate
        "Jacko,Jacki,Jackson",  # Pet's name
        "New,York,City",  # Company name
        "Y",  # Keywords switch
        "Test,Hentai,Naked",  # Keywords
        "Y",  # Special chars switch
        "Y",  # Random number switch
        "Y",  # Leet mode switch
        "N",  # Hyperspeed Print
    ]
    targets = ["Julian30771"]

    proc = subprocess.Popen(
        ["python", "cupp.py", "-i"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    proc.communicate(input="\n".join(prompts))
    if proc.returncode != 0:
        assert False, f"Error while executing script. Return code={proc.returncode}"

    with open(file) as f:
        dictionary = f.read().split("\n")

        for target in targets:
            assert (
                target in dictionary
            ), f"Target '{target}' not found in the dictionary."

    assert True, "Test interactive ok."


def test_no_changes():
    """For refactoring purposes.
    If changes to output has been made, julian_benchmark.txt has to be updated.
    """
    with open("test/julian_benchmark.txt") as benchmark:
        with open("julian.txt") as target:
            assert benchmark.read() == target.read()
