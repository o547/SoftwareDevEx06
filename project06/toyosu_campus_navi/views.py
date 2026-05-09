from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from .navi import navi
from .map import map
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class DemoIndexView(View):

    def get(self, request):
        nodes = list(navi.nodes.keys())
        nodes[:] = [x for x in nodes if not x.startswith("中継_")]
        return render(
            request,
            "toyosu_campus_navi/demo_index.html",
            {
                "nodes": nodes,
                "map_image_file": "map4F.png",
                "start": " ---- ",
                "goal": " ---- ",
            },
        )

    def post(self, request):
        start = request.POST["form_start"]
        goal = request.POST["form_goal"]
        shortest_path_string = ""
        estimated_time = ""
        map_image_file = "map4F.png"
        if start != "" and goal != "":
            try:
                if start == goal:
                    shortest_path_string = "出発地点と目標地点が同じです"
                else:
                    shortest_path, estimated_time = navi.shortestPath(start, goal)
                    estimated_time = round(estimated_time)
                    map.drow_arrows(shortest_path)
                    shortest_path_string = " → ".join(shortest_path)
                    map_image_file = "output.png"
            except:
                shortest_path_string = "取得できませんでした"

        if start == "":
            start = " ---- "
        if goal == "":
            goal = " ---- "
        nodes = list(navi.nodes.keys())
        nodes[:] = [x for x in nodes if not x.startswith("中継_")]
        return render(
            request,
            "toyosu_campus_navi/demo_index.html",
            {
                "start": start,
                "goal": goal,
                "shortest_path_string": shortest_path_string,
                "nodes": nodes,
                "map_image_file": map_image_file,
                "estimated_time": estimated_time,
            },
        )
        
class PlotView(View):
    def get(self, request):

        return render(
            request,
            "toyosu_campus_navi/plot.html",
        )

class IndexView(View):
    def get(self, request):
        user_id = str(request.user)
        login_button_text = "ログイン"
        if(user_id != "AnonymousUser"):
            login_button_text = "履歴"
            
        return render(
            request,
            "toyosu_campus_navi/index.html",
            {"user_id":user_id}
        )
        
class UserLoginView(View):
    def post(self, request):
        login_id = request.POST["login-id"]
        login_password = request.POST["login-password"]
        login_method = request.POST["login-method"]
        if(login_method == "login"):
            user = authenticate(request,username=login_id, password=login_password)
            login(request, user)
        elif(login_method == "create"):
            print("id:"+login_id+" pass"+login_password)
            User.objects.create_user(login_id,"",login_password)
            user = authenticate(request,username=login_id, password=login_password)
            login(request, user)
        
        return redirect("toyosu_campus_navi:index")




demo_index = DemoIndexView.as_view()
index = IndexView.as_view()
user_login = UserLoginView.as_view()
plot = PlotView.as_view()