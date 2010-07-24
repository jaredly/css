#!/usr/bin/env python

from codetalker.pgm.tokens import *
import constants
import re

## specified http://www.w3.org/TR/2008/REC-CSS2-20080411/syndata.html#tokenization

class SYMBOL(CharToken):
    chars = '@#-%();{}[].:>+,'

class HTMLCOMMENT(StringToken):
    strings = '<!--', '-->'

class URI(ReToken):
    rx = re.compile(r'url\([^)]*\)')

class UNIT(IIdToken):
    strings = 'em', 'px', 'pt', 'mm', 'cm', 'rad', 'deg', 'grad', 'in'

class COLOR(IIdToken):
    strings = constants.colors

class NODE_NAME(IIdToken):
    strings = constants.tags

class HEXCOLOR(ReToken):
    rx = re.compile(r'#([\da-fA-F]{6}|[\da-fA-F]{3})')

the_tokens = [NUMBER, HEXCOLOR, CMCOMMENT, HTMLCOMMENT, SYMBOL, UNIT, COLOR, NODE_NAME, STRING, SSTRING, URI, ID, WHITE, NEWLINE, ANY]

# vim: et sw=4 sts=4
