from django.contrib.auth import authenticate, get_user_model
from .models import *
User = get_user_model()



# C8履歴管理部
class HistoryInfoManegement:
    pass


# C9お知らせ管理部
class NoticeManegement:
    pass


# C10ユーザ情報管理部
class UserInfoManegement:

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
class SectionInfoManegement:
    pass


# C16経路管理部
class routeManagement:
    def get_node_coodinate(self, request, section_name):
        try:
            building, floor, section = str(section_name).split("_")
        except:
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

    def get_all_node_coodinates(self, request):
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
