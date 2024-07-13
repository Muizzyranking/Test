from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("register/applicant/", views.register_applicant,
         name="register_applicant"),
    path("register/company/", views.register_company, name="register_company"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("feed/", views.feed, name="feed"),
    path("company/<str:company>", views.company_profile, name="company"),
    path("user/<str:username>", views.applicant_profile, name="user"),
    path("edit/company", views.edit_company_profile, name="edit_company"),
    path("edit/profile", views.edit_applicant_profile, name="edit_profile"),
]
