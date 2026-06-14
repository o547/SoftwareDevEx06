from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from .navi import navi
from .map import map
from .processes import (
    CampusMapImageCreate,
    ChatBotProcess,
    HistoryInfoProcess,
    LocationProcess,
    LoginProcess,
    NoticeProcess,
    RouteSearchProcess,
    SectionInfoProcess,
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
import uuid


# フロントに送る情報をまとめる
def create_info_to_send(request):
    uset_info = LoginProcess().get_user_info(request)
    alert_message = request.session.get("alert_message")
    if alert_message:
        del request.session["alert_message"]
    return {
        "alert_message": alert_message,
        "is_login": uset_info["is_login"],
        "username": uset_info["username"],
        "is_superuser": uset_info["is_superuser"],
        "language": uset_info["language"],
    }


# /
class IndexView(View):
    def get(self, request):
        nodes = SectionInfoProcess().get_all_sections(request)
        all_notices = NoticeProcess().get_all_notices(request)
        info_to_send = create_info_to_send(request) | {
            "section_names": [node["section_name"] for node in nodes],
            "notices": all_notices["notices"],
            "notices_alert_message": all_notices["alert_message"],
        }

        search_result = request.session.get("search_result")
        if search_result:
            # 検索から遷移した場合
            del request.session["search_result"]
            info_to_send = info_to_send | {
                "route": search_result["route"],
                "map_files": search_result["map_files"],
                "map_folder_name": search_result["map_folder_name"],
            }

        request.session["chat_history"] = ""
        return render(request, "toyosu_campus_navi/index.html", info_to_send)


# /notice
class NoticeView(View):
    def get(self, request, notice_id):
        info_to_send = create_info_to_send(request) | {
            "notice": NoticeProcess().get_notice(request, notice_id),
        }
        return render(request, "toyosu_campus_navi/notice.html", info_to_send)


# /notice/management
class NoticeManagementView(View):
    def get(self, request):
        all_notices = NoticeProcess().get_all_notices(request)
        info_to_send = create_info_to_send(request) | {
            "notices": all_notices["notices"],
            "notices_alert_message": all_notices["alert_message"],
        }
        return render(
            request, "toyosu_campus_navi/notice_management.html", info_to_send
        )


# /notice/edit
class NoticeEditView(View):
    def get(self, request):
        info_to_send = create_info_to_send(request)
        if "notice_id" in request.GET:
            # 既存のお知らせの編集
            notice_id = request.GET.get("notice_id")
            info_to_send = info_to_send | {
                "current_notice": NoticeProcess().get_notice(request, notice_id),
            }

        return render(request, "toyosu_campus_navi/notice_edit.html", info_to_send)


# /notice/delete
class NoticeDeleteView(View):
    def get(self, request, notice_id):
        alert_message = NoticeProcess().notice_delete(request, notice_id)
        if alert_message:
            request.session["alert_message"] = alert_message
        return redirect("toyosu_campus_navi:notice_management")


# /notice/submit
class NoticeSubmitView(View):
    def post(self, request):
        body = json.loads(request.body)
        notice_title = body["title"]
        notice_body = body["body"]
        notice_id = body["notice_id"]
        alert_message = ""
        if notice_id is None:
            alert_message = NoticeProcess().create_notice(
                request, notice_title, notice_body
            )
        else:
            alert_message = NoticeProcess().update_notice(
                request, uuid.UUID(notice_id), notice_title, notice_body
            )
        if alert_message:
            request.session["alert_message"] = alert_message

        return JsonResponse({"alert_message": alert_message})


# /history
class HistoryView(View):
    def get(self, request):
        info_to_send = create_info_to_send(request) | {
            "histories": HistoryInfoProcess().get_all_histories(
                request, request.user.username
            ),
        }
        return render(request, "toyosu_campus_navi/history.html", info_to_send)


# /identify/wing
class IdentifyWingView(View):
    def post(self, request):

        body = json.loads(request.body)
        latitude = body["latitude"]
        longitude = body["longitude"]
        wing_name = LocationProcess().identify_wing(request, latitude, longitude)
        return JsonResponse({"wing_name": wing_name})


# /user/login
class UserLoginView(View):
    def post(self, request):

        login_id = request.POST["login-id"]
        login_password = request.POST["login-password"]
        login_method = request.POST["login-method"]

        if login_method == "login":
            alert_message = LoginProcess().user_login(request, login_id, login_password)
            if alert_message == "":
                return redirect("toyosu_campus_navi:history")
        elif login_method == "regist":
            LoginProcess().user_regist(request, login_id, login_password)

        return redirect("toyosu_campus_navi:index")


# /chatbot/submit
class ChatBotView(View):
    def post(self, request):

        body = json.loads(request.body)
        question = body["question"]
        reply = ChatBotProcess().reply_to_chat(request, question)
        response = reply["user_output"]
        alert_message = reply["alert_message"]

        return JsonResponse(
            {"chatbot_response": response, "alert_message": alert_message}
        )


# /language/submit
class LanguageView(View):
    def post(self, request):

        body = json.loads(request.body)
        language = body["language"]
        response = LoginProcess().save_language(request, language)
        alert_message = request.session.get("alert_message")
        if alert_message:
            del request.session["alert_message"]
        return JsonResponse({"alert_message": alert_message})


# /coordinate/submit
class CoordinateSubmitView(View):
    def post(self, request):
        body = json.loads(request.body)
        section_name = SectionInfoProcess().identify_section(
            request, body["image_x"], body["image_y"], body["map_name"]
        )
        print(section_name)
        section_info = SectionInfoProcess().get_section_info(request, section_name)
        return JsonResponse(section_info)


# /search
class SearchView(View):
    def get(self, request, start, goal):
        print("start : " + start)
        print("goal : " + goal)
        search_result = RouteSearchProcess().route_search_main(request, start, goal)
        if search_result["alert_message"] != "":
            request.session["alert_message"] = search_result["alert_message"]
        request.session["search_result"] = search_result

        return redirect("toyosu_campus_navi:index")


# -------------------豊洲キャンパスナビ対象外 ここから-------------------


# /demo/guide
# 経路案内のデモ画面
class DemoIndexView(View):
    def get(self, request):
        nodes = list(navi.nodes.keys())
        nodes[:] = [x for x in nodes if not x.startswith("中継_")]
        return render(
            request,
            "toyosu_campus_navi/demo_index.html",
            {
                "nodes": nodes,
                "map_image_file": "map4F.png",
                "start": " ---- ",
                "goal": " ---- ",
            },
        )

    def post(self, request):
        start = request.POST["form_start"]
        goal = request.POST["form_goal"]
        shortest_path_string = ""
        estimated_time = ""
        map_image_file = "map4F.png"
        if start != "" and goal != "":
            try:
                if start == goal:
                    shortest_path_string = "出発地点と目標地点が同じです"
                else:
                    shortest_path, estimated_time = navi.shortestPath(start, goal)
                    estimated_time = round(estimated_time)
                    map.drow_arrows(shortest_path)
                    shortest_path_string = " → ".join(shortest_path)
                    map_image_file = "demo_output/output.png"
            except Exception:
                shortest_path_string = "取得できませんでした"

        if start == "":
            start = " ---- "
        if goal == "":
            goal = " ---- "
        nodes = list(navi.nodes.keys())
        nodes[:] = [x for x in nodes if not x.startswith("中継_")]
        return render(
            request,
            "toyosu_campus_navi/demo_index.html",
            {
                "start": start,
                "goal": goal,
                "shortest_path_string": shortest_path_string,
                "nodes": nodes,
                "map_image_file": map_image_file,
                "estimated_time": estimated_time,
            },
        )


# /plot
# 地図データ作成用の画像座標取得アプリ
class PlotView(View):
    def get(self, request):
        return render(
            request,
            "toyosu_campus_navi/plot.html",
        )


# /debug
# ここを書き換えて、/deubugにアクセスする
class DebugView(View):
    def get(self, request):
        from managements import Section

        objects = Section.objects.filter(building="交流棟")
        for object in objects:
            object.delete()

        return redirect("toyosu_campus_navi:index")


# -------------------豊洲キャンパスナビ対象外 ここまで-------------------


index = IndexView.as_view()
user_login = UserLoginView.as_view()
chatbot_submit = ChatBotView.as_view()
language_submit = LanguageView.as_view()
search_submit = SearchView.as_view()
coordinate_submit = CoordinateSubmitView.as_view()
notice = NoticeView.as_view()
notice_management = NoticeManagementView.as_view()
notice_edit = NoticeEditView.as_view()
notice_delete = NoticeDeleteView.as_view()
notice_submit = NoticeSubmitView.as_view()
history = HistoryView.as_view()
identify_wing = IdentifyWingView.as_view()
plot = PlotView.as_view()
demo_index = DemoIndexView.as_view()
debug = DebugView.as_view()
