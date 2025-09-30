from django.test import TestCase
from django.contrib.auth.models import User
from .models import JobApplications
import datetime

class JobApplicationsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_create_job_application(self):
        # Create a job application
        job_app = JobApplications.objects.create(
            company="Mega Prime Foods",
            job_name="IT",
            job_desc="N/A",
            status="No Response",
            application_date=datetime.date(2025, 8, 15),
            user=self.user
        )

        # Assertions to verify the object was created correctly
        self.assertEqual(job_app.company, "Mega Prime Foods")
        self.assertEqual(job_app.status, "No Response")
        self.assertEqual(job_app.user.username, "testuser")
