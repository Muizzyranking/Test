from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField

from .models import Applicant, Company


class CompanySignUpForm(UserCreationForm):
    company = forms.CharField(max_length=100, required=True)
    website = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username',
                  'address', 'city', 'country', 'zip', 'password1',
                  'password2']

    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.save()
        Company.objects.create(user=user,
                               company_name=self.cleaned_data['company'],
                               website=self.cleaned_data['website'])
        return user


class CompanyEditForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    country = CountryField()
    zip = forms.CharField(max_length=100)
    country = CountryField().formfield()

    class Meta:
        model = Company
        fields = ['company_name', 'about', 'website', 'logo']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['address'].initial = user.address
            self.fields['city'].initial = user.city
            self.fields['country'].initial = user.country
            self.fields['zip'].initial = user.zip


class ApplicantSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username',
                  'address', 'city', 'country', 'zip', 'password1',
                  'password2']

    def save(self):
        user = super().save(commit=False)
        user.is_applicant = True
        user.save()
        Applicant.objects.create(user=user)
        return user


class ApplicantEditForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    country = CountryField()
    zip = forms.CharField(max_length=100)
    country = CountryField().formfield()

    class Meta:
        model = Applicant
        fields = ['about', 'resume']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['address'].initial = user.address
            self.fields['city'].initial = user.city
            self.fields['country'].initial = user.country
            self.fields['zip'].initial = user.zip
