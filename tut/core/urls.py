from .views import index, room, flood_messages, sroom
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('<int:room_name>/', room, name='room'),
    path('s/<int:room_name>/', sroom, name='sroom'),
    path('flood/<int:room_name>/', flood_messages),
]
