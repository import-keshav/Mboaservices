from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from Invigilator import routing as invigilator_routing
from Orders import routing as orders_routing

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                invigilator_routing.websocket_urlpatterns +
                orders_routing.websocket_urlpatterns
            )
        )
    )
})
