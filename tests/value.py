#!/usr/bin/env python

from codetalker import testing

import css.grammar as grammar
import css.values
# from css import newgrammar as css

parse_rule = testing.parse_rule(__name__, grammar.grammar)

parse_rule(css.values.length, (
    '10',
    '-10',
    '10px',
    '10 px',
    '-10 px',
    '10 em',
    '-  10 pt',
    '14.3px',
    ), (
    '10p',
    '-em',
    ))

parse_rule(css.values.percentage, (
    '115%',
    '20%',
    '43.2%',
    ), (
    '23',
    '%',
    '24 %',
    '1.4 %',
    ))

parse_rule(css.values.value, (
    '20%',
    '-15.3 px',
    'green',
    '#123',
    '#FFFaab',
    'url(http://example.com/favicon.png)',
    'rgb(0, 0, 100%)',
    ), (
    '#12',
    '#FfFfFfF',
    'oranges',
    ))

# vim: et sw=4 sts=4
