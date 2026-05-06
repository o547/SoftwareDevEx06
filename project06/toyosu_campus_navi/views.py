from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View
from .navi import navi
from .map import map
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.models import User


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

class IndexView(View):
    def get(self, request):
        return render(
            request,
            "toyosu_campus_navi/index.html"
        )




demo_index = DemoIndexView.as_view()
index = IndexView.as_view()

