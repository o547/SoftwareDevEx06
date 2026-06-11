from django.contrib.auth import authenticate, login
from .models import *
import os
import cv2
from .navi import navi
import numpy as np
from django.conf import settings
from .managements import (
    HistoryInfoManagement,
    NoticeManagement,
    UserInfoManagement,
    SectionInfoManagement,
    RouteManagement,
)


# C3お知らせ処理部
class NoticeProcess:
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
            floor_routes = {}

            # routeを「棟_階」ごとに分割する
            for section_name in route:
                building, floor, section = section_name.split("_", 2)
                key = building + "_" + floor

                if key not in floor_routes:
                    floor_routes[key] = []

                floor_routes[key].append(section_name)

            print("階ごとの経路:", floor_routes)

            # 階ごとに平面地図を作成する
            for key in floor_routes:
                floor_output_files = self.create_floor_map(
                    request, floor_routes[key], map_folder_name
                )
                output_files.extend(floor_output_files)

            # 複数階層の場合のみ、通った階層画像だけで全体地図を作成する
            if len(output_files) >= 2:
                whole_map_file = self.create_whole_map(
                    request, output_files, map_folder_name
                )

                if whole_map_file != "":
                    output_files.append(whole_map_file)

            return {"output_files": output_files, "alert_message": ""}

        except Exception as e:
            print("C5エラー:", e)
            return {
                "output_files": [],
                "alert_message": "構内図画像を作成できませんでした",
            }

    # M5-2 平面地図作成処理
    def create_floor_map(self, request, route, map_folder_name):
        output_files = []

        # routeの先頭から、描画対象の棟・階を取得する
        building, floor, section = route[0].split("_", 2)

        input_name = (
            "static/toyosu_campus_navi/image/floor_map/"
            + building
            + "_"
            + floor
            + ".jpg"
        )
        print("入力画像:", input_name)

        output_folder = os.path.join(
            "static",
            "toyosu_campus_navi",
            "image",
            "floor_maps",
            "created_maps",
            map_folder_name,
        )

        os.makedirs(output_folder, exist_ok=True)

        output_file_name = building + "_" + floor + "_route.jpg"
        output_name = os.path.join(output_folder, output_file_name)

        img = cv2.imdecode(np.fromfile(input_name, dtype=np.uint8), cv2.IMREAD_COLOR)

        if img is None:
            print("画像を読み込めませんでした:", input_name)
            return output_files

        color = (0, 0, 255)
        thickness = 2
        line_type = cv2.LINE_AA
        tipLength = 0.1

        # 経路に沿って矢印を描画する
        for i in range(len(route) - 1):
            start_node = RouteManagement().get_node_coordinate(request, route[i])
            goal_node = RouteManagement().get_node_coordinate(request, route[i + 1])

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
                tipLength=tipLength,
            )

        cv2.imencode(".jpg", img)[1].tofile(output_name)

        print("C5で画像を保存しました:", output_name)

        output_files.append(
            "floor_maps/created_maps/" + map_folder_name + "/" + output_file_name
        )

        return output_files

    # M5-3 全体地図作成処理
    def create_whole_map(self, request, floor_map_files, map_folder_name):
        images = []

        # 通った階層の_route画像だけを読み込む
        for file_name in floor_map_files:
            input_name = os.path.join(
                "static", "toyosu_campus_navi", "image", file_name
            )

            img = cv2.imdecode(
                np.fromfile(input_name, dtype=np.uint8), cv2.IMREAD_COLOR
            )

            if img is not None:
                images.append((file_name, img))
            else:
                print("画像を読み込めませんでした:", input_name)

        if len(images) == 0:
            return ""

        offset_x = 220
        offset_y = 380

        positions = []
        canvas_height = 0
        canvas_width = 0

        # 画像サイズを考慮してキャンバスサイズを決める
        for i, (file_name, img) in enumerate(images):
            h, w = img.shape[:2]

            x = offset_x * i
            y = offset_y * i

            positions.append((x, y))

            canvas_width = max(canvas_width, x + w)
            canvas_height = max(canvas_height, y + h)

        canvas_height += 100
        canvas_width += 100

        canvas = np.full((canvas_height, canvas_width, 3), 255, dtype=np.uint8)

        for i, (file_name, img) in enumerate(images):
            h, w = img.shape[:2]

            # 平面地図を平行四辺形に変形する
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

            x, y = positions[i]

            # 白背景以外だけを貼り付ける
            mask = np.any(skewed_img < 245, axis=2)

            roi = canvas[y : y + h, x : x + w]
            roi[mask] = skewed_img[mask]
            canvas[y : y + h, x : x + w] = roi

            # 階層ラベルを表示する
            floor_text = file_name.split("/")[-1]
            floor_text = floor_text.replace("_route.jpg", "")
            floor_text = floor_text.split("_")[-1]
            floor_text = floor_text.replace("階", "F")

            cv2.putText(
                canvas,
                floor_text,
                (x + 30, y + h - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 0, 255),
                4,
                cv2.LINE_AA,
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

        output_file_name = "whole_map_route.jpg"
        output_name = os.path.join(output_folder, output_file_name)

        cv2.imencode(".jpg", canvas)[1].tofile(output_name)

        print("全体地図を保存しました:", output_name)

        return "floor_maps/created_maps/" + map_folder_name + "/" + output_file_name


# C6位置情報処理部
class LocationProcess:
    pass


# C11経路検索部
class RouteSearchProcess:
    pass


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
    pass


# C14チャットボット処理部
class ChatBotProcess:
    def reply_to_chat(self, request, user_input):
        user_output = "返答文"
        # APIキーはkeys.pyで管理している
        api_key = settings.GEMINI_API_KEY
        return user_output
