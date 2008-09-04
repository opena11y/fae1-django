import datetime, os, sys, time

report_dir = '/var/www/html/fae/wamtout'

def delete_files_before(cutoff):
    os.chdir(report_dir)
    pwd = os.getcwd()
    if pwd != report_dir:
        print 'Invalid directory:', report_dir
        sys.exit(0)

    filenames = os.listdir('.')
    success = 0

    for filename in filenames:
        fstat = os.stat(filename)
        mtime = fstat.st_mtime
        if mtime < cutoff:
            print "Deleting", filename, datetime.datetime.fromtimestamp(mtime)
            try:
                os.remove(filename)
                success += 1
            except OSError, err:
                print "Unable to delete", filename, ":", err
                pass

    print "Deleted", success, "files from", report_dir
                                        
#------------------------------------------------
def get_cutoff_date():
    # Get current system date
    today = datetime.date.today()

    # Ask user for cutoff date (expect yyyy-mm-dd format)
    prompt = 'Cutoff date: '
    response = raw_input(prompt)

    # Convert date string to datetime.date object
    (year, month, day) = response.split('-')
    input_date = datetime.date(int(year), int(month), int(day))

    if today < input_date:
        print 'Date is in the future!'
        sys.exit(0)

    return input_date

#------------------------------------------------
def main():
    cutoff = get_cutoff_date()
    epoch_seconds = time.mktime(cutoff.timetuple())
    delete_files_before(epoch_seconds)

if __name__ == "__main__":
    main()
