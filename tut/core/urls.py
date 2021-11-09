from .views import index, room
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('<int:room_name>/', room, name='room'),
]
