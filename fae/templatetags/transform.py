from django import template
from django.conf import settings
from lxml import etree

register = template.Library()

@register.tag
def transform(parser, token):

    """Usage: 'transform' xml-filename xslt-filename

    Tag that transforms an XML document according to template rules in an XSLT stylesheet.
    """
    try:
        tag_name, xml_doc, xslt_doc = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires two arguments" % token.contents.split()[0]
    return TransformNode(xml_doc, xslt_doc)

class TransformNode(template.Node):
    def __init__(self, xml_doc, xslt_doc):
        self.xml_doc = settings.XML_PATH + xml_doc
        self.xslt_doc = settings.XSLT_PATH + xslt_doc

    def render(self, context):
        xml_doc = etree.parse(self.xml_doc)
        xslt_doc = etree.parse(self.xslt_doc)
        process = etree.XSLT(xslt_doc)
        return unicode(process(xml_doc))
