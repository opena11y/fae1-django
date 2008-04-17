from django.conf import settings
from lxml import etree

from labels import labels

# initialization functions called from __init__.py

#----------------------------------------------------------------
#def init_results_preprocessors():
#   global evaluate_proc, summarize_proc
#   evaluate_xslt = etree.parse(settings.XSLT_PATH + 'evaluate.xsl')
#   evaluate_proc = etree.XSLT(evaluate_xslt)
#   summarize_xslt = etree.parse(settings.XSLT_PATH + 'summarize.xsl')
#   summarize_proc = etree.XSLT(summarize_xslt)

#----------------------------------------------------------------
def init_report_procs():
    global summary_report_xslt, site_report_xslt, pgrpteval_xslt

    summary_report_xslt = etree.parse(settings.XSLT_PATH + 'summary_report.xsl')
    # summary_report_proc = etree.XSLT(summary_report_xslt)

    site_report_xslt = etree.parse(settings.XSLT_PATH + 'site_report.xsl')
    # site_report_proc = etree.XSLT(site_report_xslt)

    pgrpteval_xslt = etree.parse(settings.XSLT_PATH + 'pgrpteval.xsl')

    # page_report_xslt = etree.parse(settings.XSLT_PATH + 'page_report.xsl')
    # page_report_proc = etree.XSLT(page_report_xslt)

    # report_menu_xslt = etree.parse(settings.XSLT_PATH + 'menu_report.xsl')
    # report_menu_proc = etree.XSLT(report_menu_xslt)

#----------------------------------------------------------------
def get_report_content(report_info, title):
    global summary_report_xslt, site_report_xslt

    rptid = report_info['rptid']
    pgcount = report_info['pgcount']
    section = report_info['section']
    filename = report_info['filename']
    results_data = etree.parse(filename)

    params = {
        'id': u"'%s'" % rptid,
        'pc': u"'%s'" % pgcount,
        'section': u"'%s'" % section,
        'title': u"'%s'" % title,
        }
    if report_info['type'] == 'summary':
        summary_report_proc = etree.XSLT(summary_report_xslt)
        return unicode(summary_report_proc(results_data, **params))
    elif report_info['type'] == 'sitewide':
        site_report_proc = etree.XSLT(site_report_xslt)
        return unicode(site_report_proc(results_data, **params))

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

    pgrpteval_proc = etree.XSLT(pgrpteval_xslt)
    return unicode(pgrpteval_proc(results_data, **params))
