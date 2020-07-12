from django.urls import path

from . import views

urlpatterns = [
	path('get-invigilator-client-chat/<int:invigilator>/<int:client>', views.GetInvigilatorClientChat.as_view())
]