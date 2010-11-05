"""
Print the email address of each active user to stdout on a separate line.
To sort the output and remove duplicates, run with the following command:
    python print_email_addresses.py | sort -u
"""
from project.fae.models import User

#------------------------------------------------
def list_email_addresses():
    users = User.objects.all()
    for user in users:
        if user.is_active:
            print user.email

#------------------------------------------------
def main():
    list_email_addresses()

if __name__ == "__main__":
    main()
