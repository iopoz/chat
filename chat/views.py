from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response

# Create your views here.
from django.template.context_processors import csrf

from chat.forms import NewMessageForm, UserRegistrationForm
from chat.models import ChatRooms, Subject, Chat

ROOM_ID = None


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
    ROOM_ID = room_id
    msg_form = NewMessageForm(request.POST)
    context = {'msgs': Chat.objects.filter(msg_room=ROOM_ID),
               'username': auth.get_user(request).username,
               'form': msg_form,
               'subjects': Subject.objects.all(),
               'chat_room': ChatRooms.objects.get(id=ROOM_ID)}

    return render(request, 'chat_room.html', context)


def add_post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(msg_author=request.user, message=msg, msg_room=get_room_id(request, True))
        if msg != '':
            c.save()
        return JsonResponse({'msg': msg, 'user': c.msg_author.username})
    else:
        return HttpResponse('Request must be POST.')


def messages(request):

    context = {'msgs': Chat.objects.filter(msg_room=get_room_id(request))}
    return render(request, 'messages.html', context)


def login(request):
    context = {}
    context.update(csrf(request))
    context['login_error'] = 'Incorrect data!'
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponse("Account is not active at the moment.")
    else:
        return redirect(request.META.get('HTTP_REFERER'), context)


def logout(request):
    context = {}
    context.update(csrf(request))
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register(request):
    context = {}
    context.update(csrf(request))
    if request.POST:
        new_user_form = UserRegistrationForm(request.POST)
        if new_user_form.is_valid():
            # user = User.objects.filter(email=request.POST['email'], user=request.POST['username'])
            # if user is None:
            new_user_form.save()
            new_user = auth.authenticate(
                username=new_user_form.cleaned_data['username'],
                password=new_user_form.cleaned_data['password2'])
            auth.login(request,new_user)
            return redirect('/')
        #else:
            #main_new_user_form = new_user_form
        context['error'] = new_user_form.error_messages
        context['email'] = new_user_form.cleaned_data.get('email')
        context['first_name'] = new_user_form.cleaned_data.get('first_name')
        context['last_name'] = new_user_form.cleaned_data.get('last_name')
        context['username'] = new_user_form.cleaned_data.get('username')
    #context['form'] = UserRegistrationForm()
    return render_to_response('registration.html', context)

def get_room_id(request, full=False):
    try:
        url_list = request.META.get('HTTP_REFERER').split('/')
        ROOM_ID = int(url_list[-2])
        if not full:
            return ROOM_ID
        else:
            return ChatRooms.objects.get(id=ROOM_ID)
    except ValueError:
        print('waitinf for chat room')
