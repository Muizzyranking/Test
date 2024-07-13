from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = CountryField()
    zip = models.IntegerField()
    is_company = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    about = models.TextField(blank=True)
    logo = models.ImageField(upload_to="logos/", blank=True)

    def __str__(self):
        return self.company_name


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True)

    def __str__(self):
        return self.user.username
