from django.urls import path
from . import views


urlpatterns = [
    path("jobs/", views.all_jobs, name="jobs"),
    path("add_job/", views.add_job, name="add-job"),
    path("job/<slug:slug>/", views.job_details, name="job"),
    path("edit/<slug:slug>/", views.edit_job, name="edit-job"),
    path("delete/<slug:slug>/", views.delete_job, name="delete-job"),
    path("apply/<slug:slug>/", views.apply_to_job, name="apply"),
    path("applications/", views.applications, name="applications"),
    path("application/<slug:slug>", views.application,
         name="application-details"),
    path('update_application/<int:id>/',
         views.update_application_status, name='update-application-status')
]
