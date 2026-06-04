from django.urls import path
from . import views

app_name = "toyosu_campus_navi"

urlpatterns = [
    path("demo/guide", views.demo_index, name="demo_index"),
    path("plot", views.plot, name="plot"),
    path("", views.index, name="index"),
    path("user/login", views.user_login, name="user_login"),
    path("chatbot/submit", views.chatbot_submit, name="chatbot_submit"),
    path("language/submit", views.language_submit, name="language_submit"),
    path("coordinate/submit", views.coordinate_submit, name="coordinate_submit"),
    path("search/<str:start>/<str:goal>", views.search_submit, name="search_submit"),
    path("notice", views.notice, name="notice"),
    path("notice/management", views.notice_management, name="notice_management"),
    path("notice/edit", views.notice_edit, name="notice_edit"),
    path("history", views.history, name="history"),
    path("debug", views.debug, name="debug"),
]
