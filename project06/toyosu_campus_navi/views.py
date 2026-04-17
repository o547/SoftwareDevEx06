from django.shortcuts import render

# Create your views here.
from django.views import View
import networkx as nx
from .navi import navi

class IndexView(View):
    def get(self, request):
        # 出発地ノードと目的地ノードを設定
        start="405教室"
        end="自動販売機"
        shortest_path=navi.shortestPath(start,end)
        print("Shortest Path:", shortest_path) 
        shortest_path_string = " → ".join(shortest_path)
        return render(request, "toyosu_campus_navi/index.html", 
                      {"start": start,"end":end,"shortest_path_string":shortest_path_string}
                      )
    
index = IndexView.as_view()