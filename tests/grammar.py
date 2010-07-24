#!/usr/bin/env python

from codetalker import testing

import css.grammar as grammar
import css.values

parse_rule = testing.parse_rule(__name__, grammar.grammar)

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
    }''', '''ul#one {
        margin: 0 2px;
        lots of random junk;
    }'''))

if __name__ == '__main__':
    for name, fn in sorted(globals().items()):
        if name.startswith('test_'):
            print 'testing', name
            fn()
            print 'test passed'
    print 'Finished!'


# vim: et sw=4 sts=4
