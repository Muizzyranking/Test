from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from users.models import Company, Applicant


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    salary = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    applicants = models.ManyToManyField(Applicant, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}. Active: {self.is_active}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            while Job.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{base_slug}-{get_random_string(4)}'
            self.slug = unique_slug
        super().save(*args, **kwargs)


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('interview', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted')
    ], default='pending')
    cover_letter = models.TextField()

    def __str__(self):
        return f"{self.applicant.user.username} applied for {self.job.title}"
