from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/discussion/(?P<room_id>[-\w]+)/$', consumers.DiscussionConsumer.as_asgi()),
]
