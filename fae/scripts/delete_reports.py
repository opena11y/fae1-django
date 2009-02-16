"""
Delete reports created by specified username,
or all users if "all" is specified.

"""
import datetime, sys
from django.core.exceptions import ObjectDoesNotExist
from project.fae.models import User, UserReport

DEBUG = False
EXCLUDE_ARCHIVED = True
EXCLUDE_NO_STATS = False

#------------------------------------------------
def confirm_date():
    # Get current system date
    today = datetime.date.today()

    # Ask user for current date (expect yyyy-mm-dd format)
    prompt = 'Today\'s date: '
    response = raw_input(prompt)

    # Convert date string to datetime.date object
    (year, month, day) = response.split('-')
    input_date = datetime.date(int(year), int(month), int(day))

    if today != input_date:
        print 'Date is incorrect!'
        sys.exit(0)

#------------------------------------------------
def delete_user_reports(user):
    reports = UserReport.objects.filter(user=user)

    # Exclude based on the following criteria
    if EXCLUDE_ARCHIVED: reports = reports.exclude(archive=True)
    if EXCLUDE_NO_STATS: reports = reports.exclude(stats=False)

    count = reports.count()
    if not count:
        print 'No reports found for user', user.username
        return

    # Get confirmation before deleting
    prompt = 'Delete ' + str(count) + ' report(s) for user ' + user.username + '? (yes | no) '
    response = raw_input(prompt)

    if response == 'yes':
        for report in reports:
            if DEBUG:
                print user.username + ':', report.title
            else:
                report.delete()
    else:
        print 'Aborted!'

#------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print 'Please provide username argument!'
        sys.exit(0)

    if not DEBUG: confirm_date()

    username = sys.argv[1]
    if username == 'all':
        users = User.objects.all()
        for user in users:
            delete_user_reports(user)
    else:
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            print 'Username', username, 'not found!'
            sys.exit(0)
        delete_user_reports(user)

if __name__ == "__main__":
    main()
