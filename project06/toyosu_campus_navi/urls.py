from django.urls import path
from . import views
app_name="toyosu_campus_navi"

urlpatterns=[
  path("demo",views.demo_index , name="demo_index"),
  path("plot",views.plot , name="plot"),
  path("",views.index , name="index"),
  path("user/login",views.user_login,name="user_login")
] 