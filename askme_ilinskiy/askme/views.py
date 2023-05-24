from . import models

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseServerError


# Create your views here.
def index(request):
    try:
        page_num = request.GET.get('page_num', 0)
        page_num = int(page_num)
    except ValueError:
        page_num = 0
    COUNT_PAGES = 20
    res_pagination = models.paginate(page_num, COUNT_PAGES, models.QUESTIONS)
    try:
        pagination = res_pagination["pagination"]
        questions = res_pagination["cur_arr"]
    except KeyError:
        return HttpResponseServerError()
    context = {"questions": questions, "tags": models.TAGS, "best_members": models.BEST_MEMBERS,
               "paginator": pagination}
    return render(request, "index.html", context)


def popularPosts(request):
    try:
        page_num = request.GET.get('page_num', 0)
        page_num = int(page_num)
    except ValueError:
        page_num = 0
    COUNT_PAGES = 20
    res_pagination = models.paginate(page_num, COUNT_PAGES, models.QUESTIONS)
    try:
        pagination = res_pagination["pagination"]
        questions = res_pagination["cur_arr"]
    except KeyError:
        return HttpResponseServerError()
    context = {"questions": questions, "tags": models.TAGS, "best_members": models.BEST_MEMBERS,
               "paginator": pagination}
    return render(request, "popular_posts.html", context)

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
