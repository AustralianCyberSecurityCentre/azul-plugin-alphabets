"""Library and CLI program for finding possible base64 alphabets in buffers."""

from __future__ import print_function

import os
import sys

VALID = set([c for c in range(0x20, 0x7F)])


def bufset(b: bytes) -> set[int]:
    """Bufset converts a byte string to a set of ints."""
    if sys.version_info[0] == 2:
        return {ord(c) for c in b}
    return {c for c in b}


def find_b64_alphabets(buf):
    """Return a list of valid 64 & 65 char alphabets from supplied byte buf."""
    return find_basen_alphabets(buf, acceptable_lengths=[64, 65])


def find_basen_alphabets(buf: bytes, acceptable_lengths=(32, 64, 65, 85)) -> list[str]:
    """Return a list of valid base 32, 64 and 85 alphabets in buf.

    Use of the keyword argument "acceptable_lengths" will allow finding
    alternate baseN alphabets. Default = [32, 64, 65, 85].
    """
    res: list[str] = []
    for split_char in (b"\0", b'"', b"'", b"\n", b"\r\n"):
        for chunk in buf.split(split_char):
            if len(chunk) in acceptable_lengths:
                if is_basen_alphabet(chunk) and chunk not in res:
                    res.append(chunk.decode())
    return res


def is_basen_alphabet(buf: bytes):
    """Return True if passed byte string is a valid baseN char alphabet."""
    # Create set, check that there were no repeats in string.
    bs = bufset(buf)
    if len(bs) != len(buf):
        return False

    # Check that all chars were valid.
    if not bs.issubset(VALID):
        return False

    return True


HELP = "Finds base64 alphabets. baseN searching not supported by CLI tool."
USAGE = "Usage: b64_alphabet_finder <filepath>|-h/--help"


def main():
    """Only simple CLI support needed."""
    if len(sys.argv) != 2:
        # Incorrect usage.
        print(USAGE, file=sys.stderr)
        return 1
    else:
        # Got required arg - is it help, or invalid?
        if sys.argv[1] in ("-h", "--help"):
            print("%s\n%s" % (HELP, USAGE))
            return 0
        elif not os.path.exists(sys.argv[1]):
            print("Error: specified path file does not exist", file=sys.stderr)
            return 1

        # Scan for base64 files and return.
        with open(sys.argv[1], "rb") as file_handle:
            results = find_basen_alphabets(file_handle.read())
        for res in results:
            print(res)

    # If we get this far, things must have turned out OK.
    return 0


if __name__ == "__main__":
    main()
