# chat/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Room, Message


def index(request):
    print("🏠 INDEX VIEW called")
    rooms = Room.objects.all()
    print(f"📋 Found {rooms.count()} rooms")
    for room in rooms:
        print(f"  - {room.name} (created: {room.created_at})")
    return render(request, 'chat/index.html', {'rooms': rooms})


def room(request, room_name):
    print(f"🚪 ROOM VIEW called for: {room_name}")

    room_obj, created = Room.objects.get_or_create(name=room_name)
    print(f"🏠 Room {'created' if created else 'found'}: {room_obj.name}")

    messages = Message.objects.filter(room=room_obj).order_by('timestamp')[:50]
    print(f"💬 Found {messages.count()} messages in room {room_name}")

    for msg in messages:
        print(f"  - {msg.user.username}: {msg.content[:30]}...")

    context = {
        'room_name': room_name,
        'messages': messages
    }
    print(f"📦 Context: room_name={room_name}, messages_count={messages.count()}")

    return render(request, 'chat/room.html', context)


def get_messages(request, room_name):
    print(f"📨 GET_MESSAGES API called for room: {room_name}")

    room_obj = get_object_or_404(Room, name=room_name)
    messages = Message.objects.filter(room=room_obj).order_by('timestamp')

    messages_data = [{
        'username': msg.user.username,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%H:%M')
    } for msg in messages]

    print(f"📋 Returning {len(messages_data)} messages")
    return JsonResponse({'messages': messages_data})