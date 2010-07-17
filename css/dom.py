class CSSStyleSheet:
    def __init__(self, title, href, media, rules):
        self.cssrules = self.rules = rules
        self.disabled = False
        self.href = href
        self.media = media
        self.ownerRule = None # ?
        self.parentStyleSheet = None # ?
        self.title = title
        self.type = 'text/css'
        for rule in rules:
            rule.parentStyleSheet = self

class CSSStyleRule:
    def __init__(self, selectors, text, style):
        self.cssText = text
        self.parentRule = None # ?
        self.parentStyleSheet = None
        self.selectorText = selectors
        self.style = style

