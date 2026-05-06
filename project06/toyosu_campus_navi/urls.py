from django.urls import path
from . import views
app_name="toyosu_campus_navi"

urlpatterns=[
  path("demo",views.demo_index , name="demo_index"),
  path("",views.index , name="index"),

] 