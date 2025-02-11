from django.db import models

class JobOpening(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    applied = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)
    notes = models.TextField(null=True)
    url = models.URLField()
    company = models.CharField(max_length=255)
    title = models.CharField()
    location = models.CharField()

    def __str__(self) -> str:
        return f"JobOpening: `{self.title}` @ `{self.company}`"

