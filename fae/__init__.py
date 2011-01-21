from django.db.models import signals

from models import UserReport, GuestReport
import processors

# instantiate Relax NG validator
# processors.init_rng_validator()

# instantiate XSLT processors
processors.init_report_procs()

def delete_report_notification(sender, **kwargs):
    instance = kwargs['instance']
    instance.remove_results_file()

signals.pre_delete.connect(delete_report_notification, sender=UserReport)
signals.pre_delete.connect(delete_report_notification, sender=GuestReport)

import utils
utils.init_logger('TIMING')
