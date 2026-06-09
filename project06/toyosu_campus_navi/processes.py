from django.contrib.auth import authenticate, login
from django.conf import settings
import datetime
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
    pass


# C6位置情報処理部
class LocationProcess:
    pass


# C11経路検索部
class RouteSearchProcess:
    def route_search_main(self, request, start, goal):
        # 最短経路を計算
        route = self.shortest_route_search(request, start, goal)
        alert_message = ""
        if route == []:
            alert_message = "経路を検索できませんでした"

        # 構内図画像を作成
        map_folder_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        map_files = CampusMapImageCreate().create_floor_map(
            request, route, map_folder_name
        )

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
