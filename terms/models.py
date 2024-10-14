from django.db import models


class ContactFormSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class DataDownload(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Data downloaded by {self.email} at {self.timestamp}"