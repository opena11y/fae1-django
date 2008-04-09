from django.conf import settings
from lxml import etree

from utils import get_results_filename
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
    global summary_report_xslt

    summary_report_xslt = etree.parse(settings.XSLT_PATH + 'summary_report.xsl')
    # summary_report_proc = etree.XSLT(summary_report_xslt)

    # site_report_xslt = etree.parse(settings.XSLT_PATH + 'site_report.xsl')
    # site_report = etree.XSLT(site_report_xslt)

    # page_report_xslt = etree.parse(settings.XSLT_PATH + 'page_report.xsl')
    # page_report = etree.XSLT(page_report_xslt)

    # report_menu_xslt = etree.parse(settings.XSLT_PATH + 'menu_report.xsl')
    # report_menu = etree.XSLT(report_menu_xslt)

#----------------------------------------------------------------
def get_report_content(report_info, title, is_logged_in):
    global summary_report_xslt

    rptid = report_info['rptid']
    pgcount = report_info['pgcount']

    results_file = get_results_filename(is_logged_in, rptid)
    results_data = etree.parse(results_file)

    params = {
        'id': u"'%s'" % rptid,
        'pc': u"'%s'" % pgcount,
        'title': u"'%s'" % title,
        }
    if report_info['type'] == 'summary':
        summary_report_proc = etree.XSLT(summary_report_xslt)
        return unicode(summary_report_proc(results_data, **params))
