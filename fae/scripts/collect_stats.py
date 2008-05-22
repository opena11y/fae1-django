import datetime
import logging
import os

from project.settings import STATS_DAYS_OFFSET as DAYS_OFFSET
from project.fae.models import UserReport, GuestReport, UsageStats
from project.fae.scripts import utils

#------------------------------------------------
def collect_user_stats(date):
    reports = utils.get_reports_by_date(UserReport, date)
    count = reports.count()
    pgcount = 0
    depth_1 = 0
    depth_2 = 0

    for report in reports:
        pgcount += report.pgcount
        if report.depth == 1: depth_1 += 1
        if report.depth == 2: depth_2 += 1
        report.stats = True
        logging.debug("%s : %s : %s", report.timestamp, report.pgcount, report.depth)
        report.save()

    return (count, pgcount, depth_1, depth_2)

#------------------------------------------------
def collect_guest_stats(date):
    reports = utils.get_reports_by_date(GuestReport, date)
    count = reports.count()
    pgcount = 0

    for report in reports:
        pgcount += report.pgcount
        report.stats = True
        logging.debug('%s : %s', report.timestamp, report.pgcount)
        report.save()

    return (count, pgcount)

#------------------------------------------------
def collect_stats(date):
    stats = UsageStats(
        date=date,
        user_reports = 0,
        user_pgcount = 0,
        guest_reports = 0,
        guest_pgcount = 0,
        depth_1 = 0,
        depth_2 = 0
        )

    count, pgcount, depth_1, depth_2 = collect_user_stats(date)
    if count:
        logging.info("Collected stats from %3d UserReports  for %s", count, date)
        stats.user_reports = count
        stats.user_pgcount = pgcount
        stats.depth_1 = depth_1
        stats.depth_2 = depth_2

    count, pgcount = collect_guest_stats(date)
    if count:
        logging.info("Collected stats from %3d GuestReports for %s", count, date)
        stats.guest_reports = count
        stats.guest_pgcount = pgcount

    count = stats.user_reports + stats.guest_reports
    if count:
        logging.debug(
            "%s: user_reports: %d %d guest_reports: %d %d depth_1: %d depth_2 %d",
            stats.date,
            stats.user_reports,
            stats.user_pgcount,
            stats.guest_reports,
            stats.guest_pgcount,
            stats.depth_1,
            stats.depth_2)
        stats.save()

#------------------------------------------------
def main():
    utils.init_logging('collect_stats.log')
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    start_date = utils.get_latest_date(UsageStats, 'date') + datetime.timedelta(days=1)
    end_date = datetime.date.today() - datetime.timedelta(days=DAYS_OFFSET)

    # DO NOT process records created today
    assert start_date <= yesterday and end_date <= yesterday

    logging.info('---------------------------------------------------------------------')
    logging.info("Collecting usage statistics starting %s and ending %s", start_date, end_date)

    date = start_date
    while date <= end_date:
        collect_stats(date)
        date += datetime.timedelta(days=1)

if __name__ == "__main__":
    main()
