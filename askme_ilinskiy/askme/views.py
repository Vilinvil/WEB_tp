from . import models
from . import forms

from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.http import HttpResponseNotFound


def authenticated_user(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {"is_authorized": True, "username": request.user}
            return func(request, *args, **kwargs, context=context)
        else:
            return func(request, *args, **kwargs)

    return wrapper


@authenticated_user
def index(request, context=None):
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
    if context is None:
        context = {}
    context.update({"questions": questions, "tags": tags, "best_members": models.BEST_MEMBERS,
                    "paginator": pagination,
                    'header_text': "Popular posts" if type_posts == "popular" else "New posts"})
    return render(request, "index.html", context)


def login_user(request):
    print(request.POST)
    if request.method == 'GET':
        login_form = forms.LoginForm()
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            login_form.add_error(None, "Invalid username or password")
    context = {"form": login_form}
    return render(request, "login.html", context=context)


def logout_user(request):
    auth.logout(request)
    return redirect(reverse(index))


def register(request):
    print(request.POST)
    if request.method == 'GET':
        register_form = forms.RegistrationForm()
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            if user:
                return redirect(reverse('login'))
            print("not login")
            register_form.add_error(None, "User saving error")

        else:
            print("not form")

    context = {'form': register_form}
    return render(request, "register.html", context)


@authenticated_user
@login_required
def settings(request, context=None):
    if context is None:
        context = {}
    context.update({"best_members": models.BEST_MEMBERS})
    return render(request, "settings.html", context)


@authenticated_user
@login_required
def new_question(request, context=None):
    if context is None:
        context = {}
    context.update({"best_members": models.BEST_MEMBERS})
    return render(request, "new_question.html", context)


@authenticated_user
def tags(request, tag_id, context=None):
    tag = models.Tag.objects.get(pk=tag_id)
    posts = tag.post.all()
    print(type(posts))
    posts = models.Post.objects.addTags(posts)
    print(type(posts))

    tags = models.Tag.objects.all()[:15]
    tags = tags.values()
    cur_tag = models.Tag.objects.get(pk=tag_id)
    if context is None:
        context = {}
    context.update({"questions": posts, "tags": tags, "best_members": models.BEST_MEMBERS,
                    "tag_name": cur_tag})
    return render(request, "tags.html", context)


@authenticated_user
def questionById(request, user_id, context=None):
    try:
        post = models.Post.objects.get(pk=user_id)
    except models.Post.DoesNotExist:
        return HttpResponseNotFound()

    answers = post.answer_set.all()
    answers = answers.order_by('-mark')

    tags = models.Tag.objects.all()[:15]
    tags = tags.values()
    if context is None:
        context = {}
    context.update({"tags": tags, "best_members": models.BEST_MEMBERS, "question": post,
                    "answers": answers})
    return render(request, "question_by_id.html", context)
