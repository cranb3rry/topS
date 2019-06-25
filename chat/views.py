
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def index(request):
    return render(request, 'chat/index.html', {})

def vcmsg(request):
    return render(request, 'chat/vcmsg.html', {})

def vcmsgwidget(request):
    return render(request, 'chat/vcmsgwidget.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })