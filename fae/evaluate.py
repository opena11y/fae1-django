import os
import subprocess
import logging

from datetime import datetime
from urllib import unquote
from lxml import etree

from django.conf import settings
from django.utils.encoding import smart_str

from uid import generate
from resource_acquisition import call_wget, call_dhtmlget

# Set default resource_acquistion function
if settings.USE_DHTMLGET:
    download_resources = call_dhtmlget
else:
    download_resources = call_wget

if settings.RESOURCES_DEBUG:
    call = subprocess.check_call
else:
    call = subprocess.call

class XMLValidationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

#----------------------------------------------------------------
def evaluate(params, is_logged_in, timestamp):
    uid = generate()

    # Select the appropriate download function
    if params['dhtml'] and is_logged_in:
        download_resources = call_dhtmlget
    else:
        download_resources = call_wget

    start_time = datetime.now()
    download_resources(params, is_logged_in, uid)
    end_time = datetime.now()

    if settings.LOGGING and is_logged_in:
        logging.debug("Elapsed time for %s download: %s", uid, end_time - start_time)

    start_time = datetime.now()
    pgcount = analyze_resources(params, is_logged_in, uid, timestamp)
    end_time = datetime.now()

    if settings.LOGGING and is_logged_in:
        logging.debug("Elapsed time for %s analysis: %s", uid, end_time - start_time)

    if not settings.RESOURCES_DEBUG: remove_resources(uid)
    return (pgcount, uid)

#----------------------------------------------------------------
def multi_evaluate(params, is_logged_in, timestamp):
    uid = generate()

    # Select the appropriate download function
    if params['dhtml'] and is_logged_in:
        download_resources = call_dhtmlget
    else:
        download_resources = call_wget

    urls = params['urls'].split()

    for url in urls:
        params['url'] = url
        download_resources(params, is_logged_in, uid)

    # Cleanup the params dictionary
    del params['url']

    pgcount = analyze_resources(params, is_logged_in, uid, timestamp)
    if not settings.RESOURCES_DEBUG: remove_resources(uid)
    return (pgcount, uid)

#----------------------------------------------------------------
def evaluate_dhtml(params, is_logged_in, timestamp):
    uid = generate()
    request = params['request']
    save_resources(request, uid)
    pgcount = analyze_resources(params, is_logged_in, uid, timestamp)
    if not settings.RESOURCES_DEBUG: remove_resources(uid)
    return (pgcount, uid)

#----------------------------------------------------------------
def save_resources(request, uid):
    """
    Save each string sent as POST data in a separate file.

    The strings are sent as POST['docN'], where N ranges
    from 1 through POST['num_docs'] inclusive. Assertion:
    Caller has tested that len(POST['doc1']) > 0.
    """
    # Current convention for saving HTML files
    file_prefix = 'FILE.'
    html_suffix = '.HTML'

    # Create the directory
    site_dir = os.path.join(settings.SITES_DIR, uid)
    mkdir = ['mkdir', site_dir]
    call(mkdir)

    num_docs = int(request.POST['num_docs'])
    for i in range(1, num_docs + 1):
        doc_id = 'doc' + str(i)
        doc_name = file_prefix + doc_id + '.html' + html_suffix
        filename = os.path.join(site_dir, doc_name)
        file = open(filename, 'wb')

        # To avoid getting escaped/urlencoded soup...
        file.write(unquote(smart_str(request.POST[doc_id])))
        file.close()

#----------------------------------------------------------------
def analyze_resources(params, is_logged_in, uid, timestamp, test=False):
    """
    Process the downloaded files in the sites directory
    (identified by uid) and output results file (also named
    according to uid) in the appropriate reports directory.

    Keys of interest in params dict: url, title, depth, span, username

    """
    results_file = get_results_filename(is_logged_in, uid)
    site_dir = os.path.join(settings.SITES_DIR, uid)

    # Only if this function was called by multi_evaluate should
    # we have a 'urls' key. The value of 'urls' will be a space-
    # separated string of one or more URLs and we need to pass a
    # comma-separated string to wamt
    if 'urls' in params:
        urls = params['urls'].split()
        url = ', '.join(urls)
    else:
        url = params['url']

    title = params['title']
    depth = params.get('depth', '0')
    span = params.get('span', '')
    if not span: span = '0'
    user = params['username']

    # construct command and call it
    wamt = []
    if not is_logged_in: wamt.append('nice')
    wamt.append(settings.WAMT)
    wamt.extend(['-dir', site_dir])
    wamt.extend(['-out', results_file])
    wamt.extend(['-rpt', title])
    wamt.extend(['-date', timestamp.strftime('%Y-%m-%d %H:%M')])
    wamt.extend(['-user', user])
    wamt.extend(['-url',  url])
    wamt.extend(['-depth', depth])
    wamt.extend(['-span', span])

    if test: return ' '.join(wamt)
    retval = call(wamt)

    # validate results file
    parser = etree.XMLParser(dtd_validation=True)
    try:
        tree = etree.parse(results_file, parser)
    except etree.XMLSyntaxError:
        if not settings.RESULTS_FILE_DEBUG:
            remove_results_file(is_logged_in, uid)
        raise XMLValidationError(uid)

    # run preprocessor transformations
    run_evaluate_proc(results_file)
    run_summarize_proc(results_file)

    pgcount = get_results_pgcount(results_file)
    # Remove the results file if no pages were analyzed,
    # but keep it if in debugging mode.
    if not (pgcount or settings.RESULTS_FILE_DEBUG):
        remove_results_file(is_logged_in, uid)
    return pgcount

#----------------------------------------------------------------
def remove_resources(uid):
    cmd = ['rm', '-rf']
    cmd.append(os.path.join(settings.SITES_DIR, uid))
    return call(cmd)

#----------------------------------------------------------------
def remove_results_file(is_logged_in, uid):
    cmd = ['rm', '-f']
    cmd.append(get_results_filename(is_logged_in, uid))
    return call(cmd)

#----------------------------------------------------------------
def run_evaluate_proc(filename):
    stylesheet = os.path.join(settings.XSLT_PATH, 'evaluate.xsl')
    run_xsltproc(filename, stylesheet)
    
#----------------------------------------------------------------
def run_summarize_proc(filename):
    stylesheet = os.path.join(settings.XSLT_PATH, 'summarize.xsl')
    run_xsltproc(filename, stylesheet)

#----------------------------------------------------------------
def run_xsltproc(filename, stylesheet):
    xsltproc = [settings.XSLTPROC]
    xsltproc.extend(['-o', filename])
    xsltproc.append(stylesheet)
    xsltproc.append(filename)
    call(xsltproc)

#----------------------------------------------------------------
def get_results_filename(is_logged_in, uid):
    if is_logged_in:
        results_dir = settings.USER_REPORTS_DIR
    else:
        results_dir = settings.GUEST_REPORTS_DIR
    return os.path.join(results_dir, uid + '.xml')

#----------------------------------------------------------------
def get_results_pgcount(filename):
    doc = etree.parse(filename)
    rlist = doc.xpath('/results/meta/pg-count')
    return int(rlist[0].text)
