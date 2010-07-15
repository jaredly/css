#!/usr/bin/env python

import sys
import css
import cssutils
import timeit
text = open(sys.argv[1]).read()

print 'codetalker:', timeit.timeit('css.css.from_string(text)', 'from __main__ import css,text', number=20)
print 'cssutils:', timeit.timeit('cssutils.CSSParser().parseString(text)', 'from __main__ import cssutils, text', number=20)


# vim: et sw=4 sts=4
