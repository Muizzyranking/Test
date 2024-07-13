from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JobApplyForm, JobPostForm, JobEditForm
from .models import Job, Application
from users.models import Applicant


def job_details(request: HttpRequest, slug: str) -> HttpResponse:
    job = Job.objects.get(slug=slug)
    return render(request, 'jobs/job_details.html', {'job': job})


def all_jobs(request: HttpRequest) -> HttpResponse:
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'jobs/all_jobs.html', {'jobs': jobs})


@login_required(login_url='/login/')
def apply_to_job(request, slug):
    if request.user.is_company:
        messages.error(request, 'You cannot apply to a job.')
        return redirect('home')
    job = get_object_or_404(Job, slug=slug)
    applicant = get_object_or_404(Applicant, user=request.user)

    if not applicant.resume:
        messages.error(
            request, 'You must upload a resume before applying.')
        return redirect('edit_profile')

    try:
        applied = Application.objects.get(job=job, applicant=applicant)
        is_applied = True
    except Application.DoesNotExist:
        applied = None
        is_applied = False

    if request.method == 'POST':
        form = JobApplyForm(request.POST, instance=applied)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = applicant
            application.resume = applicant.resume
            application.save()
            if is_applied:
                messages.success(
                    request, 'Your application has been updated.')
            else:
                messages.success(
                    request, 'Your application has been submitted.')
            return redirect('job', slug=job.slug)
    else:
        form = JobApplyForm(instance=applied)

    context = {'form': form, 'job': job}

    return render(request, 'jobs/apply.html', context)


@login_required(login_url='/login/')
def add_job(request: HttpRequest) -> HttpResponse:
    user = request.user
    if not user.is_company:
        messages.error(request, "Something went wrong")
        return redirect('home')
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            form.save(user=user)
            messages.success(request, "Job Posted Successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid Form Data.")
    else:
        form = JobPostForm()
    return render(request, 'jobs/add_job.html', {'form': form})


@login_required(login_url='/login/')
def edit_job(request: HttpRequest, slug: str) -> HttpResponse:
    user = request.user
    if not user.is_company:
        messages.error(request, "Something went wrong")
        return redirect('home')
    job = get_object_or_404(Job, slug=slug)

    if job.company.user != user:
        messages.error(request, "Something went wrong")
        return redirect('home')

    if request.method == 'POST':
        form = JobEditForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job Updated Successfully!")
            return redirect('job', slug=slug)
        else:
            messages.error(request, "Invalid Form Data.")
    else:
        form = JobEditForm(instance=job)
    return render(request, 'jobs/edit_job.html', {'form': form})


@login_required(login_url='/login/')
def delete_job(request: HttpRequest, slug: str) -> HttpResponse:
    """
    View to handle the deletion of a job.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the job to be deleted.

    Returns:
        HttpResponse: A redirect to the company's profile page if the
                    deletion is successful, or a redirect to the home page
                    if the user is not the job's owner or a company.
    """
    user = request.user
    if not user.is_company:
        messages.error(request, "Something went wrong")
        return redirect('home')
    job = get_object_or_404(Job, slug=slug)
    if job.company.user != user:
        messages.error(request, "Something went wrong")
        return redirect('home')
    job.delete()
    messages.success(request, "Job Deleted Successfully!")
    return redirect('company', user.company.company_name)


@login_required(login_url='/login/')
def applications(request):
    user = request.user
    if user.is_company:
        jobs = Job.objects.filter(company__user=user).order_by('-created_at')
        applications = Application.objects.filter(
            job__in=jobs)
        context = {'applications': applications, 'jobs': jobs}
        return render(request, 'jobs/applications/company.html', context)
    elif user.is_applicant:
        applications = Application.objects.filter(
            applicant__user=user).order_by('-application_date')
        context = {'applications': applications}
        return render(request, 'jobs/applications/applicant.html', context)


@login_required(login_url='/login/')
def application(request, slug):
    user = request.user
    if not user.is_company:
        messages.error(request, 'You cannot access this page.')
        return redirect('home')
    if user.is_company:
        job = Job.objects.get(slug=slug)
        application = Application.objects.filter(
            job=job)

    status_choices = Application._meta.get_field('status').choices
    context = {'applications': application,
               'jobs': job, 'status_choices': status_choices}

    return render(request, 'jobs/application-detail.html', context)


@login_required(login_url='/login/')
def update_application_status(request, id):
    application = get_object_or_404(Application, id=id)
    job = application.job
    if request.method == 'POST':
        new_status = request.POST.get('status')
        status_choices = dict(Application._meta.get_field('status').choices)
        if new_status in status_choices:
            application.status = new_status
            application.save()
            messages.success(
                request, 'Application status updated successfully.')
        else:
            messages.error(request, 'Invalid status selected.')
    return redirect('application-details', slug=job.slug)
