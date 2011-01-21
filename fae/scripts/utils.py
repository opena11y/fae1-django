import datetime
import logging
import os

from project.settings import MAINTENANCE_LOG, MAINTENANCE_FMT

#------------------------------------------------
def get_logger(name):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create file handler
    fh = logging.FileHandler(MAINTENANCE_LOG)
    fh.setLevel(logging.INFO)
    fh.setFormatter(MAINTENANCE_FMT)

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(MAINTENANCE_FMT)

    #add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

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
