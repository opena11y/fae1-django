import datetime
import logging
import os

from project.settings import LOGS_DIR

#------------------------------------------------
def init_logging(filename):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%a %d %b %Y %H:%M:%S',
        filename=os.path.join(LOGS_DIR, filename),
        filemode='a')

    console = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

#------------------------------------------------
def get_latest_date(model, fieldname):
    try:
        record = model.objects.latest(fieldname)
        return getattr(record, fieldname)
    except model.DoesNotExist:
        return datetime.date(2009, 3, 1)

#------------------------------------------------
def get_reports_by_date(model, date):
    year = model.objects.filter(timestamp__year=date.year)
    month = year.filter(timestamp__month=date.month)
    return month.filter(timestamp__day=date.day)
