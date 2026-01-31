from django.urls import path
from . import views

app_name = 'ai_chat'

urlpatterns = [
    path('chat/send/', views.send_message, name='send_message'),
]
