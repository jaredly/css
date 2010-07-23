#!/usr/bin/env python

from codetalker import testing

from css import grammar as css

parse_rule = testing.parse_rule(__name__, css.grammar)

parse_rule(css.length, (
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

parse_rule(css.percentage, (
    '115%',
    '20%',
    '43.2%',
    ), (
    '23',
    '%',
    '24 %',
    '1.4 %',
    ))

parse_rule(css.class_, (
    '.one',
    '.green',
    '.GReEn',
    '.div',
    ), (
    'one',
    ))

parse_rule(css.selector_part, (
    'div',
    'div#some',
    'div#one.green',
    'div.frown',
    'ul.cheese:first-child',
    'li.one.two.three',
    'a#b.c.d:last-child',
    ), (
    'one',
    'div# and',
    'div. one',
    ))



# vim: et sw=4 sts=4
