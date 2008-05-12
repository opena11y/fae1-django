from django.conf import settings
from lxml import etree
import os

from labels import labels

#----------------------------------------------------------------
def init_report_procs():
    """Initialize XSLT transform processors."""

    global summary_report_xslt, site_report_xslt, page_report_xslt, report_menu_xslt, report_urls_xslt, pgrpteval_xslt

    summary_report_xslt = etree.parse(os.path.join(settings.XSLT_PATH, 'summary_report.xsl'))
    site_report_xslt = etree.parse(os.path.join(settings.XSLT_PATH, 'site_report.xsl'))
    page_report_xslt = etree.parse(os.path.join(settings.XSLT_PATH, 'page_report.xsl'))
    report_menu_xslt = etree.parse(os.path.join(settings.XSLT_PATH, 'report_menu.xsl'))
    report_urls_xslt = etree.parse(os.path.join(settings.XSLT_PATH, 'report_urls.xsl'))
    pgrpteval_xslt = etree.parse(os.path.join(settings.XSLT_PATH, 'pgrpteval.xsl'))

#----------------------------------------------------------------
def get_report_content(report_info, title):
    global summary_report_xslt, site_report_xslt, page_report_xslt, report_menu_xslt, report_urls_xslt

    rptid = report_info['rptid']
    pgcount = report_info['pgcount']
    section = report_info['section']
    pageid = report_info['pageid']
    filename = report_info['filename']
    results_data = etree.parse(filename)

    params = {
        'id': u"'%s'" % rptid,
        'pc': u"'%s'" % pgcount,
        'section': u"'%s'" % section,
        'pid': u"'%s'" % pageid,
        'title': u"'%s'" % title,
        }
    if report_info['type'] == 'summary':
        proc = etree.XSLT(summary_report_xslt)
    elif report_info['type'] == 'sitewide':
        proc = etree.XSLT(site_report_xslt)
    elif report_info['type'] == 'page':
        proc = etree.XSLT(page_report_xslt)
    elif report_info['type'] == 'menu':
        proc = etree.XSLT(report_menu_xslt)
    elif report_info['type'] == 'urls':
        proc = etree.XSLT(report_urls_xslt)
    else:
        proc = None

    if proc:
        return unicode(proc(results_data, **params))
    else:
        return None

#----------------------------------------------------------------
def get_pgrpteval_content(report_info, testid, eval):
    global pgrpteval_xslt

    rptid = report_info['rptid']
    section = report_info['section']
    filename = report_info['filename']
    results_data = etree.parse(filename)

    params = {
        'id': u"'%s'" % rptid,
        'section': u"'%s'" % section,
        'testid': u"'%s'" % testid,
        'eval': u"'%s'" % eval,
        }

    transform = etree.XSLT(pgrpteval_xslt)
    return unicode(transform(results_data, **params))
