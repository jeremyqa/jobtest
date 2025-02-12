from django.contrib import admin

from jobproject.models import JobOpening

class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ["created", "company", "applied", "active"]

admin.site.register(JobOpening, JobOpeningAdmin)
