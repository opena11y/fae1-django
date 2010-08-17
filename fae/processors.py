from django.conf import settings
from lxml import etree
import os

from labels import labels

#----------------------------------------------------------------
def init_report_procs():
    """Initialize XSLT transform processors."""

    global summary_report_xslt, site_report_xslt, page_report_xslt, report_menu_xslt, report_urls_xslt, data_export_xslt, pgrpteval_xslt

    summary_report_xslt = etree.parse(os.path.join(settings.XSLT_PATH, 'summary_report.xsl'))
    site_report_xslt    = etree.parse(os.path.join(settings.XSLT_PATH, 'site_report.xsl'))
    page_report_xslt    = etree.parse(os.path.join(settings.XSLT_PATH, 'page_report.xsl'))
    report_menu_xslt    = etree.parse(os.path.join(settings.XSLT_PATH, 'report_menu.xsl'))
    report_urls_xslt    = etree.parse(os.path.join(settings.XSLT_PATH, 'report_urls.xsl'))
    data_export_xslt    = etree.parse(os.path.join(settings.XSLT_PATH, 'data_export.xsl'))
    pgrpteval_xslt      = etree.parse(os.path.join(settings.XSLT_PATH, 'pgrpteval.xsl'))

#----------------------------------------------------------------
def get_report_content(report_info, title):

    # Try parsing the XML results file
    filename = report_info['filename']
    try:
        results_data = etree.parse(filename)
    except IOError:
        return None

    # Set up dictionary with top-level parameters
    params = {
        'id':      u"'%s'" % report_info['rptid'],
        'pc':      u"'%s'" % report_info['pgcount'],
        'section': u"'%s'" % report_info['section'],
        'pid':     u"'%s'" % report_info['pageid'],
        'ruleset': u"'%s'" % settings.RULESET,
        'title':   u"'%s'" % title,
        }

    # Select the appropriate XSLT stylesheet
    t = report_info['type']
    if   t == 'summary':
        proc = etree.XSLT(summary_report_xslt)
    elif t == 'sitewide':
        proc = etree.XSLT(site_report_xslt)
    elif t == 'page':
        proc = etree.XSLT(page_report_xslt)
    elif t == 'menu':
        proc = etree.XSLT(report_menu_xslt)
    elif t == 'urls':
        proc = etree.XSLT(report_urls_xslt)
    elif t == 'xml':
        proc = etree.XSLT(data_export_xslt)
    else:
        proc = None

    if t == 'page' or t == 'sitewide':
        params['nodata'] = u"'%s'" % labels['nodata']

    # Transform the results data
    if proc:
        return unicode(proc(results_data, **params))
    else:
        return None

#----------------------------------------------------------------
def get_pgrpteval_content(report_info, testid, eval):

    # Try parsing the XML results file
    filename = report_info['filename']
    try:
        results_data = etree.parse(filename)
    except IOError:
        return None

    # Set up dictionary with top-level parameters
    params = {
        'id':      u"'%s'" % report_info['rptid'],
        'section': u"'%s'" % report_info['section'],
        'testid':  u"'%s'" % testid,
        'eval':    u"'%s'" % eval,
        }

    # Transform the results data
    transform = etree.XSLT(pgrpteval_xslt)
    return unicode(transform(results_data, **params))
