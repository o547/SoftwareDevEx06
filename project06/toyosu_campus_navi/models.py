from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# F1 ユーザ情報
# デフォルトのUserの拡張項目
class UserInfo(AbstractUser):
    language = models.CharField(max_length=16, default="JA")


# F2 お知らせ情報
class Notice(models.Model):
    notice_ID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    title = models.TextField(max_length=127, verbose_name="タイトル")
    body = models.TextField(blank=False, verbose_name="本文")


# F3 履歴情報
class History(models.Model):
    history_ID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="ユーザー"
    )
    start_section = models.ForeignKey(
        "Section",
        on_delete=models.CASCADE,
        verbose_name="開始地",
        related_name="start_section",
    )
    goal_section = models.ForeignKey(
        "Section",
        on_delete=models.CASCADE,
        verbose_name="目的地",
        related_name="goal_section",
    )


# F4 区画情報
class Section(models.Model):
    section_ID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID"
    )
    building = models.CharField(max_length=128, verbose_name="棟")
    floor = models.CharField(max_length=128, verbose_name="階")
    section = models.CharField(max_length=128, verbose_name="区画")
    node_x = models.BigIntegerField(verbose_name="ノードx座標")
    node_y = models.BigIntegerField(verbose_name="ノードy座標")
    top_left_x = models.BigIntegerField(null=True, verbose_name="区画の左上x座標")
    top_left_y = models.BigIntegerField(null=True, verbose_name="区画の左上y座標")
    bottom_right_x = models.BigIntegerField(null=True, verbose_name="区画の右下x座標")
    bottom_right_y = models.BigIntegerField(null=True, verbose_name="区画の右下y座標")
    usage = models.CharField(null=True, max_length=1023, verbose_name="使用用途")
    capacity = models.BigIntegerField(null=True, verbose_name="収容人数")
    business_hours = models.CharField(
        null=True, max_length=1023, verbose_name="営業時間"
    )

    def __str__(self):
        return f"{self.building}_{self.floor}_{self.section}"


# F5 エッジ情報
class Edge(models.Model):
    edge_ID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID"
    )
    section_a = models.ForeignKey(
        "Section",
        on_delete=models.CASCADE,
        verbose_name="区画A",
        related_name="section_a",
    )
    section_b = models.ForeignKey(
        "Section",
        on_delete=models.CASCADE,
        verbose_name="区画B",
        related_name="section_b",
    )
    estimated_travel_time = models.BigIntegerField(
        null=True, verbose_name="推定移動時間(ミリ秒)"
    )
