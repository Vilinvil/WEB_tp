from . import models

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseServerError


# Create your views here.
def index(request):
    try:
        page_num = request.GET.get('page_num', 0)
        type_posts = request.GET.get("type", "")
        page_num = int(page_num)
    except ValueError:
        page_num = 0
    COUNT_PAGES = 20
    left = (page_num - 1) * COUNT_PAGES if page_num >= 1 else 0
    right = (page_num + 3) * COUNT_PAGES
    posts = []
    if type_posts == "popular":
        posts = models.Post.objects.popularPosts(left, right)
    else:
        posts = models.Post.objects.newPosts(left, right)

    res_pagination = models.paginate(page_num, COUNT_PAGES, posts)
    try:
        pagination = res_pagination["pagination"]
        questions = res_pagination["cur_arr"]
    except KeyError:
        return HttpResponseServerError()

    tags = models.Tag.objects.all()[:15]
    tags = tags.values()

    questions = models.Post.objects.addTags(questions)
    context = {"questions": questions, "tags": tags, "best_members": models.BEST_MEMBERS,
               "paginator": pagination, 'header_text': "Popular posts" if type_posts == "popular" else "New posts"}
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
    tag = models.Tag.objects.get(pk=tag_id)
    posts = tag.post.all()
    print(type(posts))
    posts = models.Post.objects.addTags(posts)
    print(type(posts))

    tags = models.Tag.objects.all()[:15]
    tags = tags.values()
    cur_tag = models.Tag.objects.get(pk=tag_id)
    context = {"questions": posts, "tags": tags, "best_members": models.BEST_MEMBERS,
               "tag_name": cur_tag}
    return render(request, "tags.html", context)


def questionById(request, user_id):
    # Добавить валидацию
    post = models.Post.objects.get(pk=user_id)

    answers = post.answer_set.all()
    answers = answers.order_by('-mark')

    tags = models.Tag.objects.all()[:15]
    tags = tags.values()
    context = {"tags": tags, "best_members": models.BEST_MEMBERS, "question": post,
               "answers": answers}
    return render(request, "question_by_id.html", context)
