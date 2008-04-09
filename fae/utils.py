from django.conf import settings
from urlparse import urlparse

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
