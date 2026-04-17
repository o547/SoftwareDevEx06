from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View
import networkx as nx
from .navi import navi


class IndexView(View):

    def get(self, request):
        return render(
            request,
            "toyosu_campus_navi/index.html",
            {"nodes" : navi.NODE_LIST},
        )

    def post(self, request):
        start = request.POST["form_start"]
        end = request.POST["form_end"]
        shortest_path_string = ""
        if start != "" and end != "":
            try:
                if start == end:
                    shortest_path_string = "出発地点と目標地点が同じです"
                else:
                    shortest_path_string = " → ".join(navi.shortestPath(start, end))
            except:
                shortest_path_string = "取得できませんでした"

        return render(
            request,
            "toyosu_campus_navi/index.html",
            {
                "start": start, 
                "end": end,
                "shortest_path_string" : shortest_path_string,
                "nodes" : navi.NODE_LIST
            },
        )


index = IndexView.as_view()
