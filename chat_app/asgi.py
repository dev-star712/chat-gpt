"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

import apps.chat.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

application = ProtocolTypeRouter(
    {
        "http":get_asgi_application(),
        "websocket":AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(apps.chat.routing.websocket_urlpatterns))
        )
    }
)
