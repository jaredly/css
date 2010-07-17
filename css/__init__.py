from grammar import grammar, t

def parseString(text, title=None, href=None, media='screen'):
    return t.from_string(text, title=title, href=href, media=media)

# vim: et sw=4 sts=4
