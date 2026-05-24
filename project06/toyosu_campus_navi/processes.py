from django.contrib.auth import authenticate, login
from .models import *
from .manegements import *


# C3お知らせ処理部
class NoticeProcess:
    pass


# C4ログイン処理部
class LoginProcess:
    def user_login(self, request, username, password):
        user = UserInfoManegement().certification(
            request, username=username, password=password
        )
        if user is not None:
            # ログイン成功
            login(request, user)
            return True
        else:
            request.session["alert_message"] = "ログインできませんでした"
            return False

    def user_regist(self, request, username, password):
        if UserInfoManegement().check_existence(request, username):
            # ユーザーIDが既に存在している
            request.session["alert_message"] = "そのIDは存在しています"
            return False
        else:
            # アカウントを新規作成する
            user = UserInfoManegement().user_regist(request, username, password)
            login(request, user)
            return True

    def save_language(self, request, language):
        user_info = self.get_user_info(request)
        if user_info["is_login"]:
            if UserInfoManegement().save_language(
                request, language, user_info["username"]
            ):
                request.session["alert_message"] = "言語情報を保存できませんでした"
        request.session["language"] = language

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
    pass


# C15履歴情報処理部
class HistoryInfoProcess:
    pass


# C14チャットボット処理部
class ChatBotProcess:
    def reply_to_chat(self, request, user_input):
        user_output = "返答文"
        return user_output
