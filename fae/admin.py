from django.contrib import admin
from django.contrib.auth.models import User
from project.fae import models

admin.site.register(models.Organization)
admin.site.register(models.UserProfile)
admin.site.register(models.EmailSuffix)

class UserReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'timestamp', 'stats', 'archive')
    ordering = ('user__username',)
    list_filter = ('timestamp', 'archive', 'stats')
    search_fields = ('user__username', 'user__last_name', 'user__first_name')

admin.site.register(models.UserReport, UserReportAdmin)

class GuestReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'url', 'stats')
    ordering = ('-timestamp',)
    list_filter = ('stats',)

admin.site.register(models.GuestReport, GuestReportAdmin)

class UsageStatsAdmin(admin.ModelAdmin):
    list_display = ('date', 'user_reports', 'user_pgcount', 'guest_reports', 'guest_pgcount')
    ordering = ('-date',)
    list_filter = ('date',)

admin.site.register(models.UsageStats, UsageStatsAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_staff')
    ordering = ('username',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'last_name', 'first_name')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
