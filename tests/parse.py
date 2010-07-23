#!/usr/bin/env python

import os
HERE = os.path.dirname(__file__)
local = lambda *a:os.path.join(HERE, *a)

from css import parseString

import textwrap

"""
def test_basic():
    text = '''body {
    color: green;
    }'''
    css = parseString(text)
    assert len(css.rules) == 1
    assert css.rules[0].style.keys() == ['color']
    assert css.rules[0].style['color'] == 'green'

def test_multi():
    text = '''body {
    margin: 2px 3px 1em 4em;}'''
    css = parseString(text)
    assert css.rules[0].style['margin'] == '2px 3px 1em 4em'
    """

# vim: et sw=4 sts=4
