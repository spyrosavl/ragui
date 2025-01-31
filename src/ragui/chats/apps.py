import os

from django.apps import AppConfig

from ragui.api.loader import get_ragui_instance


class ChatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ragui.chats"
    _ragui = None

    @classmethod
    def get_ragui(cls):
        return cls._ragui

    def ready(self):
        if os.environ.get("RAGUI_SCRIPT", None):
            ChatsConfig._ragui = get_ragui_instance()
