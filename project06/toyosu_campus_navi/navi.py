import networkx as nx
class navi:
    instance = None
    # ノード（頂点）のリスト
    nodes = {
        "401教室": (116 , 187),
        "402教室": (185 , 187),
        "403教室": (500, 125),
        "404教室": (619, 125),
        "405教室": (700, 125),
        "406教室": (760, 125),
        "407教室": (832 , 125),
        "408教室": (888, 125) ,
        "教室棟_女性トイレ": (933, 133),
        "中継_教室棟_トイレ": (888, 170),
        "教室棟_男性トイレ": (933, 170),
        "教室棟_多目的トイレ": (915, 170),
        "教室棟_渡り廊下入口": (423 , 137),
        "交流棟_渡り廊下入口": (332, 137),
        "中継_交流棟_トイレ": (308, 150),
        "自動販売機": (332, 148),
        "交流棟_男性トイレ": (268, 150),
        "交流棟_女性トイレ": (282, 150),
        "交流棟_エレベーター": (292, 194),
        "中継_交流棟_右上": (312 , 112),
        "中継_交流棟_左上": (242 , 112),
        "中継_交流棟_右下": (305 , 217),
        "中継_交流棟_左下": (242 , 217),
        "中継_交流棟_教室前": (242 , 187),
    }

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls.initialize()
        return cls.instance

    #初期化処理
    @classmethod
    def initialize(cls):
        NODE_LIST =list(cls.nodes.keys())

        nodes = cls.nodes
        Graph_LIST = [
            ("403教室", "404教室", cls.pythagorean(nodes["403教室"], nodes["404教室"])),
            ("404教室", "405教室", cls.pythagorean(nodes["404教室"], nodes["405教室"])),
            ("405教室", "406教室", cls.pythagorean(nodes["405教室"], nodes["406教室"])),
            ("406教室", "407教室", cls.pythagorean(nodes["406教室"], nodes["407教室"])),
            ("407教室", "408教室", cls.pythagorean(nodes["407教室"], nodes["408教室"])),
            ("408教室", "教室棟_女性トイレ", cls.pythagorean(nodes["408教室"], nodes["教室棟_女性トイレ"])),
            ("407教室", "中継_教室棟_トイレ", cls.pythagorean(nodes["407教室"], nodes["中継_教室棟_トイレ"])),
            ("408教室", "中継_教室棟_トイレ", cls.pythagorean(nodes["408教室"], nodes["中継_教室棟_トイレ"])),
            ("中継_教室棟_トイレ", "教室棟_男性トイレ", cls.pythagorean(nodes["中継_教室棟_トイレ"], nodes["教室棟_男性トイレ"])),
            ("教室棟_多目的トイレ", "教室棟_男性トイレ", cls.pythagorean(nodes["教室棟_多目的トイレ"], nodes["教室棟_男性トイレ"])),
            ("中継_教室棟_トイレ", "教室棟_多目的トイレ", cls.pythagorean(nodes["中継_教室棟_トイレ"], nodes["教室棟_多目的トイレ"])),
            ("403教室", "教室棟_渡り廊下入口", cls.pythagorean(nodes["403教室"], nodes["教室棟_渡り廊下入口"])),
            ("教室棟_渡り廊下入口", "交流棟_渡り廊下入口", cls.pythagorean(nodes["教室棟_渡り廊下入口"], nodes["交流棟_渡り廊下入口"])*1.5),
            ("交流棟_渡り廊下入口", "自動販売機", cls.pythagorean(nodes["交流棟_渡り廊下入口"], nodes["自動販売機"])),
            ("交流棟_渡り廊下入口", "中継_交流棟_トイレ", cls.pythagorean(nodes["交流棟_渡り廊下入口"], nodes["中継_交流棟_トイレ"])),
            ("中継_交流棟_トイレ", "交流棟_男性トイレ", cls.pythagorean(nodes["中継_交流棟_トイレ"], nodes["交流棟_男性トイレ"])),
            ("中継_交流棟_トイレ", "交流棟_女性トイレ", cls.pythagorean(nodes["中継_交流棟_トイレ"], nodes["交流棟_女性トイレ"])),
            ("交流棟_男性トイレ", "交流棟_女性トイレ", cls.pythagorean(nodes["交流棟_男性トイレ"], nodes["交流棟_女性トイレ"])),
            ("中継_交流棟_トイレ", "中継_交流棟_右上", cls.pythagorean(nodes["中継_交流棟_トイレ"], nodes["中継_交流棟_右上"])),
            ("中継_交流棟_トイレ", "交流棟_エレベーター", cls.pythagorean(nodes["中継_交流棟_トイレ"], nodes["交流棟_エレベーター"])),
            ("中継_交流棟_トイレ", "交流棟_渡り廊下入口", cls.pythagorean(nodes["中継_交流棟_トイレ"], nodes["交流棟_渡り廊下入口"])),
            ("交流棟_渡り廊下入口", "中継_交流棟_右上", cls.pythagorean(nodes["交流棟_渡り廊下入口"], nodes["中継_交流棟_右上"])),
            ("中継_交流棟_右上", "中継_交流棟_左上", cls.pythagorean(nodes["中継_交流棟_右上"], nodes["中継_交流棟_左上"])),
            ("中継_交流棟_左上", "中継_交流棟_教室前", cls.pythagorean(nodes["中継_交流棟_左上"], nodes["中継_交流棟_教室前"])),
            ("中継_交流棟_教室前", "中継_交流棟_左下", cls.pythagorean(nodes["中継_交流棟_教室前"], nodes["中継_交流棟_左下"])),
            ("中継_交流棟_左下", "中継_交流棟_右下", cls.pythagorean(nodes["中継_交流棟_左下"], nodes["中継_交流棟_右下"])),
            ("交流棟_エレベーター", "中継_交流棟_右下", cls.pythagorean(nodes["交流棟_エレベーター"], nodes["中継_交流棟_右下"])),
            ("中継_交流棟_トイレ", "中継_交流棟_右下", cls.pythagorean(nodes["中継_交流棟_トイレ"], nodes["中継_交流棟_右下"])),
            ("中継_交流棟_教室前", "402教室", cls.pythagorean(nodes["中継_交流棟_教室前"], nodes["402教室"])),
            ("402教室", "401教室", cls.pythagorean(nodes["402教室"], nodes["401教室"])),
        ]
        Graph = nx.Graph()
        Graph.add_nodes_from(NODE_LIST)
        Graph.add_weighted_edges_from(Graph_LIST)
        print("地図データが初期化されました")
        return Graph

    @classmethod
    def shortestPath(cls,start,goal):
        Graph=cls.get_instance()
        # ダイクストラ法で最短経路とその推定移動時間を求める
        shortest_path = nx.dijkstra_path(Graph, start, goal)
        estimated_time = nx.dijkstra_path_length(Graph, start, goal) / 7
        return shortest_path, estimated_time

    @classmethod
    def pythagorean(cls,start_coord,goal_coord):
        return ( (start_coord[0]-goal_coord[0])**2 + (start_coord[1]-goal_coord[1])**2)**0.5
