import subprocess
from django.conf import settings
from datetime import datetime
from urlparse import urlparse
from lxml import etree

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

    # save first url for results metadata
    first_url = urls[0]

    for url in urls:
        params['url'] = url
        download_resources(params, is_logged_in, uid)

    # reset url for results metadata
    params['url'] = first_url
    pgcount = analyze_resources(params, is_logged_in, uid, timestamp)
    if not settings.RESOURCES_DEBUG: remove_resources(uid)
    return (pgcount, uid)

#----------------------------------------------------------------
def download_resources(params, is_logged_in, uid):
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
    site_dir = settings.SITES_DIR + uid
    url = params['url']
    depth = params.get('depth', '')
    span = params.get('span', '')

    # construct command
    wget = []
    if not is_logged_in: wget.append('nice')
    wget.append(settings.WGET)
    wget.extend(['--no-check-certificate', '--type-postfixes', '--tries=3', '--timeout=30', '--waitretry=3'])
    wget.extend(['-Q', '6m'])
    wget.extend(['-R', settings.REJECT_LIST])
    wget.extend(['-k', '-p', '-x'])
    if depth == '1' or depth == '2':
        wget.extend(['-r', '-l', depth])
        if span == '1':
            wget.append('-HD{%s}' % get_next_level_domain(url))
    wget.extend(['-P', site_dir])
    wget.append(url)
    return call(wget)

#----------------------------------------------------------------
def analyze_resources(params, is_logged_in, uid, timestamp):
    """
    Process the downloaded files in the sites directory
    (identified by uid) and output results file (also named
    according to uid) in the appropriate reports directory.

    Keys of interest in params dict: url, title, depth, span, username

    """
    results_file = get_results_filename(is_logged_in, uid)
    site_dir = settings.SITES_DIR + uid

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
    retval = call(wamt)

    # run preprocessor transformations
    run_evaluate_proc(results_file)
    run_summarize_proc(results_file)

    pgcount = get_results_pgcount(results_file)
    return pgcount

#----------------------------------------------------------------
def remove_resources(uid):
    cmd = ['rm']
    cmd.append('-rf')
    cmd.append(settings.SITES_DIR + uid)
    return call(cmd)

#----------------------------------------------------------------
def run_evaluate_proc(filename):
    stylesheet = settings.XSLT_PATH + 'evaluate.xsl'
    run_xsltproc(filename, stylesheet)
    
#----------------------------------------------------------------
def run_summarize_proc(filename):
    stylesheet = settings.XSLT_PATH + 'summarize.xsl'
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
    return results_dir + uid + '.xml'

#----------------------------------------------------------------
def get_results_pgcount(filename):
    doc = etree.parse(filename)
    rlist = doc.xpath('/results/meta/pg-count')
    return int(rlist[0].text)
