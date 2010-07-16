#!/usr/bin/env python

import sys
import css
import cssutils
from css_py.parse import parse
import timeit
text = open(sys.argv[1]).read()


print 'css-py:', timeit.timeit('parse(text)', 'from __main__ import parse, text', number=20)
print 'codetalker:', timeit.timeit('css.parseString(text)', 'from __main__ import css,text', number=20)
print 'cssutils:', timeit.timeit('cssutils.CSSParser().parseString(text)', 'from __main__ import cssutils, text', number=20)


# vim: et sw=4 sts=4
