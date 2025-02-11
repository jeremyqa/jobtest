from django.contrib import admin

from jobproject.models import JobOpening


class JobOpeningAdmin(admin.ModelAdmin):
    pass

admin.site.register(JobOpening, JobOpeningAdmin)
