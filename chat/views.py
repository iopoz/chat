from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, render_to_response

# Create your views here.
from django.template.context_processors import csrf

from chat.forms import NewMessageForm
from chat.models import ChatRooms, Subject, Chat


def home(request):
    chat_rooms = ChatRooms.objects.all()
    subjects = Subject.objects.all()
    user = auth.get_user(request).username
    rooms = []
    room_info = {}
    for room in chat_rooms:
        room_info['room'] = room
        room_info['msg_count'] = len(Chat.objects.filter(msg_room=room.id))
        rooms.append(room_info)
        room_info = {}
    n = 1
    while n < len(rooms):
        for i in range(len(rooms) - n):
            if rooms[i]['msg_count'] > rooms[i + 1]['msg_count']:
                rooms[i], rooms[i + 1] = rooms[i + 1], rooms[i]
        n += 1
    sorted_rooms = rooms[-5:]
    rooms = []
    for room in reversed(sorted_rooms):
        rooms.append(room['room'])
    context = {
        'rooms': rooms,
        'subjects': subjects,
        'username': user
    }
    return render(request, 'home.html', context)


def display_chat_room(request, room_id):
    msg_form = NewMessageForm(request.POST)
    context = {'msgs': Chat.objects.filter(msg_room=room_id),
               'username': auth.get_user(request).username,
               'form': msg_form,
               'subjects': Subject.objects.all()}

    return render(request, 'chat_room.html', context)


def login(request):
    context = {}
    context['login_error'] = 'Incorrect data!'
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(request.META.get('HTTP_REFERER'), context)
    else:
        return redirect(request.META.get('HTTP_REFERER'), context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register(request):
    return True
