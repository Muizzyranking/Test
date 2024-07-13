from django.contrib import admin
from users.models import User, Company, Applicant
from jobs.models import Job, Application

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Applicant)
admin.site.register(Application)
