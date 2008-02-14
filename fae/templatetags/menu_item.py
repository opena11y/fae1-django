from django import template
from project.fae.labels import labels

register = template.Library()

#----------------------------------------------------------------
def get_list_item(url, label, is_selected):
    """Return HTML 'li' element containing only an 'a' element.

    Return a list item (li element) that contains an anchor (a
    element) with href value equal to url and text content equal
    to label. If is_selected, set CSS class appropriately.

    """
    highlight = ' class="highlight"' if is_selected else ''
    return '<li' + highlight + '><a href="' + url + '">' + label + '</a></li>'

#----------------------------------------------------------------
@register.tag
def menu_item(parser, token):
    """Usage: 'menu_item' page_type

    This tag is used for non-report page types. It is the most
    general purpose of the tags in this module.

    """
    try:
        tag_name, page_type = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires one argument" % token.contents.split()[0]
    return MenuItemNode(page_type)

class MenuItemNode(template.Node):
    def __init__(self, page_type):
        self.page_type = page_type
        self.label = labels[page_type]

    def render(self, context):
        # Determine whether menu item is currently selected
        selected = context['page_type'] == self.page_type

        # Construct the URL
        if self.page_type == 'index':
            url = r'/'
        else:
            url = r'/' + self.page_type + r'/'

        return get_list_item(url, self.label, selected)

#----------------------------------------------------------------
@register.tag
def section_item(parser, token):
    """Usage: 'section_item' section
    
    This tag is used for creating menu items based on the report
    sections of sitewide and page reports. These sections
    correspond to the five main categories of best practices.

    """
    try:
        tag_name, section = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires one argument" % token.contents.split()[0]
    return SectionItemNode(section)

class SectionItemNode(template.Node):
    def __init__(self, section):
        self.section = section
        self.label = labels['section'][section]

    def render(self, context):
        # Get the report dictionary
        report = context['report']

        # Determine whether menu item is currently selected
        selected = (context['page_type'] == 'report') and (report['section'] == self.section)

        # Construct the URL
        url = r'/report/' + report['rptid'] + r'/' + report['type'] + r'/'

        if report['type'] == 'page':
            url += report['pageid'] + r'/'

        url += self.section + r'/'

        return get_list_item(url, self.label, selected)

#----------------------------------------------------------------
@register.tag
def report_item(parser, token):
    """Usage: 'report_item' report_type

    This tag is used for creating menu items for the various
    report types. Valid report_type values include summary,
    sitewide, page and menu.

    """
    try:
        tag_name, report_type = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires one argument" % token.contents.split()[0]
    return ReportItemNode(report_type)

class ReportItemNode(template.Node):
    def __init__(self, type):
        self.type = type
        self.label = labels['report'][type]

    def render(self, context):
        # Get the report dictionary
        report = context['report']

        # Determine whether item is currently selected
        selected = (context['page_type'] == 'report') and (report['type'] == self.type)

        # Construct the URL
        url = r'/report/' + report['rptid'] + r'/' + self.type + r'/'

        if self.type == 'page':
            url += report['pageid'] + r'/'

        if self.type in ['sitewide', 'page']:
            url += report['section'] + r'/'

        # Construct the label
        label = self.label

        if self.type == 'page' and report['pgcount'] != '1':
            label += ': ' + report['pageid']

        if self.type == 'menu':
            label += ': ' + report['pgcount']

        return get_list_item(url, label, selected)

#----------------------------------------------------------------
@register.tag
def prev_next_item(parser, token):
    """Usage: 'prev_next_item'

    This tag is used for creating a bipartite menu item that
    allows moving to the previous or next page report.

    """
    try:
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires no arguments" % token.contents.split()[0]
    return PreviousNextItemNode()

class PreviousNextItemNode(template.Node):
    def __init__(self):
        self.prev_label = labels['prev']
        self.next_label = labels['next']

    def render(self, context):
        # Get the report dictionary
        report = context['report']

        # Convert relevant string values to integers
        page_number = int(report['pageid'])
        total_pages = int(report['pgcount'])

        # Construct urls (Note: invalid page_numbers are filtered below)
        url_prefix = r'/report/' + report['rptid'] + r'/page/'
        url_suffix = r'/' + report['section'] + r'/'
        prev_url = url_prefix + str(page_number - 1) + url_suffix
        next_url = url_prefix + str(page_number + 1) + url_suffix

        if page_number > 1:
            prev_tag = '<a href="' + prev_url + '">' + self.prev_label + '</a>'
        else:
            prev_tag = '<span class="grayed-out">' + self.prev_label + '</span>'

        if page_number < total_pages:
            next_tag = '<a href="' + next_url + '">' + self.next_label + '</a>'
        else:
            next_tag = '<span class="grayed-out">' + self.next_label + '</span>'

        return '<li>' + prev_tag + ' | ' + next_tag + '</li>'
