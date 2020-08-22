from django.conf.urls import url
from django.urls import path

from . import consumers as orders_consumers

websocket_urlpatterns = [
    path('orders/get-incoming-orders/<int:pk>', orders_consumers.IncomingRestaurantOrders),
    path('orders/update-get-order-status/<int:pk>', orders_consumers.UpdateGetOrderStatus),
]