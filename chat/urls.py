from django.conf.urls import url
import chat.views

urlpatterns = [
    url(r'^$', chat.views.home, name='home'),
    url(r'^rooms/(?P<room_id>[0-9]+)/$', chat.views.display_chat_room, name='chat_room'),
    url(r'^post/', chat.views.add_post, name='add_post'),
    url(r'^login/', chat.views.login, name='login'),
    url(r'^logout/', chat.views.logout, name='logout'),
    url(r'^register/', chat.views.register, name='register'),
    url(r'^messages/', chat.views.messages, name='messages')


]