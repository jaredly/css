from codetalker.pgm import Grammar, Translator
from codetalker.pgm.special import star, plus, _or, commas
from codetalker.pgm.tokens import SSTRING, STRING, ID, NUMBER, EOF, NEWLINE, WHITE, CCOMMENT,\
        ReToken, INDENT, DEDENT, StringToken, CharToken
import re

'''for css values: http://www.westciv.com/style_master/academy/css_tutorial/properties/values.html

- length: number unit
- percentage: number%
- color: #FFF #abcdef green rgb(0, 255, 50%) rgba(0, 0, 0, 50%)
- url: url(...)
- keyword: bold bolder
- shape: rect( 0px 10px auto 2em )
'''

# class CSSID(ReToken):
    # rx = re.compile(r'[\w-]+')
CSSID = ID

class SSYMBOL(CharToken):
    chars = '*[]=.>:#%+'

class SYMBOL(CharToken):
    chars = '{};,()!'

class CSSFN(ReToken):
    rx = re.compile(r'url\([^)]*\)')

def start(rule):
    rule | star(declare)
    rule.astAttrs = {'body':[declare]}

def declare(rule):
    rule | (selectors, '{', star(attr), '}')
    rule.astAttrs = {'selectors':selectors, 'body':[attr]}

def selectors(rule):
    rule | commas(selector, False)
    rule.astAttrs = {'selectors':[selector]}

def selector(rule):
    rule | plus(_or(CSSID, SSYMBOL))
    rule.astAttrs = {'items':[CSSID, SSYMBOL, WHITE]}

def attr(rule):
    rule | (_or(CSSID, ('*', CSSID)), ':', value, ';')
    rule.astAttrs = {'attr':CSSID, 'value':value}

def value(rule):
    rule | plus(_or(CSSID, NUMBER, CSSFN, '#', '%', ':', '=', '{', '(', ')', ',', '.', '*', '!', SSTRING, STRING))
    rule.astAttrs = {'items':[CSSID, NUMBER, CSSFN, SSYMBOL, SYMBOL, STRING]}

grammar = Grammar(start=start, indent=False, idchars='-', tokens = [SSYMBOL, SYMBOL, CSSFN, CSSID, SSTRING, STRING, NUMBER, CCOMMENT, NEWLINE, WHITE], ignore = [WHITE, CCOMMENT, NEWLINE], ast_tokens = [])

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

@t.translates(CSSID)
def _cssid(node):
    return node.value

@t.translates(ast.Value)
def _value(node):
    return str(node)

# vim: et sw=4 sts=4
