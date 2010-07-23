
from codetalker.pgm import Grammar, Translator
from codetalker.pgm.special import star, plus, _or, commas
from codetalker.pgm.tokens import SSTRING, STRING, ID, NUMBER, EOF, NEWLINE, WHITE, CCOMMENT,\
        ReToken, INDENT, DEDENT, StringToken, CharToken, IIdToken
import re

'''for css values: http://www.westciv.com/style_master/academy/css_tutorial/properties/values.html

- length: number unit
- percentage: number%
- color: #FFF #abcdef green rgb(0, 255, 50%) rgba(0, 0, 0, 50%)
- url: url(...)
- keyword: bold bolder
- shape: rect( 0px 10px auto 2em )
'''

import constants

# class cssid(ReToken):
    # rx = re.compile(r'[\w-]+')

class SSYMBOL(CharToken):
    chars = '*[]=.>:#%+-'

class SYMBOL(CharToken):
    chars = '{};,()!'

class CSSFN(ReToken):
    rx = re.compile(r'url\([^)]*\)')

class UNIT(IIdToken):
    strings = 'em', 'px', 'pt'

class COLOR(IIdToken):
    strings = constants.colors

class NODE_NAME(IIdToken):
    strings = constants.tags

class HEXCOLOR(ReToken):
    rx = re.compile('#([\da-fA-F]{3}|[\da-fA-F]{6})')

def start(rule):
    rule | star(declare)
    rule.astAttrs = {'body':[declare]}

def declare(rule):
    rule | (selectors, '{', star(_or(attr, ignore)), '}')
    rule.astAttrs = {'selectors':selectors, 'body':[attr]}

def selectors(rule):
    rule | commas(selector, False)
    rule.astAttrs = {'selectors':[selector]}

def selector(rule):
    rule | (selector_part, star([_or('+', '>')], selector_part))
    rule.astAttrs = {'parts':[selector_part, SSYMBOL]}

def selector_part(rule):
    rule | (_or(
                (NODE_NAME, [id], star(class_)),
                (id, star(class_)),
                plus(class_)
            ),
            [pseudo])
    rule.astAttrs = {
            'node':[NODE_NAME],
            'id':[id],
            'classes':[class_],
            'pseudo':[pseudo]
        }

def id(rule):
    rule | ('#', _or(ID, NODE_NAME, COLOR))
    rule.dont_ignore = True
    rule.pass_single = True

def class_(rule):
    rule | ('.', _or(ID, NODE_NAME, COLOR))
    rule.dont_ignore = True
    rule.pass_single = True

def pseudo(rule):
    rule | (':', cssid)
    rule.dont_ignore = True
    rule.pass_single = True

def ignore(rule):
    rule | (plus(SSYMBOL, CSSFN, '{', '(', ')', '!', ',', STRING, ID), ';')

def attr(rule):
    rule | (cssid, ':', plus(value), ['!', 'important'], ';')
    rule.astAttrs = {'attr':cssid, 'values':[value]}

def value(rule):
    rule | COLOR | HEXCOLOR | length | percentage | CSSFN
    rule.pass_single = True

def cssid(rule):
    rule | plus('-', ID) | (ID, star('-', ID))
    rule.dont_ignore = True
    rule.astAttrs = {'parts': [SSYMBOL, ID]}

def length(rule):
    rule | (['-'], NUMBER, [UNIT])
    rule.astAttrs = {'neg':[SSYMBOL], 'value':NUMBER, 'unit':[UNIT]}

def percentage(rule):
    rule | (['-', star(_or(WHITE, CCOMMENT, NEWLINE))], NUMBER, '%')
    rule.dont_ignore = True
    rule.astAttrs = {'neg':[SSYMBOL], 'value':NUMBER}

grammar = Grammar(start=start, indent=False, idchars='-',
        tokens = [NUMBER, CSSFN, UNIT, COLOR, NODE_NAME,
                  HEXCOLOR, SYMBOL, SSYMBOL, WHITE, ID,
                  CCOMMENT, STRING, NEWLINE],
        ignore = [WHITE, CCOMMENT, NEWLINE], ast_tokens = [])

from css.dom import CSSStyleSheet, CSSStyleRule

t = Translator(grammar)

ast = grammar.ast_classes

@t.translates(ast.Start)
def _start(node):
    return list(t.translate(rule) for rule in node.body)

@t.translates(ast.Declare)
def _declare(node):
    return CSSStyleRule(
            str(node.selectors),
            str(node),
            dict(t.translate(attr) for attr in node.body)
        )

@t.translates(ast.Attr)
def _attr(node):
    return t.translate(node.attr), t.translate(node.value)

@t.translates(ast.Cssid)
def _cssid(node):
    return node.value

# vim: et sw=4 sts=4
