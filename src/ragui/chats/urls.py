from django.urls import re_path

from . import views

websocket_urlpatterns = [
    re_path(
        r"^api/v1/chats/ws/chat/(?P<pipeline_id>[\w-]+)/?$",
        views.ChatConsumer.as_asgi(),
    ),
]

urlpatterns = [
    re_path(r"^pipeline/(?P<pipeline_id>[\w-]+)/?$", views.ConfigView.as_view()),
    re_path(r"^pipelines/?$", views.PipelinesView.as_view()),
    re_path(r"^health/?$", views.HealthCheckView.as_view()),
]
