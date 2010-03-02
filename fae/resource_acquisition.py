import os
import subprocess
import logging

from urlparse import urlparse

from django.conf import settings
from uid import generate

if settings.RESOURCES_DEBUG:
    call = subprocess.check_call
else:
    call = subprocess.call

#----------------------------------------------------------------
def get_next_level_domain(url):
    obj = urlparse(url)
    domain = obj.netloc.split(':')[0]
    components = domain.split('.')
    return '.'.join(components[1:])

#----------------------------------------------------------------
def call_wget(params, is_logged_in, uid, test=False):
    """
    Call wget to download resources from specified url.

    Keys of interest in params dict: url, depth (optional), span (optional)

    wget switches used:

    --no-check-certificate (not in use)
    --omit-most-urls (blank-out urls in HTML files for elim. of duplicates; fae wget only; not in use)
    --type-postfixes (save files with type-identifying postfixes; fae wget only)
    --tries
    --timeout
    --wait-retry
    -erobots (evaluate robots.txt files)
    -Q = --quota
    -R = --reject LIST
    -k = --convert-links
    -p = --page-requisites
    -x = --force-directories
    -P = --directory-prefix
    -r = --recursive
    -l = --level
    --span-hosts
    --domains=LIST

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
    wget.extend(['-P', site_dir])
    if depth == '1' or depth == '2':
        wget.extend(['-r', '-l', depth])
        if span == '1':
            wget.extend(['--span-hosts', '--domains=%s' % get_next_level_domain(url)])
    wget.append(url)

    if settings.WGET_DEBUG and url.startswith('https'):
        log_file = open(os.path.join(settings.LOGS_DIR, 'wget.log'), 'a')
        kwargs = { 'stdout': log_file, 'stderr': subprocess.STDOUT }
    else:
        kwargs = {}

    if settings.LOGGING:
        logging.debug("Calling WGET for %s: %s", params['username'], ' '.join(wget))

    if test: return ' '.join(wget)
    return call(wget, **kwargs)

#----------------------------------------------------------------
def call_dhtmlget(params, is_logged_in, uid, test=False):
    """
    Call dhtmlget to download resources from specified url.

    Keys of interest in params dict: url, depth (optional), span (optional)

    dhtmlget switches used:

    -P              # add prefix and postfix strings to filename
    -p              # include page-requisites
    -R              # replace escaped comment delimiters with non-escaped characters
    -T              # remove text content from script tags

    -l <depth>      # where depth is 0, 1 or 2; default is 0
    -C              # enable link following to all subdomains of url
    -Q <number>     # where number is in MBs; default is 10

    -N <directory>  # required

    """
    site_dir = os.path.join(settings.SITES_DIR, uid)
    url = params['url']
    depth = params.get('depth', '')
    span = params.get('span', '')

    # construct command
    dhtmlget = []
    if not is_logged_in: dhtmlget.append('nice')
    dhtmlget.append(settings.DHTMLGET)
    dhtmlget.extend(['-P', '-p', '-R', '-T'])

    if depth == '1' or depth == '2':
        dhtmlget.extend(['-l', depth])
        if span == '1':
            dhtmlget.append('-C')

    dhtmlget.extend(['-N', site_dir])
    dhtmlget.append(url)

    if settings.LOGGING:
        logging.debug("Calling DHTMLGET for %s: %s", params['username'], ' '.join(dhtmlget))

    if test: return ' '.join(dhtmlget)
    return call(dhtmlget)
