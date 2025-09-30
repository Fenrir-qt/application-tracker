from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class JobApplications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=255, null=False)
    job_name = models.CharField(max_length=255, null=False)
    job_desc = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=255, null=False)
    application_date = models.DateField(null=False)
