from . import models
from django.shortcuts import render


# Create your views here.
def index(request):
    context = {'questions': models.QUESTIONS, 'tags': models.TAGS, "best_members": models.BEST_MEMBERS}
    return render(request, 'index.html', context)


def question(request):
    return render(request, 'question.html')
