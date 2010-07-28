#!/usr/bin/env python

from css import css

text = '''#facebox .content{
background:moz-linear-gradient);
}'''

def _test_big():
    res = css.from_string(text)

# vim: et sw=4 sts=4
