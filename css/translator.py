#!/usr/bin/env python

from css.grammar import grammar
ast = grammar.ast_classes

from css.tokens import *

from codetalker.pgm import Translator

t = Translator(grammar)

class StyleSheet:
    pass
class Ruleset:
    def __init__(self, selectors, rules):
        self.selectors = selectors
        self.rules = rules

@t.translates(ast.StyleSheet)
def stylesheet(node):
    ss = StyleSheet()
    if node.charset is not None:
        ss.charset = t.translate(node.charset)
    ss.imports = list((imp.source, imp.media) for imp in node.imports)
    ss.rules = []
    for section in node.sections:
        if isinstance(section, ast.Ruleset):
            rule = t.translate(section)
            if rule is not None:
                ss.rules.append(rule)
    return ss

@t.translates(ast.Ruleset)
def ruleset(node):
    rules = {}
    if not node.selectors:
        # print 'bad apple'
        # print node._tree
        return None
    for item in node.rules:
        name, value, important = t.translate(item)
        if name is None:
            continue
        if name not in rules or important >= rules[name][1]:
            rules[name] = value, important
    return Ruleset([t.translate(sel) for sel in node.selectors], rules)

@t.translates(ast.Selector)
def selector(node):
    return [t.translate(part) for part in node.parts]

@t.translates(ast.SimpleSelector)
def simple_sel(node):
    post = {'hash':[],'class':[],'attrib':[],'pseudo':[]}
    c = {ast.Hash:'hash', ast.Cssid:'class', ast.Attrib:'attrib', ast.Pseudo:'pseudo'}
    for item in node.post:
        post[c[item.__class__]].append(t.translate(item))
    return t.translate(node.node), post

@t.translates(ast.Hash)
def hash(node):
    id = ''
    if isinstance(node.name[0], HEXCOLOR):
        id = node.name.pop(0).value
    id += t.translate(node.name[0])
    return id

@t.translates(ast.Attrib)
def attrib(node):
    return cssid(node.name), ''.join(op.value for op in node.op), t.translate(node.value)

@t.translates(ast.Pseudo)
def pseudo(node):
    return cssid(node.name), cssid(node.arg)

@t.translates(ast.Cssid)
def cssid(node):
    return ''.join(part.value for part in node.parts)

@t.translates(ast.Declaration)
def declaration(node):
    if not node.property:
        # print 'bad prop'
        # print node._tree
        return (None, None, False)
    values = list(t.translate(value) for value in node.values)
    if len(values) == 1:values = values[0]
    return cssid(node.property), values, bool(node.important)

class Transparent(object):
    def __repr__(self):
        # print 'hi'
        res = "<'%s'" % self.__class__.__name__
        for k,v in self.__dict__.iteritems():
            res += " %s=%r" % (k, v)
        return res+">"

import inspect

def straight(node):
    obj = type(node.__class__.__name__, (Transparent,), {})()
    keys = []
    if node.__dict__:
        keys = node.__dict__.keys()
    elif hasattr(node, '__slots__'):
        keys = node.__slots__
    elif hasattr(node.__class__, '__slots__'):
        # print 'parent'
        keys = node.__class__.__slots__
    for key in keys:
        v = getattr(node, key, None)
        if type(v) in (tuple, list):
            v = type(v)(t.translate(a) for a in v)
        else:
            v = t.translate(v)
        setattr(obj, key, v)
    return obj

t.translates(ast.Length)(straight)
t.translates(ast.Percentage)(straight)
t.translates(ast.Rgb)(straight)
t.translates(ast.Rgba)(straight)

@t.translates(ast.Uri)
def uri(node):
    return t.translate(node.uri)

@t.translates(ast.UriContents)
def uri_contents(node):
    return ''.join(a.value for a in node.items).strip()

# vim: et sw=4 sts=4
