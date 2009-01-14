from django.contrib import admin
from project.fae import models

admin.site.register(models.Organization)
admin.site.register(models.UserProfile)
admin.site.register(models.EmailSuffix)
admin.site.register(models.UserReport)
admin.site.register(models.GuestReport)
admin.site.register(models.UsageStats)
