from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("", include("users.urls")),
    path("", include("jobs.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
