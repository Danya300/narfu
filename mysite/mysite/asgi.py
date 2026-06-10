"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings.dev")

# Initialize Django ASGI application early to ensure settings are loaded
django_application = get_asgi_application()


async def application(scope, receive, send):
    """ASGI application wrapper for Granian."""
    if scope["type"] == "lifespan":
        # Handle lifespan protocol
        while True:
            message = await receive()
            if message["type"] == "startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                break
    else:
        # Delegate to Django ASGI application
        await django_application(scope, receive, send)
