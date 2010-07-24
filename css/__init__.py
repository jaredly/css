import grammar
import translator
css = translator.t
from dom import CSSStyleSheet

def parseString(text, title=None, href=None, media='screen'):
    return css.from_string(text)

# vim: et sw=4 sts=4
