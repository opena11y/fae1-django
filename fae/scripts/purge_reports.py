"""
Purge report metadata and results files (which happens automagically via
signals) for both UserReport and GuestReport tables.

This script is intended to be run as a cron job. It uses two different
algorithms for purging records from the two respective report tables.
Regardless of table, no report is purged unless the stats field is set,
indicating that usage stats have been collected for the report.

GuestReport: 
Each time it runs, the script gets the latest date from the PurgeStats
table to use as its start_date and the latest date from the UsageStats
table to use as its end_date.


UserReport:
Each time it runs, the script purges reports for each user that meet the
following conditions: (1) timestamp is lte cutoff_date (2) the archive
field is not set (3) the report is not one of the latest N reports, where
N is the setting for user account type buffer.
"""
import datetime
import logging
import os
from django.core.exceptions import ObjectDoesNotExist

from project.settings import ACCT_TYPE_BUFFER, DEFAULT_BUFFER
from project.fae.models import User, UserReport, GuestReport, PurgeStats, UsageStats
from project.fae.scripts import utils

#------------------------------------------------
def purge_user_reports(cutoff_date):
    users = User.objects.all()
    count = 0
    for user in users:
        try:
            profile = user.get_profile()
            buffer = ACCT_TYPE_BUFFER[profile.acct_type]
        except ObjectDoesNotExist:
            buffer = DEFAULT_BUFFER
        reports = UserReport.objects.filter(user=user).exclude(timestamp__gt=cutoff_date)
        reports = reports.exclude(archive=True).order_by('-timestamp')[buffer:]
        user_count = 0
        for report in reports:
            if report.stats:
                report.delete()
                user_count += 1
        if user_count:
            logging.info("Deleted %2d UserReports created by %s", user_count, user.username)
            count += user_count
    return count

#------------------------------------------------
def purge_guest_reports(date):
    reports = utils.get_reports_by_date(GuestReport, date)
    count = 0
    for report in reports:
        if report.stats:
            report.delete()
            count += 1

    if count: logging.info("Deleted %3d GuestReports dated %s", count, date)

    stats = PurgeStats(date=date, guest_reports=count)
    stats.save()
    return count

#------------------------------------------------
def main():
    utils.init_logging('purge_reports.log')

    ### GuestReports ###
    start_date = utils.get_latest_date(PurgeStats, 'date') + datetime.timedelta(days=1)
    end_date = utils.get_latest_date(UsageStats, 'date')

    # Since the end_date comes from a different table,
    # ensure that the following condition is met.
    assert start_date <= end_date

    logging.info('--------------------------------------------------------------')
    logging.info("Purging GuestReports starting %s and ending %s", start_date, end_date)

    date = start_date
    while date <= end_date:
        purge_guest_reports(date)
        date += datetime.timedelta(days=1)

    ### UserReports ###
    logging.info('---------------------------------------------------')
    logging.info("Purging UserReports created on or before %s",  end_date)

    count = purge_user_reports(end_date)
    logging.info("Purged %d UserReports total", count)

if __name__ == "__main__":
    main()