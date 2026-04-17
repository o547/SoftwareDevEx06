import networkx as nx
class navi:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls.initialize()
        return cls.instance

    @classmethod
    def initialize(cls):
        print("初期化処理を実行")
        
        # ノード（頂点）のリスト
        NODE_LIST = ["403教室", "404教室", "405教室", "406教室", "407教室", "408教室", "男性トイレ", "女性トイレ", "多目的トイレ", "渡り廊下", "自動販売機"]

        # エッジ（辺）のリスト
        # (始点, 終点, 重み)
        Graph_LIST = [
            ("403教室", "404教室", 1),
            ("404教室", "405教室", 1),
            ("405教室", "406教室", 1),
            ("406教室", "407教室", 1),
            ("407教室", "408教室", 1),
            ("408教室", "408教室", 1),
            ("407教室", "408教室", 1),
            ("408教室", "女性トイレ", 1),
            ("408教室", "男性トイレ", 2),
            ("408教室", "多目的トイレ", 2),
            ("403教室", "渡り廊下", 2),
            ("渡り廊下", "自動販売機", 1),

        ]
        Graph = nx.Graph()
        Graph.add_nodes_from(NODE_LIST)
        Graph.add_weighted_edges_from(Graph_LIST)
        print("初期化されました")
        return Graph

    @classmethod
    def shortestPath(cls,start,end):
        Graph=cls.get_instance()
        # ダイクストラ法で最短経路とその重みを求める
        shortest_path = nx.dijkstra_path(Graph, start, end)
        shortest_path_weight = nx.dijkstra_path_length(Graph, start, end)
        return shortest_path