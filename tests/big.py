#!/usr/bin/env python

from css import css

import os
local = lambda *a:os.path.join(os.path.dirname(__file__), *a)

def test_big():
    text = open(local('big.css')).read()
    res = css.from_string(text)

# vim: et sw=4 sts=4
