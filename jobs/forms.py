from django import forms
from users.models import Company

from .models import Job, Application


class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location',
                  'job_type', 'salary',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['salary'].required = False

    def save(self, user=None):
        job = super().save(commit=False)
        if user:
            job.company = Company.objects.get(user=user)
        job.save()
        return job


class JobEditForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location',
                  'job_type', 'salary', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['salary'].required = False


class JobApplyForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ['cover_letter']
