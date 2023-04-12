from . import models
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def index(request):
    context = {"questions": models.QUESTIONS, "tags": models.TAGS, "best_members": models.BEST_MEMBERS}
    return render(request, "index.html", context)


def login(request):
    context = {"tags": models.TAGS, "best_members": models.BEST_MEMBERS}
    return render(request, "login.html", context)


def register(request):
    context = {"tags": models.TAGS, "best_members": models.BEST_MEMBERS}
    return render(request, "register.html", context)
