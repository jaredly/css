#!/usr/bin/env python

from codetalker import testing

import css.newgrammar as grammar
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

parse_rule(grammar.class_, (
    '.one',
    '.green',
    '.GReEn',
    '.div',
    ), (
    'one',
    ))

parse_rule(grammar.simple_selector, (
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

parse_rule(grammar.selector, (
    'div li > table#man.foo',
    '#some.one td:hover',
    'body a a + div',
    ), (
    'one',
    '',
    ))

parse_rule(grammar.ruleset, (
    '''div {
        color: green;
    }''', ))


# vim: et sw=4 sts=4
