import newgrammar as grammar
from dom import CSSStyleSheet

def parseString(text, title=None, href=None, media='screen'):
    return CSSStyleSheet(
            title,
            href,
            media,
            t.from_string(text)
        )

# vim: et sw=4 sts=4
