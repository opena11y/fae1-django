"""
Delete reports not marked for archiving for the specified
username (or all users if "all" is specified).

"""
import sys
from django.core.exceptions import ObjectDoesNotExist
from project.fae.models import User, UserReport

#------------------------------------------------
def delete_user_reports(username):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        print 'Username', username, 'not found!'
        sys.exit(0)

    count = 0
    reports = UserReport.objects.filter(user=user)
    reports = reports.exclude(archive=True)
    for report in reports:
        if report.stats:
            report.delete()
            # print report.title
            count += 1
    return count

#------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print 'Please provide username argument!'
        sys.exit(0)
    username = sys.argv[1]
    count = delete_user_reports(username)
    print 'Deleted', count, 'reports!'

if __name__ == "__main__":
    main()
