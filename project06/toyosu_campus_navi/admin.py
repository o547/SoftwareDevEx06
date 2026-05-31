from django.contrib import admin
from .models import Edge, History, Notice, Section, UserInfo

admin.site.register(UserInfo)
admin.site.register(Notice)
admin.site.register(History)
admin.site.register(Section)
admin.site.register(Edge)