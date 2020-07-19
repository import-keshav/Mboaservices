from django.conf.urls import url
from django.urls import path

from . import consumers

websocket_urlpatterns = [
	path('invigilator/chat/<str:room_name>', consumers.ChatConsumer),
	path('invigilator/get-incoming-order/<int:invigilator_id>', consumers.GetIncomingOrderForInvigilator),
]