"""
Purge report metadata and results files (which happens automagically via
signals) for both UserReport and GuestReport tables.

This script is intended to be run as a cron job. It uses similar methods
for purging records from the two respective report tables. Regardless of
table, no report is purged unless the stats field is set, indicating that
usage stats have been collected for the report.

The cutoff_time that is passed into each of the purge functions is derived
from the end_date, which is retrieved as the latest date in the UsageStats
table. Since a timestamp in the report table must be compared to this date,
a timedelta(days=1) is added to the end_date to compute the cutoff_time.

GuestReport: 
Each time it runs, the script purges all GuestReport records with
timestamp value less than the cutoff_time.

UserReport:
Each time it runs, the script purges reports for each user that meet the
following conditions: (1) timestamp is lt cutoff_time (2) the archive
field is not set (3) the report is not one of the latest N reports, where
N is the setting for user account type buffer.
"""
import datetime
import logging
import os
from django.core.exceptions import ObjectDoesNotExist

from project.settings import ACCT_TYPE_BUFFER, DEFAULT_BUFFER
from project.fae.models import User, UserReport, GuestReport, UsageStats
from project.fae.scripts import utils

#------------------------------------------------
def purge_user_reports(cutoff_time):
    users = User.objects.all()
    count = 0
    for user in users:
        try:
            profile = user.get_profile()
            buffer = ACCT_TYPE_BUFFER[profile.acct_type]
        except ObjectDoesNotExist:
            buffer = DEFAULT_BUFFER
        reports = UserReport.objects.filter(user=user, timestamp__lt=cutoff_time)
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
def purge_guest_reports(cutoff_time):
    reports = GuestReport.objects.filter(timestamp__lt=cutoff_time)
    count = 0
    for report in reports:
        if report.stats:
            report.delete()
            count += 1
    return count

#------------------------------------------------
def main():
    utils.init_logging('purge_reports.log')
    end_date = utils.get_latest_date(UsageStats, 'date')
    cutoff_time = end_date + datetime.timedelta(days=1)

    ### GuestReports ###
    logging.info('----------------------------------------------------')
    logging.info("Purging GuestReports created on or before %s", end_date)

    count = purge_guest_reports(cutoff_time)
    logging.info("Purged %d GuestReports total", count)

    ### UserReports ###
    logging.info('---------------------------------------------------')
    logging.info("Purging UserReports created on or before %s", end_date)

    count = purge_user_reports(cutoff_time)
    logging.info("Purged %d UserReports total", count)

if __name__ == "__main__":
    main()
