#!/usr/bin/env python
"""
Represents a bag of letters as an 'alphagram': a sorted list of the letters in
a string.
"""

import string
import sys
import unittest

def alpha_empty(b):
    return b == ""

def make_alpha(str):
    str = str.upper()
    return ''.join(sorted(c for c in str if c >= 'A' and c <= 'Z'))

