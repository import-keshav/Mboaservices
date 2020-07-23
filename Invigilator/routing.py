from django.conf.urls import url
from django.urls import path

from . import consumers

websocket_urlpatterns = [
	path('invigilator/chat/<str:room_name>', consumers.ClientToInvigilator),
	path('invigilator/chat/<str:room_name>/<str:person>', consumers.ClientsToInvigilator),
	path('invigilator/get-incoming-order/<int:invigilator_id>', consumers.GetIncomingOrderForInvigilator),
]