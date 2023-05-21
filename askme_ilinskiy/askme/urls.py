from django.urls import path
from askme import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("settings/", views.settings, name="settings"),
    path("new_question/", views.new_question, name="new_question"),
    path("tag/<int:tag_id>", views.tags, name="tags"),
    path("question/<int:user_id>", views.questionById, name="question-by-id"),
]