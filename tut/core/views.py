# django
from asgiref.sync import async_to_sync
from django.shortcuts import render
from django.http import HttpResponse


# channels
from channels.layers import get_channel_layer

# Create your views here.


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', context={
        'room_name': room_name
    })


def sroom(request, room_name):
    return render(request, 'chat/room.html', context={
        'room_name': room_name,
        's_chat': True
    })


def flood_messages(request, room_name):
    '''
    Open
    /chat/<room_no>/ # async
    /chat/s/<room_no>/ # sync
    concurrently to see the diff
    '''
    layer = get_channel_layer()
    range_size = 100
    counter = 0
    for i in range(0, range_size):
        counter += 1
        async_to_sync(layer.group_send)(
            "chat_"+str(room_name),
            {
                'type': 'incoming_flood',
                'value': counter
            }
        )
    return HttpResponse(content={'testOver'}, status=200)
