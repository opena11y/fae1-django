from django.db import models
from django.contrib.auth.models import User

# The built-in Django User relation:

#class User(models.Model):
#   username      = models.CharField(maxlength=30, unique=True)
#   first_name    = models.CharField(maxlength=30, blank=True)
#   last_name     = models.CharField(maxlength=30, blank=True)
#   email         = models.EmailField(blank=True)
#   password      = models.CharField(maxlength=128)
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

    name          = models.CharField(maxlength=128)
    org_type      = models.IntegerField(choices=ORG_TYPE_CHOICES)
    url           = models.URLField()

    def __str__(self):
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
    acct_type     = models.IntegerField(choices=ACCT_TYPE_CHOICES)
    org           = models.ForeignKey(Organization)
    reg_date      = models.DateTimeField()
    reg_key       = models.CharField(maxlength=30)

    def __str__(self):
        return self.user.username

    class Admin:
        pass

class EmailSuffix(models.Model):
    suffix        = models.CharField(maxlength=128, primary_key=True)
    org           = models.ForeignKey(Organization)

    def __str__(self):
        return self.suffix

    class Meta:
        ordering = ["suffix"]

    class Admin:
        pass

class UserReport(models.Model):
    id            = models.CharField(maxlength=30, primary_key=True)
    user          = models.ForeignKey(User)
    timestamp     = models.DateTimeField()
    pgcount       = models.IntegerField()
    url           = models.URLField()
    urlcount      = models.IntegerField()
    depth         = models.IntegerField()
    title         = models.CharField(maxlength=128, blank=True)
    delete        = models.BooleanField(default=False)
    stats         = models.BooleanField(default=False)

    def __str__(self):
        return self.reportid

    class Meta:
        ordering = ["-timestamp"]

    class Admin:
        pass

class GuestReport(models.Model):
    id            = models.CharField(maxlength=30, primary_key=True)
    timestamp     = models.DateTimeField()
    pgcount       = models.IntegerField()
    url           = models.URLField()
    stats         = models.BooleanField(default=False)

    def __str__(self):
        return self.reportid

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
    depth_2       = models.IntegerField()
    depth_3       = models.IntegerField()

    class Admin:
        pass
