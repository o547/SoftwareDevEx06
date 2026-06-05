from django.contrib.auth import authenticate, login
from .models import *
from .manegements import *


# C3お知らせ処理部
class NoticeProcess:
    def create_notice(self, request, title, body):
        if not request.user.is_superuser:
            return "お知らせを保存できませんでした"
        else:
            if NoticeManegement().create_notice(request, title, body):
                return ""
            else:
                return "お知らせを保存できませんでした"
            
    def update_notice(self, request, id, title, body):
        if not request.user.is_superuser:
            return "お知らせを保存できませんでした"
        else:
            if NoticeManegement().update_notice(request, id, title, body):
                return ""
            else:
                return "お知らせを保存できませんでした"
    def notice_delete(self, request, id):
        if not request.user.is_superuser:
            return "お知らせを削除できませんでした"
        else:
            if NoticeManegement().delete_notice(request, id):
                return ""
            else:
                return "お知らせを削除できませんでした"



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
    #測定する
    research_building_x_max    = 100
    research_building_x_min    = 100
    research_building_y_max    = 100
    research_building_y_min    = 100
    admin_building_x_max       = 100
    admin_building_x_min       = 100
    admin_building_y_max       = 100
    admin_building_y_min       = 100
    interaction_building_x_max = 100
    interaction_building_x_min = 100
    interaction_building_y_max = 100
    interaction_building_y_min = 100
    classroom_building_x_max   = 100
    classroom_building_x_min   = 100
    classroom_building_y_max   = 100
    classroom_building_y_min   = 100
    #測定する
    def identify_wing(self, request, latitude, longitude):
        if (LocationProcess.research_building_x_min < longitude < LocationProcess.research_building_x_max and LocationProcess.research_building_y_min < latitude < LocationProcess.research_building_y_max):#研究棟の範囲内
            return "研究棟"
        elif (LocationProcess.admin_building_x_min < longitude < LocationProcess.admin_building_x_max and LocationProcess.admin_building_y_min < latitude < LocationProcess.admin_building_y_max):#本部棟の範囲内
            return "本部棟"
        elif (LocationProcess.interaction_building_x_min < longitude < LocationProcess.interaction_building_x_max and LocationProcess.interaction_building_y_min < latitude < LocationProcess.interaction_building_y_max):#交流棟の範囲内
            return "交流棟"
        elif (LocationProcess.classroom_building_x_min < longitude < LocationProcess.classroom_building_x_max and LocationProcess.classroom_building_y_min < latitude < LocationProcess.classroom_building_y_max):#教室棟の範囲内
            return "教室棟"
        else:#すべての棟の範囲外
            return ""




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
