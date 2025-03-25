from django.contrib import admin

from jobproject.models import JobOpening


class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ["applied", "company", "title", "active"]
    list_filter = [
        "active",
    ]
    search_fields = ["company", "title", "url"]


admin.site.register(JobOpening, JobOpeningAdmin)
