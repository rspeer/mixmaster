#!/usr/bin/env python
"""
This representation comes from http://github.com/offby1/anagrams .
"""

import string
import sys
import unittest

def bag_empty (b):
    return b == 1

letters_to_primes = {}
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
letterfreq = "etaoinshrdlcumwfgypbvkjxqz"
for let, prime in zip(letterfreq, primes):
    letters_to_primes[let] = prime

def bag_of_letters (str):
    str = str.lower()
    rv = 1

    for c in str:
        if (c >= 'a') and (c <= 'z'):
            rv *= letters_to_primes[c]

    return rv

def bags_equal (s1, s2):
    return s1 == s2

def subtract_bags (b1, b2):
    remainder = b1 % b2
    if (0 == remainder):
        return b1 / b2
    else:
        return 0
