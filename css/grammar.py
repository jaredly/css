from codetalker.pgm import Grammar, Translator
from codetalker.pgm.special import star, plus, _or, commas
from codetalker.pgm.tokens import STRING, ID, NUMBER, EOF, NEWLINE, WHITE, CCOMMENT,\
        ReToken, INDENT, DEDENT, StringToken
import re

'''for css values: http://www.westciv.com/style_master/academy/css_tutorial/properties/values.html

- length: number unit
- percentage: number%
- color: #FFF #abcdef green rgb(0, 255, 50%) rgba(0, 0, 0, 50%)
- url: url(...)
- keyword: bold bolder
- shape: rect( 0px 10px auto 2em )
'''

class CSSID(ReToken):
    rx = re.compile(r'[\w-]+')

class SSYMBOL(StringToken):
    items = list('.>:#%')

class SYMBOL(StringToken):
    items = list('{};,')

class CSSFN(ReToken):
    rx = re.compile(r'[\w-]+\([^)]*\)')

def start(rule):
    rule | star(declare)
    rule.astAttrs = {'body':declare}

def declare(rule):
    rule | (selectors, '{', star(attr), '}')
    rule.astAttrs = {'selectors':{'type':selectors, 'single':True}, 'body':attr}

def selectors(rule):
    rule | commas(selector, False)
    rule.astAttrs = {'selectors':selector}

def selector(rule):
    rule | plus(_or(CSSID, SSYMBOL))
    rule.astAttrs = {'items':(CSSID, SSYMBOL, WHITE)}

def attr(rule):
    rule | (CSSID, ':', value, ';')
    rule.astAttrs = {'attr':{'type':CSSID, 'single':True}, 'value':{'type':value, 'single':True}}

def value(rule):
    rule | plus(_or(CSSID, NUMBER, '#', '%', CSSFN))
    rule.astAttrs = {'items':(CSSID, NUMBER, SSYMBOL, CSSFN)}

grammar = Grammar(start=start, indent=False, tokens = [SSYMBOL, SYMBOL, CSSFN, CSSID, NUMBER, CCOMMENT, NEWLINE, WHITE], ignore = [WHITE, CCOMMENT, NEWLINE], ast_tokens = [])

from css.dom import CSSStyleSheet, CSSStyleRule

t = Translator(grammar)

ast = grammar.ast_classes

@t.translates(ast.Start)
def _start(node, scope):
    return CSSStyleSheet(
            scope.title,
            scope.href,
            scope.media,
            list(t.translate(rule, scope) for rule in node.body)
        )

@t.translates(ast.Declare)
def _declare(node, scope):
    return CSSStyleRule(
            str(node.selectors),
            str(node),
            dict(t.translate(attr, scope) for attr in node.body)
        )

@t.translates(ast.Attr)
def _attr(node, scope):
    return t.translate(node.attr, scope), t.translate(node.value, scope)

@t.translates(CSSID)
def _cssid(node, scope):
    return node.value

@t.translates(ast.Value)
def _value(node, scope):
    return str(node)

# vim: et sw=4 sts=4
