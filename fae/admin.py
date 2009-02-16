from django.contrib import admin
from project.fae import models

admin.site.register(models.Organization)
admin.site.register(models.UserProfile)
admin.site.register(models.EmailSuffix)

class UserReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'timestamp', 'archive')
    ordering = ('user',)
    list_filter = ('archive', 'user')

admin.site.register(models.UserReport, UserReportAdmin)

admin.site.register(models.GuestReport)
admin.site.register(models.UsageStats)
