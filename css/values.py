#!/usr/bin/env python

'''for css values: http://www.westciv.com/style_master/academy/css_tutorial/properties/values.html

- length: number unit
- percentage: number%
- color: #FFF #abcdef green rgb(0, 255, 50%) rgba(0, 0, 0, 50%)
- url: url(...)
- keyword: bold bolder
- shape: rect( 0px 10px auto 2em )
'''

from css.tokens import *
from codetalker.pgm.special import commas, no_ignore, _or

def value(rule):
    rule | COLOR | HEXCOLOR | percentage | length | URI | rgb | rgba
    rule.pass_single = True

def length(rule):
    rule | (['-'], NUMBER, [UNIT])
    rule.astAttrs = {'neg':SYMBOL, 'value':NUMBER, 'unit':UNIT}

def percentage(rule):
    rule | (['-'], no_ignore(NUMBER, '%'))
    rule.astAttrs = {'neg':SYMBOL, 'value':NUMBER}

def rgb(rule):
    rule | ('rgb', '(', ((_or(percentage, NUMBER), ',')*3)[:-1], ')')
    rule.astAttrs = {
            'red':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':0},
            'green':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':1},
            'blue':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':2},
            }

def rgba(rule):
    rule | ('rgba', '(', ((_or(percentage, NUMBER), ',')*4)[:-1], ')')
    rule.astAttrs = {
            'red':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':0},
            'green':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':1},
            'blue':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':2},
            'alpha':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':3},
            }

# vim: et sw=4 sts=4
