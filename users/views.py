from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404

from users.forms import ApplicantEditForm, ApplicantSignUpForm
from users.forms import CompanyEditForm,  CompanySignUpForm
from users.models import User, Company, Applicant
from jobs.models import Job, Application
from typing import Any


def company_profile(request: HttpRequest, company: str) -> HttpResponse:
    """
   View to display the profile of a company along with its posted jobs.

   Args:
       request (HttpRequest): The HTTP request object.
       company (str): The name of the company to retrieve.

   Returns:
       HttpResponse: The rendered company profile page, or a redirect to the
                     home page if the company does not exist.
   """
    try:
        company = Company.objects.get(company_name__iexact=company)
    except Company.DoesNotExist:
        messages.error(request, "Company not found.")
        return redirect('home')
    jobs: QuerySet[Job] = Job.objects.filter(company=company)
    context: dict[str, Any] = {'company': company, 'jobs': jobs}
    return render(request, 'users/company/profile.html', context)


@login_required(login_url='/login/')
def edit_company_profile(request):
    """
    View to handle the editing of a company's profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered company edit page, or a redirect to
                      the home page if the user is not a company
                      or if the company does not exist.
    """
    if not request.user.is_company:
        messages.error(request, "Something went wrong.")
        return redirect('home')
    try:
        company = get_object_or_404(Company, user=request.user)
    except [Company.DoesNotExist, Http404]:
        messages.error(request, "Something went wrong.")
        return redirect('home')
    if request.method == 'POST':
        form = CompanyEditForm(request.POST, request.FILES,
                               instance=company, user=request.user)
        if form.is_valid():
            company = form.save(commit=False)
            company.user.email = form.cleaned_data['email']
            company.user.username = form.cleaned_data['username']
            company.user.first_name = form.cleaned_data['first_name']
            company.user.last_name = form.cleaned_data['last_name']
            company.user.address = form.cleaned_data['address']
            company.user.city = form.cleaned_data['city']
            company.user.country = form.cleaned_data['country']
            company.user.zip = form.cleaned_data['zip']
            company.user.save()
            company.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('company', company.company_name)
    else:
        form = CompanyEditForm(instance=company, user=request.user)

    return render(request, 'users/company/edit.html', {'form': form})


def applicant_profile(request: HttpRequest, username: str) -> HttpResponse:
    try:
        id = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('home')
    profile = Applicant.objects.get(user=id)
    if profile is None:
        messages.error(request, "User not found.")
        return redirect('home')
    applications = Application.objects.filter(
        applicant__user=id).order_by('-application_date')
    context = {'profile': profile, 'applications': applications}
    return render(request, 'users/applicant/profile.html', context)


@login_required(login_url='/login/')
def edit_applicant_profile(request):
    if not request.user.is_applicant:
        messages.error(request, "Something went wrong.")
        return redirect('home')
    try:
        applicant = get_object_or_404(Applicant, user=request.user)
    except [Applicant.DoesNotExist, Http404]:
        messages.error(request, "Something went wrong.")
        return redirect('home')
    if request.method == 'POST':
        form = ApplicantEditForm(request.POST, request.FILES,
                                 instance=applicant, user=request.user)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.user.email = form.cleaned_data['email']
            applicant.user.username = form.cleaned_data['username']
            applicant.user.first_name = form.cleaned_data['first_name']
            applicant.user.last_name = form.cleaned_data['last_name']
            applicant.user.address = form.cleaned_data['address']
            applicant.user.city = form.cleaned_data['city']
            applicant.user.country = form.cleaned_data['country']
            applicant.user.zip = form.cleaned_data['zip']
            applicant.user.save()
            applicant.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('home')
    else:
        form = ApplicantEditForm(instance=applicant, user=request.user)

    return render(request, 'users/applicant/edit.html', {'form': form})


@login_required(login_url='/login/')
def feed(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/feed.html')


def login_user(request: HttpRequest) -> HttpResponse:
    """
    Handle user login process.

    This view function manages the user login process.
    It performs the following tasks:
    1. Redirects authenticated users to the home page.
    2. Displays a message if the user was redirected from a protected page.
    3. Processes login form submission.
    4. Authenticates the user and logs them in if credentials are valid.
    5. Redirects the user post-login, either to a specified 'next' URL
                        or the home page.
    6. Handles and displays appropriate messages for various scenarios.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered login page or redirect response.

    Raises:
        None
    """
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home')
    if 'next' in request.GET:
        messages.info(request, "You need to login first.")
    if request.method == "POST":
        form: AuthenticationForm = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username: str = form.cleaned_data.get("username")
            password: str = form.cleaned_data.get("password")
            user: User | None = authenticate(
                username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {user.username}!")
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form: AuthenticationForm = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('home')


def register(request: HttpRequest) -> HttpResponse:
    """
    User registeration view
    """
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home')
    return render(request, 'users/register/register.html')


def register_company(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home')
    if request.method == "POST":
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Registration Successful!"))
            return redirect("login")
    else:
        form = CompanySignUpForm()

    return render(request, 'users/register/company.html', {'form': form})


def register_applicant(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home')
    if request.method == "POST":
        form = ApplicantSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Registration Successful!"))
            return redirect("login")
    else:
        form = ApplicantSignUpForm()

    return render(request, 'users/register/applicant.html', {'form': form})
