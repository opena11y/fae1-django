from django.dispatch import dispatcher
from django.db.models import signals

from models import UserReport, GuestReport
import processors

# instantiate Relax NG validator
# processors.init_rng_validator()

# instantiate XSLT processors
processors.init_report_procs()

def delete_report_notification(sender, instance):
    instance.remove_results_file()

dispatcher.connect(delete_report_notification, sender=UserReport, signal=signals.pre_delete)
dispatcher.connect(delete_report_notification, sender=GuestReport, signal=signals.pre_delete)
