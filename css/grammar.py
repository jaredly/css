from codetalker.pgm import Grammar
from codetalker.pgm.special import star, plus, _or, commas
from codetalker.pgm.tokens import STRING, ID, NUMBER, EOF, NEWLINE, WHITE, CCOMMENT,\
        ReToken, INDENT, DEDENT, StringToken

import re

class CSSID(ReToken):
    rx = re.compile('[\w-]+')

class SSYMBOL(StringToken):
    items = list('.>:#')

class SYMBOL(StringToken):
    items = list('{};')

class CSSFN(ReToken):
    rx = re.compile('\w+\(([^)\'"]+|\'([^\']|\\.)\'|"([^"]|\\.)")*\)')

def start(rule):
    rule | star(declare)
    rule.astAttrs = {'body':declare}

def declare(rule):
    rule | (selector, '{', star(attr), '}')
    rule.astAttrs = {'selector':{'type':selector, 'single':True}, 'body':attr}

def selector(rule):
    rule | commas(_or(CSSID, SYMBOL), False)
    rule.astAttrs = {'items':(CSSID, SYMBOL, WHITE)}

def attr(rule):
    rule | (CSSID, ':', value, ';')
    rule.astAttrs = {'attr':CSSID, 'value':value}

def value(rule):
    rule | plus(_or(CSSID, NUMBER, CSSFN))
    rule.astAttrs = {'items':(CSSID, NUMBER, CSSFN)}

grammar = Grammar(start=start, indent=False, tokens = [SSYMBOL, SYMBOL, CSSFN, CSSID, NUMBER, CCOMMENT, NEWLINE, WHITE], ignore = [WHITE, CCOMMENT, NEWLINE], ast_tokens = [])

# vim: et sw=4 sts=4
