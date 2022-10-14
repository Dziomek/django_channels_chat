from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Room, Message
from .utils import count_messages


@login_required
def rooms(request):
    messages_counted = []
    room_objects = Room.objects.all()
    for room_object in room_objects:
        messages_counted.append(count_messages(room_object))

    print(messages_counted)

    return render(request, 'chat/rooms.html', {'rooms': room_objects, 'messages_counted': messages_counted})


@login_required
def room(request, slug):
    room_object = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room_object)

    return render(request, 'chat/room.html', {'room': room_object, 'messages': messages})


@login_required
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        password = request.POST['password']
        room_object = Room(name=room_name, password=password, admin=request.user)
        room_object.save()

    return redirect('rooms')


@login_required
def enter_room_password(request, room_name):
    room_object = Room.objects.get(name=room_name)
    if not room_object.password:
        return redirect('room', slug=room_object.slug)

    return render(request, 'chat/enter_password.html', {'room_name': room_name})


@login_required
def join_room(request, room_name):
    if request.method == 'POST':
        room_object = Room.objects.get(name=room_name)
        if not room_object.password:
            return redirect('room', slug=room_object.slug)

        password = request.POST['password']
        if password == room_object.password:
            return redirect('room', slug=room_object.slug)

    return redirect('rooms')
