from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import os
import subprocess

# rm commands in two flavors
user_rm = ['rm', '-f']
sudo_rm = ['sudo', '-u', 'apache'] + user_rm

def remove_file(filename):
    # If running under apache, user_rm works okay.
    cmd = user_rm
    cmd.append(filename)
    retval = subprocess.call(cmd)
    if retval == 0: return
    # Need sudo_rm command with standalone script.
    cmd = sudo_rm
    cmd.append(filename)
    subprocess.call(cmd)

# The built-in Django User relation:

#class User(models.Model):
#   username      = models.CharField(max_length=30, unique=True)
#   first_name    = models.CharField(max_length=30, blank=True)
#   last_name     = models.CharField(max_length=30, blank=True)
#   email         = models.EmailField(blank=True)
#   password      = models.CharField(max_length=128)
#   is_staff      = models.BooleanField(default=False)
#   is_active     = models.BooleanField(default=True)
#   is_superuser  = models.BooleanField(default=False)
#   last_login    = models.DateTimeField()
#   date_joined   = models.DateTimeField()

# Custom classes for FAE

class Organization(models.Model):
    ORG_TYPE_CHOICES = (
        (1, 'Other'),
        (2, 'Level 2'),
        (3, 'Level 3'),
        (4, 'Level 4'),
        (5, 'Partner'),
    )

    name          = models.CharField(max_length=128)
    org_type      = models.IntegerField(choices=ORG_TYPE_CHOICES)
    url           = models.URLField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

    class Admin:
        pass

class UserProfile(models.Model):
    ACCT_TYPE_CHOICES = (
        (1, 'Standard'),
        (2, 'Level 2'),
        (3, 'Level 3'),
        (4, 'Level 4'),
        (5, 'Unlimited'),
    )

    user          = models.ForeignKey(User, unique=True)
    acct_type     = models.IntegerField(choices=ACCT_TYPE_CHOICES, default=1)
    org           = models.ForeignKey(Organization)

    def __unicode__(self):
        return self.user.username

    class Admin:
        pass

class EmailSuffix(models.Model):
    suffix        = models.CharField(max_length=128, primary_key=True)
    org           = models.ForeignKey(Organization)

    def __unicode__(self):
        return self.suffix

    class Meta:
        ordering = ["suffix"]

    class Admin:
        pass

class UserReport(models.Model):
    id            = models.CharField(max_length=30, primary_key=True)
    user          = models.ForeignKey(User)
    timestamp     = models.DateTimeField()
    pgcount       = models.IntegerField()
    url           = models.URLField()
    urlcount      = models.IntegerField()
    depth         = models.IntegerField()
    title         = models.CharField(max_length=128, blank=True)
    archive       = models.BooleanField(default=False)
    stats         = models.BooleanField(default=False)

    def __unicode__(self):
        return self.id

    def get_absolute_url(self):
        return '/report/%s/summary/' % self.id

    def get_filename(self):
        return os.path.join(settings.USER_REPORTS_DIR, self.id + '.xml')

    def remove_results_file(self):
        remove_file(self.get_filename())

    class Meta:
        ordering = ["-timestamp"]

    class Admin:
        pass

class GuestReport(models.Model):
    id            = models.CharField(max_length=30, primary_key=True)
    timestamp     = models.DateTimeField()
    pgcount       = models.IntegerField()
    url           = models.URLField()
    stats         = models.BooleanField(default=False)

    def __unicode__(self):
        return self.id

    def get_filename(self):
        return os.path.join(settings.GUEST_REPORTS_DIR, self.id + '.xml')

    def remove_results_file(self):
        remove_file(self.get_filename())

    class Meta:
        ordering = ["-timestamp"]

    class Admin:
        pass

class UsageStats(models.Model):
    date          = models.DateField(primary_key=True)
    user_reports  = models.IntegerField()
    user_pgcount  = models.IntegerField()
    guest_reports = models.IntegerField()
    guest_pgcount = models.IntegerField()
    depth_1       = models.IntegerField()
    depth_2       = models.IntegerField()

    class Meta:
        get_latest_by = "date"

    class Admin:
        pass

class PurgeStats(models.Model):
    date          = models.DateField(primary_key=True)
    guest_reports = models.IntegerField()

    class Meta:
        get_latest_by = "date"

    class Admin:
        pass
