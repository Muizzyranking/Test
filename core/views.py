from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse


def home(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect(reverse('jobs'))
    return render(request, "core/home.html")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "core/home.html")
