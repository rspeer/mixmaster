#!/usr/bin/env python
"""
Represents a bag of letters as an 'alphagram': a sorted list of the letters in
a string.
"""

import string
import sys
import unittest

def alpha_empty (b):
    return b == ""

def make_alpha (str):
    str = str.lower()
    counts = []; 

    for i in range(0, 26):
        counts.append(0);

    for c in str:
        if (c >= 'a') and (c <= 'z'):
            counts[ord(c) - ord('a')] += 1

    rv = "";
    for i in range(0, 26):
        for j in range(0, counts[i]):
            rv += (chr(ord('a') + i));

    return rv;
