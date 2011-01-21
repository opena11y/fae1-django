import logging
import platform
from django.conf import settings
from django.http import HttpResponse

def init_logger(name):
    global logger

    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create file handler
    fh = logging.FileHandler(settings.TIMING_LOG)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(settings.TIMING_FMT)

    # add fh to logger
    logger.addHandler(fh)

def get_logger():
    return logger

def sysinfo(request):
    version = platform.python_version()
    html = "<html><head><title>System Information</title></head><body>Python Version %s</body></html>" % version
    return HttpResponse(html)

import urllib2
from django.core.exceptions import ValidationError

def urltest(request):
    URL_VALIDATOR_USER_AGENT = 'Django (http://www.djangoproject.com/)'

    value = u'https://netfiles.uiuc.edu/rslater/www/langtest.html'

    headers = {
        "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
        "Accept-Language": "en-us,en;q=0.5",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
        "Connection": "close",
        "User-Agent": URL_VALIDATOR_USER_AGENT,
        }

    default_error_messages = {
        'invalid': u'Enter a valid URL.',
        'invalid_link': u'This URL appears to be a broken link.',
        }

    try:
        req = urllib2.Request(value, None, headers)
        u = urllib2.urlopen(req)
    except ValueError:
        raise ValidationError(default_error_messages['invalid'])
    except: # urllib2.URLError, httplib.InvalidURL, etc.
        raise ValidationError(default_error_messages['invalid_link'])

    html = "<html><head><title>URL Test</title></head><body><p>%s</p><pre>%s</pre></body></html>" % (u.geturl(),  u.info())
    return HttpResponse(html)
