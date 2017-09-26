from django.conf.urls import url
import chat.views

urlpatterns = [
    url(r'^$', chat.views.home, name='home'),
    url(r'^rooms/(?P<room_id>[0-9]+)/$', chat.views.display_chat_room, name='chat_room'),
    url(r'^login/', chat.views.login, name='login'),
    url(r'^logout/', chat.views.logout, name='logout'),
    url(r'^register/', chat.views.register, name='register'),

]