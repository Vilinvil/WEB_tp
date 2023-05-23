from . import models
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def index(request):
    try:
        page_num = request.GET.get('page_num', 0)
        page_num = int(page_num)
    except ValueError:
        page_num = 0
    questions = models.QUESTIONS[page_num * 20:(page_num + 1) * 20]
    pagination = {"pages": []}
    if len(models.QUESTIONS[(page_num - 1) * 20:page_num * 20]) != 0:
        pagination["pages"].append({"idPage": page_num - 1, "isActive": False})
        pagination["isExistPrev"] = True

    if len(models.QUESTIONS[(page_num ) * 20:(page_num + 1) * 20]) == 0:
        page_num = 0
        questions = models.QUESTIONS[page_num * 20:(page_num + 1) * 20]
        pagination = {"pages": [{"idPage": page_num, "isActive": True}]}
        pagination["isExistPrev"] = False
    else:
        pagination["pages"].append({"idPage": page_num, "isActive": True})

    i = 1
    while i < 3:
        if len(models.QUESTIONS[(page_num + i) * 20:(page_num + i + 1) * 20]) != 0:
            pagination["pages"].append({"idPage": page_num + i, "isActive": False})
            pagination["isExistNext"] = True
        i += 1

    context = {"questions": questions, "tags": models.TAGS, "best_members": models.BEST_MEMBERS,
               "paginator": pagination}
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
