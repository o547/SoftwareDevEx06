from django.contrib.auth import authenticate, get_user_model
from .models import Edge, History, Notice, Section, UserInfo

User = get_user_model()


# C8履歴管理部
class HistoryInfoManagement:
    def save_history(self, request, username, start, goal):
        try:
            start_building, start_floor, start_section = str(start).split("_")
            goal_building, goal_floor, goal_section = str(goal).split("_")
        except ValueError:
            return False

        start_section_object = Section.objects.filter(
            building=start_building, floor=start_floor, section=start_section
        ).first()

        goal_section_object = Section.objects.filter(
            building=goal_building, floor=goal_floor, section=goal_section
        ).first()

        user_object = User.objects.filter(username=username).first()

        if (
            (start_section_object is not None)
            and (goal_section_object is not None)
            and (user_object is not None)
        ):
            try:
                History.objects.create(
                    user=user_object,
                    start_section=start_section_object,
                    goal_section=goal_section_object,
                )
            except Exception as e:
                print(e)
                return False
            return True

        else:
            return False

    def get_all_histories(self, request, username):
        try:
            user_object = User.objects.filter(username=username).first()
            all_history_object = History.objects.all().filter(user=user_object)
            histories = []

            for history_object in all_history_object:
                start_section_name = (
                    history_object.start_section.building
                    + "_"
                    + history_object.start_section.floor
                    + "_"
                    + history_object.start_section.section
                )
                goal_section_name = (
                    history_object.goal_section.building
                    + "_"
                    + history_object.goal_section.floor
                    + "_"
                    + history_object.goal_section.section
                )
                histories.append(
                    {
                        "history_id": history_object.history_ID,
                        "start_section_name": start_section_name,
                        "goal_section_name": goal_section_name,
                    }
                )
            return histories
        except Exception as e:
            print(e)
            return []


# C9お知らせ管理部
class NoticeManagement:
    def create_notice(self, request, title, body):
        try:
            Notice.objects.create(
                title=title,
                body=body,
            )
        except Exception as e:
            print(e)
            return False
        return True

    def update_notice(self, request, id, title, body):
        try:
            notice_object = Notice.objects.get(notice_ID=id)
            notice_object.title = title
            notice_object.body = body
            notice_object.save()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_notice(self, request, id):
        try:
            notice_object = Notice.objects.get(notice_ID=id)
            notice_object.delete()
            return True
        except Exception as e:
            print(e)
            return False

    def get_notice(self, request, id):
        notice_object = Notice.objects.filter(notice_ID=id).first()
        if notice_object is not None:
            return {
                "title": notice_object.title,
                "body": notice_object.body,
                "created_at": notice_object.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": notice_object.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        else:
            return {
                "title": "",
                "body": "",
                "created_at": "",
                "updated_at": "",
            }

    def get_all_notices(self, request):
        all_notice_object = Notice.objects.all()
        notices = []

        for notice_object in all_notice_object:
            notices.append(
                {
                    "notice_id": notice_object.notice_ID,
                    "title": notice_object.title,
                    "body": notice_object.body,
                    "created_at": notice_object.created_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "updated_at": notice_object.updated_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
            )
        return notices


# C10ユーザ情報管理部
class UserInfoManagement:
    def check_existence(self, request, username):
        if User.objects.filter(username=username).exists():
            return True
        return False

    def certification(self, request, username, password):
        return authenticate(request, username=username, password=password)

    def user_regist(self, request, username, password):
        return User.objects.create_user(username, "", password)

    def save_language(self, request, language, username):
        if User.objects.filter(username=username).update(language=language):
            return True
        else:
            return False


# C12区画情報管理部
class SectionInfoManagement:
    pass


# C16経路管理部
class RouteManagement:
    def get_node_coordinate(self, request, section_name):
        try:
            building, floor, section = str(section_name).split("_")
        except ValueError:
            return {"section_id": None, "node_x": -1, "node_y": -1}

        section_object = Section.objects.filter(
            building=building, floor=floor, section=section
        ).first()

        if section_object is not None:
            return {
                "section_id": section_object.section_ID,
                "node_x": section_object.node_x,
                "node_y": section_object.node_y,
            }
        else:
            return {"section_id": None, "node_x": -1, "node_y": -1}

    def get_all_node_coordinates(self, request):
        all_section_object = Section.objects.all()
        nodes = []
        for section_object in all_section_object:
            section_name = (
                section_object.building
                + "_"
                + section_object.floor
                + "_"
                + section_object.section
            )
            nodes.append(
                {
                    "section_name": section_name,
                    "section_id": section_object.section_ID,
                    "node_x": section_object.node_x,
                    "node_y": section_object.node_y,
                }
            )
        return nodes

    def get_all_edges(self, request):
        all_edge_object = Edge.objects.all()
        edges = []
        for edge_object in all_edge_object:
            section_name_a = (
                edge_object.section_a.building
                + "_"
                + edge_object.section_a.floor
                + "_"
                + edge_object.section_a.section
            )
            section_name_b = (
                edge_object.section_b.building
                + "_"
                + edge_object.section_b.floor
                + "_"
                + edge_object.section_b.section
            )
            edges.append(
                {"section_name_a": section_name_a, "section_name_b": section_name_b}
            )
        return edges
