from django.contrib.auth import authenticate, login
from django.conf import settings
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
