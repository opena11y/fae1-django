from django import template

register = template.Library()

href_dictionary = {
    'best_practices': 'http://html.cita.illinois.edu/',
    'firefox_ext':    'http://firefox.cita.illinois.edu/',
    'iitaa_home':     'http://www.dhs.state.il.us/IITAA/',
    'iitaa_impl':     'http://www.dhs.state.il.us/IITAA/IITAAWebImplementationGuidelines.html',
    'section_508':    'http://www.access-board.gov/sec508/standards.htm',
    'wcag':           'http://www.w3.org/TR/wcag/',
    }

@register.tag
def href_lookup(parser, token):
    """Usage: 'href_lookup' href_id

    Tag that finds the value of an href_id in the hrefs dictionary.
    """
    try:
        tag_name, href_id = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires one argument" % token.contents.split()[0]
    return HrefLookup(href_id)

class HrefLookup(template.Node):
    def __init__(self, href_id):
        self.href_value = href_dictionary.get(href_id, '')

    def render(self, context):
        return unicode(self.href_value)
