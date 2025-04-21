from django.contrib import admin

from jobproject.models import JobOpening


class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ["applied", "company", "title", "active", "status"]
    list_filter = ["active", "status"]
    search_fields = ["company", "title", "url", "status"]


admin.site.register(JobOpening, JobOpeningAdmin)
