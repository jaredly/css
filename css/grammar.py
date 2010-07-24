#!/usr/bin/env python

from css.tokens import *
from codetalker.pgm.special import commas, star, plus, _or, no_ignore, _not
from codetalker.pgm import Grammar

def cssid(rule):
    ids = ID, COLOR, NODE_NAME, UNIT
    rule | plus('-', _or(*ids)) | (_or(*ids), star('-', _or(*ids)))
    rule.dont_ignore = True
    rule.astAttrs = {'parts': (SYMBOL, ) + ids}

def stylesheet(rule):
    rule | ([charset], star(import_), star(section))
    rule.astAttrs = {
            'charset': charset,
            'imports': [import_],
            'sections': [section],
        }

def charset(rule):
    rule | (no_ignore('@', 'charset'), _or(STRING, SSTRING), ';')
    rule.astAttrs = {'name':{'type':[STRING, SSTRING],'single':True}}

def section(rule):
    rule | ruleset | media | page | font_face
    rule.pass_single = True

def import_(rule):
    rule | (no_ignore('@', 'import'), import_from, [commas(cssid, False)], ';')
    rule.astAttrs = {
        'source':import_from,
        'media':[cssid],
    }

def import_from(rule):
    rule | STRING | URI
    rule.pass_single = True

def media(rule):
    rule | (no_ignore('@', 'media'), commas(cssid, False), '{', star(ruleset), '}')
    rule.astAttrs = {
            'media':[cssid],
            'rulesets':[ruleset],
        }

def page(rule):
    rule | (no_ignore('@', 'page'), [cssid], [':', cssid], block)
    rule.astAttrs = {
        'page':[cssid],
        'rules':[declaration],
    }

def font_face(rule):
    rule | (no_ignore('@', 'font', '-', 'face'), block)
    rule.astAttrs = {
        'rules':[declaration],
    }

def ruleset(rule):
    rule | (commas(selector, False), block)
    rule.astAttrs = {
        'selectors': [selector],
        'rules':[declaration],
    }

def selector(rule):
    rule | (simple_selector, star([_or('+', '>')], simple_selector))
    rule.astAttrs = {
        'parts':[simple_selector, SYMBOL],
    }

def simple_selector(rule):
    postops = hash, class_, attrib, pseudo
    rule | (NODE_NAME, star(_or(postops)))
    rule | plus(_or(postops))
    rule.astAttrs = {
        'node': NODE_NAME,
        'post': postops,
    }

def hash(rule):
    rule | ('#', cssid)
    rule.dont_ignore = True
    rule.astAttrs = {'name':{'type':cssid,'single':True}}

def class_(rule):
    rule | ('.', cssid)
    rule.dont_ignore = True
    rule.astAttrs = {'name':{'type':cssid,'single':True}}

def attrib(rule):
    rule | ('[', cssid, _or('=', no_ignore('|','='), no_ignore('~','=')),
            _or(cssid, _or(STRING, SSTRING)))
    rule.astAttrs = {
        'name':cssid,
        'op':[SYMBOL],
        'value':{
            'type':[cssid, STRING, SSTRING],
            'single':True,
            'start':1,
        }
    }

def pseudo(rule):
    rule | (':', cssid, ['(', cssid, ')'])
    rule.astAttrs = {
        'name':{'type':cssid, 'single':True},
        'args':{'type':cssid, 'single':True, 'start':1},
    }

def declaration(rule):
    rule | (cssid, ':', plus(value), [important])
    rule | star(_not(_or(';', '}')))
    rule.astAttrs = {
        'property':{'type':cssid, 'single':True},
        'values':[value],
        'important':important,
    }

def important(rule):
    rule | ('!', 'important')
    rule.dont_ignore = True

from values import value

block = '{', commas(declaration, True, ';'), '}'

grammar = Grammar(start=stylesheet, tokens = the_tokens,
                  ignore = [WHITE, CMCOMMENT, NEWLINE])

# vim: et sw=4 sts=4
