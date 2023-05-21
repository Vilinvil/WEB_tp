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


def settings(request):
    context = {"tags": models.TAGS, "best_members": models.BEST_MEMBERS, "author": models.AUTHOR}
    return render(request, "settings.html", context)


def new_question(request):
    context = {"tags": models.TAGS, "best_members": models.BEST_MEMBERS}
    return render(request, "new_question.html", context)


def tags(request, tag_id):
    res = []
    for question in models.QUESTIONS:
        tags_list = [tag['name'] for tag in question['tags']]
        for tag in tags_list:
            if int(tag[3:]) == tag_id:
                res.append(question)
    context = {"questions": res, "tags": models.TAGS, "best_members": models.BEST_MEMBERS, "target_tag": tag_id}
    return render(request, "tags.html", context)


def questionById(request, user_id):
    # Добавить валидацию
    context = {"tags": models.TAGS, "best_members": models.BEST_MEMBERS, "question": models.QUESTIONS[user_id],
               "answers": models.ANSWERS}
    return render(request, "question_by_id.html", context)
