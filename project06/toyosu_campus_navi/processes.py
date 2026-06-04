from django.contrib.auth import authenticate, login
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
    pass


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
