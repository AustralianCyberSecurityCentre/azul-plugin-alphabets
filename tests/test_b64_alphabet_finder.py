from __future__ import print_function

import os
import sys
import unittest

from azul_plugin_alphabets import b64_alphabet_finder


class TestBase64AlphabetFinder(unittest.TestCase):
    def test_find(self):
        contains = b"""zs78dfy6vnauwicv as
            ddfdbc,\0\a\n\rkajsdghfkajsdhf
            the following 2 lines are valid
            \0ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/\0
            \0ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\0
            the following line invalid - it has duplicate A
            \0AACDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/\0
            the following line invalid - it has invalid characters (tab)
            \0\tBCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/\0
            \n1234567890qwertyuiop[]asdfghjkl;\n
            978234jygasdhfbv"""
        # Test base64 alphabets.
        does_not_contain = b"asdjkfha asdf asdf asdf ' asdfasdf as'asdf "
        res = b64_alphabet_finder.find_b64_alphabets(contains)
        self.assertEqual(len(res), 2)
        res = b64_alphabet_finder.find_b64_alphabets(does_not_contain)
        self.assertEqual(len(res), 0)

        # Test base32 (basen) alphabet.
        res = b64_alphabet_finder.find_basen_alphabets(contains)
        self.assertEqual(len(res), 3)
        res = b64_alphabet_finder.find_basen_alphabets(contains, acceptable_lengths=[32])
        self.assertEqual(len(res), 1)


class TestBase64AlphabetFinderMain(unittest.TestCase):
    def setUp(self):
        self.argv = sys.argv

    def tearDown(self):
        sys.argv = self.argv

    def test_main(self):
        # Test success.
        sys.argv = [b64_alphabet_finder.__file__, __file__]
        self.assertEqual(b64_alphabet_finder.main(), 0)
        sys.argv = [b64_alphabet_finder.__file__, "--help"]
        self.assertEqual(b64_alphabet_finder.main(), 0)

        # Test without file argument - assert exit status 1.
        sys.argv = [
            b64_alphabet_finder.__file__,
        ]
        self.assertEqual(b64_alphabet_finder.main(), 1)

        # Test on non-existant file - assert exit status 1.
        sys.argv = [b64_alphabet_finder.__file__, os.path.join(__file__, "foo")]
        self.assertEqual(b64_alphabet_finder.main(), 1)
