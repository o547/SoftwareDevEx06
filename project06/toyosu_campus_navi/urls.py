from django.urls import path
from . import views
app_name="toyosu_campus_navi"

urlpatterns=[
  path("",views.index , name="index"),
] 