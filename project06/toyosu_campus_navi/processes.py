from django.contrib.auth import authenticate, login
from .models import *
import os
import cv2
from .navi import navi
import numpy as np
from django.conf import settings
import datetime
import networkx as nx

from .managements import (
    HistoryInfoManagement,
    NoticeManagement,
    UserInfoManagement,
    SectionInfoManagement,
    RouteManagement,
)
from google import genai


# C3お知らせ処理部
class NoticeProcess:
    def create_notice(self, request, title, body):
        if not request.user.is_superuser:
            return "お知らせを保存できませんでした"
        else:
            if NoticeManagement().create_notice(request, title, body):
                return ""
            else:
                return "お知らせを保存できませんでした"

    def update_notice(self, request, id, title, body):
        if not request.user.is_superuser:
            return "お知らせを保存できませんでした"
        else:
            if NoticeManagement().update_notice(request, id, title, body):
                return ""
            else:
                return "お知らせを保存できませんでした"

    def notice_delete(self, request, id):
        if not request.user.is_superuser:
            return "お知らせを削除できませんでした"
        else:
            if NoticeManagement().delete_notice(request, id):
                return ""
            else:
                return "お知らせを削除できませんでした"
    def get_notice(self, request, id):
        notice_object = NoticeManagement().get_notice(request, id)
        if notice_object and notice_object.get("title") != "":
            return {
                "title": notice_object["title"],
                "body": notice_object["body"],
                "created_at": notice_object["created_at"],
                "updated_at": notice_object["updated_at"],
                "alert_message": "",
            }
        else:
            return {
                "title": "",
                "body": "",
                "created_at": "",
                "updated_at": "",
                "alert_message": "お知らせを取得できませんでした",
            }

    def get_all_notices(self, request):
        try:
            notices = NoticeManagement().get_all_notices(request)
            if notices is None:
                return {
                    "notices": [],
                    "alert_message": "お知らせを取得できませんでした",
                }

            return {"notices": notices, "alert_message": ""}
        except Exception:
            return {"notices": [], "alert_message": "お知らせを取得できませんでした"}


# C4ログイン処理部
class LoginProcess:
    def user_login(self, request, username, password):
        user = UserInfoManagement().certification(
            request, username=username, password=password
        )
        if user is not None:
            # ログイン成功
            login(request, user)
            return ""
        else:
            request.session["alert_message"] = "ログインできませんでした"
            return "ログインできませんでした"

    def user_regist(self, request, username, password):
        if UserInfoManagement().check_existence(request, username):
            # ユーザーIDが既に存在している
            request.session["alert_message"] = "そのIDは存在しています"
            return "そのIDは存在しています"
        else:
            # アカウントを新規作成する
            user = UserInfoManagement().user_regist(request, username, password)
            login(request, user)
            return ""

    def save_language(self, request, language):
        user_info = self.get_user_info(request)
        if user_info["is_login"]:
            if not (
                UserInfoManagement().save_language(
                    request, language, user_info["username"]
                )
            ):
                request.session["alert_message"] = "言語情報を保存できませんでした"
        request.session["language"] = language
        return "言語情報を保存できませんでした"

    def get_user_info(self, request):
        if request.user.is_authenticated:
            return {
                "is_login": True,
                "id": request.user.id,
                "username": request.user.username,
                "is_superuser": request.user.is_superuser,
                "language": request.user.language,
            }
        else:
            return {
                "is_login": False,
                "id": -1,
                "username": "AnonymousUser",
                "is_superuser": False,
                "language": "JA",
            }


# C5構内図画像作成部
class CampusMapImageCreate:
    # M5-1 構内図画像作成主処理
    def create_map_image(self, request, route, map_folder_name):
        try:
            output_files = []

            floor_map_files = self.create_floor_map(request, route, map_folder_name)

            if not floor_map_files:
                return {
                    "output_files": [],
                    "alert_message": "平面地図を作成できませんでした",
                }

            output_files.extend(floor_map_files)

            used_buildings = []

            for section_name in route:
                building, _, _ = section_name.split("_", 2)

                if building not in used_buildings:
                    used_buildings.append(building)

            for building in used_buildings:
                whole_map_file = self.create_whole_map(
                    request,
                    building,
                    floor_map_files,
                    map_folder_name,
                    route,
                )

                if whole_map_file == "":
                    return {
                        "output_files": output_files,
                        "alert_message": "全体地図を作成できませんでした",
                    }

                output_files.append(whole_map_file)

            return {
                "output_files": output_files,
                "alert_message": "",
            }

        except Exception as e:
            print("C5エラー:", e)
            return {
                "output_files": [],
                "alert_message": "構内図画像を作成できませんでした",
            }

    # M5-2 平面地図作成処理

    def create_floor_map(self, request, route, map_folder_name):
        try:
            output_files = []

            if not route:
                print("routeが空です")
                return []

            # routeを「棟_階」ごとに分割する
            floor_routes = {}

            for section_name in route:
                building, floor, _ = section_name.split("_", 2)
                key = building + "_" + floor

                if key not in floor_routes:
                    floor_routes[key] = []

                floor_routes[key].append(section_name)

            print("平面地図作成処理内の階ごとの経路:", floor_routes)

            output_folder = os.path.join(
                "static",
                "toyosu_campus_navi",
                "image",
                "floor_maps",
                "created_maps",
                map_folder_name,
            )

            os.makedirs(output_folder, exist_ok=True)

            # 階ごとに画像を作成する
            for key in floor_routes:
                floor_route = floor_routes[key]

                building, floor, _ = floor_route[0].split("_", 2)

                input_name = (
                    "static/toyosu_campus_navi/image/floor_map/"
                    + building
                    + "_"
                    + floor
                    + ".jpg"
                )

                print("入力画像:", input_name)

                img = cv2.imdecode(
                    np.fromfile(input_name, dtype=np.uint8),
                    cv2.IMREAD_COLOR,
                )

                if img is None:
                    print("画像を読み込めませんでした:", input_name)
                    return []

                color = (0, 0, 255)
                thickness = 2
                line_type = cv2.LINE_AA
                tip_length = 0.1

                # 同じ階の中だけ矢印を描画する
                for i in range(len(floor_route) - 1):
                    start_node = RouteManagement().get_node_coordinate(
                        request,
                        floor_route[i],
                    )
                    goal_node = RouteManagement().get_node_coordinate(
                        request,
                        floor_route[i + 1],
                    )

                    if start_node["node_x"] == -1 or goal_node["node_x"] == -1:
                        continue

                    start = (start_node["node_x"], start_node["node_y"])
                    goal = (goal_node["node_x"], goal_node["node_y"])

                    cv2.arrowedLine(
                        img,
                        start,
                        goal,
                        color,
                        thickness=thickness,
                        line_type=line_type,
                        tipLength=tip_length,
                    )

                output_file_name = building + "_" + floor + "_route.jpg"

                output_name = os.path.join(
                    output_folder,
                    output_file_name,
                )

                cv2.imencode(".jpg", img)[1].tofile(output_name)

                print("C5で画像を保存しました:", output_name)

                output_files.append(output_file_name)

            return output_files

        except Exception as e:
            print("M5-2エラー:", e)
            return []

    # M5-3 全体地図作成処理

    def create_whole_map(
        self,
        request,
        building,
        floor_map_files,
        map_folder_name,
        route,
    ):
        try:
            images = []

            building_floors = {
                "教室棟": ["1階", "2階", "3階", "4階", "5階", "6階", "7階"],
                "交流棟": ["1階", "2階", "3階", "4階", "5階", "6階"],
                "研究棟": [
                    "1階",
                    "2階",
                    "3階",
                    "4階",
                    "5階",
                    "6階",
                    "7階",
                    "8階",
                    "9階",
                    "10階",
                    "11階",
                    "12階",
                    "13階",
                    "14階",
                ],
                "本部棟": [
                    "B1階",
                    "1階",
                    "2階",
                    "3階",
                    "4階",
                    "5階",
                    "6階",
                    "7階",
                    "8階",
                    "9階",
                    "10階",
                    "11階",
                    "12階",
                    "13階",
                    "14階",
                ],
            }

            if building not in building_floors:
                print("階層情報がありません:", building)
                return ""

            floors_in_building = building_floors[building]
            floors = list(reversed(floors_in_building))

            if not floors:
                print("階層情報がありません:", building)
                return ""

            # 階層間移動を隣接階ごとに分解する
            # 例: 1階 -> 4階 の場合、1->2, 2->3, 3->4 に分解する
            floor_moves = []

            for i in range(len(route) - 1):
                current_building, current_floor, _ = route[i].split("_", 2)
                next_building, next_floor, _ = route[i + 1].split("_", 2)

                if current_building != building or next_building != building:
                    continue

                if current_floor == next_floor:
                    continue

                if (
                    current_floor not in floors_in_building
                    or next_floor not in floors_in_building
                ):
                    continue

                current_index = floors_in_building.index(current_floor)
                next_index = floors_in_building.index(next_floor)

                # 上の階へ移動する場合
                if current_index < next_index:
                    for j in range(current_index, next_index):
                        floor_moves.append(
                            [floors_in_building[j], floors_in_building[j + 1]]
                        )

                # 下の階へ移動する場合
                else:
                    for j in range(current_index, next_index, -1):
                        floor_moves.append(
                            [floors_in_building[j], floors_in_building[j - 1]]
                        )

            # その棟の全階層画像を読み込む
            for floor in floors:
                route_file_name = building + "_" + floor + "_route.jpg"
                normal_file_name = building + "_" + floor + ".jpg"

                # 経路が通った階はcreated_maps内の_route画像を使う
                if route_file_name in floor_map_files:
                    input_name = os.path.join(
                        "static",
                        "toyosu_campus_navi",
                        "image",
                        "floor_maps",
                        "created_maps",
                        map_folder_name,
                        route_file_name,
                    )

                # 経路が通っていない階は元の平面地図を使う
                else:
                    input_name = os.path.join(
                        "static",
                        "toyosu_campus_navi",
                        "image",
                        "floor_map",
                        normal_file_name,
                    )

                img = cv2.imdecode(
                    np.fromfile(input_name, dtype=np.uint8),
                    cv2.IMREAD_COLOR,
                )

                if img is None:
                    print("画像を読み込めませんでした:", input_name)
                    return ""

                images.append((floor, img))

            if not images:
                return ""

            margin_x = 80
            margin_y = 80
            floor_gap = 80

            skewed_images = []
            canvas_width = 0
            canvas_height = margin_y

            # 先に全画像を平行四辺形に変形し、必要なキャンバスサイズを計算する
            for floor, img in images:
                h, w = img.shape[:2]

                shift = w // 5

                src = np.float32(
                    [
                        [0, 0],
                        [w, 0],
                        [0, h],
                        [w, h],
                    ]
                )

                dst = np.float32(
                    [
                        [shift, 0],
                        [w, 0],
                        [0, h],
                        [w - shift, h],
                    ]
                )

                matrix = cv2.getPerspectiveTransform(src, dst)

                skewed_img = cv2.warpPerspective(
                    img,
                    matrix,
                    (w, h),
                    flags=cv2.INTER_NEAREST,
                    borderMode=cv2.BORDER_CONSTANT,
                    borderValue=(255, 255, 255),
                )

                skewed_images.append((floor, skewed_img))

                canvas_width = max(canvas_width, margin_x + w + margin_x)
                canvas_height += h + floor_gap

            canvas_height += margin_y

            canvas = np.full(
                (canvas_height, canvas_width, 3),
                255,
                dtype=np.uint8,
            )

            current_y = margin_y

            # 上から順に縦方向へ配置する
            floor_positions = {}

            for floor, skewed_img in skewed_images:
                h, w = skewed_img.shape[:2]

                x = margin_x
                y = current_y

                # 白背景以外だけ貼り付ける
                mask = np.any(skewed_img < 245, axis=2)

                roi = canvas[y : y + h, x : x + w]
                roi[mask] = skewed_img[mask]
                canvas[y : y + h, x : x + w] = roi

                # 階層ラベル
                floor_text = floor.replace("階", "F")

                cv2.putText(
                    canvas,
                    floor_text,
                    (x + 20, y + 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (120, 120, 120),
                    4,
                    cv2.LINE_AA,
                )

                floor_positions[floor] = {
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h,
                }

                current_y += h + floor_gap

            # 階層間の真ん中に移動方向の矢印を描画する
            for start_floor, goal_floor in floor_moves:
                if (
                    start_floor not in floor_positions
                    or goal_floor not in floor_positions
                ):
                    continue

                start_info = floor_positions[start_floor]
                goal_info = floor_positions[goal_floor]

                # 上に表示されている階と下に表示されている階を判定する
                if start_info["y"] < goal_info["y"]:
                    upper_info = start_info
                    lower_info = goal_info
                else:
                    upper_info = goal_info
                    lower_info = start_info

                upper_bottom = upper_info["y"] + upper_info["h"]
                lower_top = lower_info["y"]

                # 階層と階層の間の中央
                middle_y = (upper_bottom + lower_top) // 2

                start_center_x = start_info["x"] + start_info["w"] // 2
                goal_center_x = goal_info["x"] + goal_info["w"] // 2
                arrow_x = (start_center_x + goal_center_x) // 2

                arrow_half_length = min(
                    30,
                    max(10, (lower_top - upper_bottom) // 2 - 5),
                )

                # 上方向移動
                if start_info["y"] > goal_info["y"]:
                    start_point = (
                        arrow_x,
                        middle_y + arrow_half_length,
                    )
                    goal_point = (
                        arrow_x,
                        middle_y - arrow_half_length,
                    )

                # 下方向移動
                else:
                    start_point = (
                        arrow_x,
                        middle_y - arrow_half_length,
                    )
                    goal_point = (
                        arrow_x,
                        middle_y + arrow_half_length,
                    )

                cv2.arrowedLine(
                    canvas,
                    start_point,
                    goal_point,
                    (0, 0, 255),
                    thickness=4,
                    line_type=cv2.LINE_AA,
                    tipLength=0.25,
                )

            output_folder = os.path.join(
                "static",
                "toyosu_campus_navi",
                "image",
                "floor_maps",
                "created_maps",
                map_folder_name,
            )

            os.makedirs(output_folder, exist_ok=True)

            output_file_name = building + "_whole_map_route.jpg"

            output_name = os.path.join(
                output_folder,
                output_file_name,
            )

            cv2.imencode(".jpg", canvas)[1].tofile(output_name)

            print("全体地図を保存しました:", output_name)

            return output_file_name

        except Exception as e:
            print("M5-3エラー:", e)
            return ""


# C6位置情報処理部
class LocationProcess:
    building_corners = {  # 座標軸みたいな順番で振ってるよ
        "研究棟": [
            (35.66084064312956, 139.79622391567102),
            (35.66160337591864, 139.7952422271883),
            (35.6609452469163, 139.79511348115886),
            (35.66045273623358, 139.79578939781348),
        ],
        "本部棟": [
            (35.660060468897704, 139.79538170201735),
            (35.66049196284233, 139.79474601849697),
            (35.65998201520272, 139.79415593252867),
            (35.65958320772811, 139.79473797187012),
        ],
        "交流棟": [
            (35.660546444247146, 139.7946655522341),
            (35.66072732220492, 139.79438392029468),
            (35.66024352722512, 139.79383674966095),
            (35.66004739328722, 139.79411838160343),
        ],
        "教室棟": [
            (35.661256878214196, 139.79510811673092),
            (35.661426858408745, 139.79502765046252),
            (35.66092999220623, 139.79435709821595),
            (35.660651048422466, 139.79467896328956),
        ],
    }

    def identify_wing(self, request, latitude, longitude):
        test = False

        if not test:
            for building_name, corners in LocationProcess.building_corners.items():
                signs = []
                n = len(corners)
                for i in range(n):
                    x1, y1 = corners[i]
                    x2, y2 = corners[(i + 1) % n]
                    cross = (x2 - x1) * (longitude - y1) - (y2 - y1) * (latitude - x1)
                    signs.append(cross)
                if all(sign >= 0 for sign in signs) or all(sign <= 0 for sign in signs):
                    return building_name
            return ""

        else:
            best_building_name = None
            best_distance = None
            for building_name, corners in LocationProcess.building_corners.items():
                n = len(corners)
                x = sum(p[1] for p in corners) / n
                y = sum(p[0] for p in corners) / n
                distance = (longitude - x) ** 2 + (latitude - y) ** 2
                if best_building_name is None:
                    best_building_name = building_name
                    best_distance = distance
                elif distance < best_distance:
                    best_building_name = building_name
                    best_distance = distance
            return best_building_name


# C11経路検索部
class RouteSearchProcess:
    graph_instance = None

    def route_search_main(self, request, start, goal):
        # 最短経路を計算
        route = self.shortest_route_search(request, start, goal)
        alert_message = ""
        if len(route) == 0:
            alert_message = "経路を検索できませんでした"
        print("経路 : " + str(route))

        # 構内図画像を作成

        map_folder_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        map_result = CampusMapImageCreate().create_map_image(
            request, route, map_folder_name
        )

        map_files = map_result["output_files"]

        if map_result["alert_message"] != "":
            alert_message = map_result["alert_message"]

        # ログイン済みであれば保存
        if request.user.is_authenticated:
            HistoryInfoManagement().save_history(
                request, request.user.username, start, goal
            )

        return {
            "route": route,
            "map_files": map_files,
            "map_folder_name": map_folder_name,
            "alert_message": alert_message,
        }

    def shortest_route_search(self, request, start, goal):
        if RouteSearchProcess.graph_instance is None:
            # グラフデータを初期化
            edges = RouteManagement().get_all_edges(request)
            nodes = RouteManagement().get_all_node_coordinates(request)

            node_list = []
            for node in nodes:
                node_list.append(node["section_name"])

            edge_list = []
            for edge in edges:
                edge_list.append(
                    (
                        str(edge["section_name_a"]),
                        str(edge["section_name_b"]),
                        edge["estimated_travel_time"],
                    )
                )
            graph = nx.Graph()
            graph.add_nodes_from(node_list)
            graph.add_weighted_edges_from(edge_list)
            RouteSearchProcess.graph_instance = graph
            print("グラフデータが初期化されました")

        raw_route = nx.dijkstra_path(RouteSearchProcess.graph_instance, start, goal)
        route = [node for node in raw_route if "エレベータ調整用" not in node]
        # estimated_time = nx.dijkstra_path_length(RouteSearchProcess.graph_instance, start, goal)
        return route


# C13区画情報処理部
class SectionInfoProcess:
    def get_all_sections(self, request):
        nodes = RouteManagement().get_all_node_coordinates(request)
        sections = []
        for node in nodes:
            sections.append(
                {
                    "section_id": node["section_id"],
                    "section_name": node["section_name"],
                }
            )
        return sections

    def get_section_info(self, request, section_name):
        if not section_name:
            return {"section": "", "usage": "", "capacity": -1, "business_hours": ""}

        try:
            section_info = SectionInfoManagement().get_section_info(section_name)
            if section_info:
                return {
                    "section": section_info.get("section", ""),
                    "usage": section_info.get("usage", ""),
                    "capacity": section_info.get("capacity", -1),
                    "business_hours": section_info.get("business_hours", ""),
                }
        except Exception:
            pass

        return {"section": "", "usage": "", "capacity": -1, "business_hours": ""}

    def identify_section(self, request, image_x, image_y, map_name):
        section_objects = SectionInfoManagement().get_coordinate_list(map_name)
        for section in section_objects:
            if section.get("top_left_x") in [None, -1]:
                continue

            if (
                image_x >= section["top_left_x"]
                and image_y >= section["top_left_y"]
                and image_x <= section["bottom_right_x"]
                and image_y <= section["bottom_right_y"]
            ):
                return section["section_name"]

        return ""


# C15履歴情報処理部
class HistoryInfoProcess:
    def save_history(self, request, username, start, goal):
        result = HistoryInfoManagement().save_history(request, username, start, goal)
        if result:
            return ""
        else:
            return "履歴が保存できませんでした"

    def get_all_histories(self, request, username):
        histories = HistoryInfoManagement().get_all_histories(request, username)
        return histories


# C14チャットボット処理部
class ChatBotProcess:
    def reply_to_chat(self, request, user_input):
        # APIキーはkeys.pyで管理している
        api_key = settings.GEMINI_API_KEY
        user_output = ""
        alert_message = ""
        if api_key == "ここにAPIキーを入力":
            alert_message = "チャットボットが使用できません．"
            return {"user_output": user_output, "alert_message": alert_message}
        else:
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=self.create_prompt(request, user_input),
                )
                user_output = response.text
                history = request.session.get("chat_history", "")
                request.session["chat_history"] = (
                    history
                    + "ユーザの入力："
                    + user_input
                    + "チャットボットの出力："
                    + user_output
                )
                return {"user_output": user_output, "alert_message": alert_message}
            except Exception as e:
                print("エラー内容:", e)
                alert_message = "チャットボットが使用できません．"
                return {"user_output": user_output, "alert_message": alert_message}

    def create_prompt(self, request, user_input):
        route = RouteManagement().get_all_node_coordinates(request)
        all_route = ""
        for r in route:
            if not ("中継" in r["section_name"] or "区画調整" in r["section_name"]):
                all_route += (
                    f"区画名：{r['section_name']}"
                    # + f"ノード(区画)のid：{r['section_id']}"
                    # + f"ノードの座標(x,y)：{r['node_x']},{r['node_y']}"
                )
        history = request.session.get("chat_history", "")
        prompt = (
            "あなたはキャンパス案内のチャットボットです．ユーザの質問に答え，経路案内が必要ならリンクを返してください．送信元の言語に合わせて出力してください．"
            f"ユーザの質問はこれです．{user_input}"
            "返答分の形式はこちらです．"
            "案内に無関係そうな文章が入力された場合：URLは出力せず，案内に関係することを答えてもらうように促してください．"
            "案内に関係ありそうで始点と終点が一意に特定できる場合：URLを出力し，始点の区画名→終点の区画名までの経路案内はこちらです！と出力し，brタグで改行してURLを表示してください．"
            "案内に関係ありそうで始点と終点のどちらかあるいは両方が特定できない場合：URLは出力せず，特定できそうな範囲まで絞るためにいくつか選択肢を用意してください．"
            "案内に関係ありそうで情報を聞くだけの場合：区画情報から答えられる範囲で質問の意図を満たすように回答してください．"
            "案内に関係ありそうで区画が存在しなそうな場合：見つかりません．ほかに情報はありますか的な回答をしてください．"
            f"区画の情報一覧はこちらです．{all_route}"
            "URLはaタグで囲ってクリックできるようにしてください．URLの形式はこちらです．/search/始点の区画名/終点の区画名"
            f"過去のチャット履歴はこちらです．{history}"
        )
        return prompt
