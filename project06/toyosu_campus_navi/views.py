from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View
from .navi import navi
from .map import map

class IndexView(View):

    def get(self, request):
        nodes=list(navi.nodes.keys())
        nodes[:] = [x for x in nodes if not x.startswith("中継_")]
        return render(
            request,
            "toyosu_campus_navi/index.html",
            {"nodes" : nodes,
             "map_image_file": "map4F.png"},
        )

    def post(self, request):
        start = request.POST["form_start"]
        end = request.POST["form_end"]
        shortest_path_string = ""
        map_image_file = "map4F.png"
        if start != "" and end != "":
            try:
                if start == end:
                    shortest_path_string = "出発地点と目標地点が同じです"
                else:
                    shortest_path = navi.shortestPath(start, end)
                    map.drow_arrows(shortest_path)
                    shortest_path_string = " → ".join(shortest_path)
                    map_image_file = "output.png"
            except:
                shortest_path_string = "取得できませんでした"

        nodes=list(navi.nodes.keys())
        nodes[:] = [x for x in nodes if not x.startswith("中継_")]
        return render(
            request,
            "toyosu_campus_navi/index.html",
            {
                "start": start, 
                "end": end,
                "shortest_path_string" : shortest_path_string,
                "nodes" : nodes,
                "map_image_file" : map_image_file
            },
        )


index = IndexView.as_view()
