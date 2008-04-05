from django.conf import settings
from subprocess import call
from urlparse import urlparse
from uid import generate

# run_wget(params, uid)
# search for .HTML file
# if .HTML file exists
#     run_ocaml(uid)
# else
#     return (0, uid)
# num_pages = get_pgcount(uid)

# report = UserReport(id=uid, user=request.user, pgcount=num_pages...)
# return (pgcount, uid)

#----------------------------------------------------------------
def evaluate(params, is_logged_in):
    uid = generate()
    download_url(params, is_logged_in, uid)
    # if True: remove_download(uid)
    return (True, uid)

#----------------------------------------------------------------
def multi_evaluate(params, is_logged_in):
    uid = generate()
    urls = params['urls']
    for url in urls.split():
        download_url({'url': url}, is_logged_in, uid)
    # if True: remove_download(uid)
    return (True, uid)

#----------------------------------------------------------------
def remove_download(uid):
    cmd = ['rm']
    cmd.append('-rf')
    cmd.append(settings.SITES_DIR + uid)
    return call(cmd)

#----------------------------------------------------------------
def get_next_level_domain(url):
    obj = urlparse(url)
    domain = obj.netloc.split(':')[0]
    components = domain.split('.')
    return '.'.join(components[1:])

#----------------------------------------------------------------
def download_url(params, is_logged_in, uid):
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
    directory = settings.SITES_DIR + uid;
    url = params['url']
    depth = params.get('depth', '')
    span = params.get('span', '')

    reject_list = '.aac,.ac3,.avi,.doc,.mov,.mp2,.mp3,.mpeg,.mpg,.pdf,.ppt,.qt,.wav,.wma'

    wget = []
    if not is_logged_in: wget.append('nice')
    wget.append(settings.WGET)
    wget.extend(['--no-check-certificate', '--type-postfixes', '--tries=3', '--timeout=30', '--waitretry=3'])
    wget.append('-Q 6m')
    wget.append('-R %s' % reject_list)
    wget.extend(['-k', '-p', '-x'])
    if depth == '1' or depth == '2':
        wget.append('-r')
        wget.append('-l %s' % depth)
        if span == '1':
            wget.append('-HD{%s}' % get_next_level_domain(url))
    wget.append('-P')
    wget.append(directory)
    wget.append(url)
    return call(wget)
