import datetime
import logging
import os

from project.settings import PURGE_DAYS_OFFSET as DAYS_OFFSET
from project.fae.models import UserReport, GuestReport, PurgeStats
from project.fae.scripts import utils

#------------------------------------------------
def purge_user_reports(date):
    reports = utils.get_reports_by_date(UserReport, date)
    count = 0
    for report in reports:
        if not report.archive and report.stats:
            report.delete()
            count += 1
    if count: logging.info("Deleted %3d UserReports  for %s", count, date)
    return count

#------------------------------------------------
def purge_guest_reports(date):
    reports = utils.get_reports_by_date(GuestReport, date)
    count = 0
    for report in reports:
        if report.stats:
            report.delete()
            count += 1
    if count: logging.info("Deleted %3d GuestReports for %s", count, date)
    return count

#------------------------------------------------
def purge_reports(date):
    stats = PurgeStats(
        date=date,
        user_reports = 0,
        guest_reports = 0
        )

    stats.user_reports = purge_user_reports(date)
    stats.guest_reports = purge_guest_reports(date)

    count = stats.user_reports + stats.guest_reports
    if count:
        logging.debug(
            "%s: user_reports: %d guest_reports: %d",
            stats.date,
            stats.user_reports,
            stats.guest_reports)
        stats.save()

#------------------------------------------------
def main():
    utils.init_logging('purge_reports.log')
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    start_date = utils.get_latest_date(PurgeStats, 'date') + datetime.timedelta(days=1)
    end_date = datetime.date.today() - datetime.timedelta(days=DAYS_OFFSET)

    # DO NOT process records created today
    assert start_date <= yesterday and end_date <= yesterday

    logging.info('---------------------------------------------------------')
    logging.info("Purging reports starting %s and ending %s", start_date, end_date)

    date = start_date
    while date <= end_date:
        purge_reports(date)
        date += datetime.timedelta(days=1)

if __name__ == "__main__":
    main()
