import os
import subprocess

from datetime import datetime
from urllib import unquote
from urlparse import urlparse
from lxml import etree

from django.conf import settings
from django.utils.encoding import smart_str

from uid import generate

if settings.RESOURCES_DEBUG:
    call = subprocess.check_call
else:
    call = subprocess.call

#----------------------------------------------------------------
def evaluate(params, is_logged_in, timestamp):
    uid = generate()
    download_resources(params, is_logged_in, uid)
    pgcount = analyze_resources(params, is_logged_in, uid, timestamp)
    if not settings.RESOURCES_DEBUG: remove_resources(uid)
    return (pgcount, uid)

#----------------------------------------------------------------
def multi_evaluate(params, is_logged_in, timestamp):
    uid = generate()
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
def download_resources(params, is_logged_in, uid, test=False):
    """
    Call wget to download resources from specified url.

    Keys of interest in params dict: url, depth (optional), span (optional)

    wget switches used:

    --no-check-certificate
    --type-postfixes (save files with type-identifying postfixes; fae wget only)
    --omit-most-urls (blank-out urls in HTML files to facilitate elim. of duplicates; fae wget only)
    --tries
    --timeout
    --wait-retry
    -erobots (evaluate robots.txt files)
    -Q = --quota
    -R = --reject LIST
    -k = --convert-links
    -p = --page-requisites
    -x = --force-directories
    -r = --recursive
    -l = --level
    -H = --span-hosts
    -D = --domains=LIST
    -P = --directory-prefix

    """
    site_dir = os.path.join(settings.SITES_DIR, uid)
    url = params['url']
    depth = params.get('depth', '')
    span = params.get('span', '')

    # construct command
    wget = []
    if not is_logged_in: wget.append('nice')
    wget.append(settings.WGET)
    wget.extend(['--type-postfixes', '--tries=3', '--timeout=30', '--waitretry=3', '-erobots=off'])
    wget.extend(['-Q', '6m'])
    wget.extend(['-R', settings.REJECT_LIST])
    wget.extend(['-k', '-p', '-x'])
    if depth == '1' or depth == '2':
        wget.extend(['-r', '-l', depth])
        if span == '1':
            wget.append('-HD{%s}' % get_next_level_domain(url))
    wget.extend(['-P', site_dir])
    wget.append(url)

    if test: return ' '.join(wget)
    return call(wget)

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
        # TODO: provide more info if invalid
        return 0

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
def get_next_level_domain(url):
    obj = urlparse(url)
    domain = obj.netloc.split(':')[0]
    components = domain.split('.')
    return '.'.join(components[1:])

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
