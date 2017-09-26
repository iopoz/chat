from django.contrib import admin

from chat.models import Subject, ChatRooms, Chat


class SubjectAdmin(admin.ModelAdmin):
    fields = ['subject_name']


class MessageInLine(admin.TabularInline):
    model = Chat
    extra = 0


class RoomAdmin(admin.ModelAdmin):
    inlines = [MessageInLine]


admin.site.register(ChatRooms, RoomAdmin)
admin.site.register(Subject, SubjectAdmin)
