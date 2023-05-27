from askme import views

from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("settings/", views.settings, name="settings"),
    path("new_question/", views.new_question, name="new_question"),
    path("tag/<int:tag_id>", views.tags, name="tags"),
    path("question/<int:question_id>", views.questionById, name="question-by-id"),
    path("logout/", views.logout_user, name="logout")
]