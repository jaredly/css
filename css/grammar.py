from codetalker.pgm import Grammar, Translator
from codetalker.pgm.special import star, plus, _or, commas
from codetalker.pgm.tokens import STRING, ID, NUMBER, EOF, NEWLINE, WHITE, CCOMMENT,\
        ReToken, INDENT, DEDENT, StringToken

import re

class CSSID(ReToken):
    rx = re.compile('[\w-]+')

class SSYMBOL(StringToken):
    items = list('.>:#')

class SYMBOL(StringToken):
    items = list('{};,')

class CSSFN(ReToken):
    rx = re.compile('[\w-]+\(([^)\'"]+|\'([^\']|\\.)\'|"([^"]|\\.)")*\)')

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
    rule | _or(CSSID, SYMBOL)
    rule.astAttrs = {'items':(CSSID, SYMBOL, WHITE)}

def attr(rule):
    rule | (CSSID, ':', value, ';')
    rule.astAttrs = {'attr':{'type':CSSID, 'single':True}, 'value':{'type':value, 'single':True}}

def value(rule):
    rule | plus(_or(CSSID, NUMBER, CSSFN))
    rule.astAttrs = {'items':(CSSID, NUMBER, CSSFN)}

grammar = Grammar(start=start, indent=False, tokens = [SSYMBOL, SYMBOL, CSSFN, CSSID, NUMBER, CCOMMENT, NEWLINE, WHITE], ignore = [WHITE, CCOMMENT, NEWLINE], ast_tokens = [])

t = Translator(grammar)

class CSSStyleSheet(object):
    def __init__(self, rules=[]):
        self.rules = list(rules)

class SelectorList(object):
    def __init__(self, text, selectors):
        self.selectors = selectors
        self.text = text

class CSSRule(object):
    def __init__(self, selectors, attrs):
        self.selectors = selectors
        self.attrs = attrs

ast = grammar.ast_classes

@t.translates(ast.start)
def _start(node, scope):
    return CSSStyleSheet(t.translate(rule, scope) for rule in node.body)

@t.translates(ast.declare)
def _declare(node, scope):
    selectors = t.translate(node.selectors, scope)
    return CSSRule(selectors, dict(t.translate(attr, scope) for attr in node.body))

@t.translates(ast.selectors)
def _selectors(node, scope):
    return SelectorList(str(node), (t.translate(sel) for sel in node.selectors))

@t.translates(ast.selector)
def _selector(node, scope):
    return str(node)

@t.translates(ast.attr)
def _attr(node, scope):
    return t.translate(node.attr, scope), t.translate(node.value, scope)

@t.translates(CSSID)
def _cssid(node, scope):
    return node.value

@t.translates(ast.value)
def _value(node, scope):
    return str(node)

# vim: et sw=4 sts=4
