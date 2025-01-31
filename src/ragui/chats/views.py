import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import JsonResponse
from django.views import View

from .apps import ChatsConfig


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pipeline_id = self.scope["url_route"]["kwargs"]["pipeline_id"]
        ragui = ChatsConfig.get_ragui()

        if ragui is None:
            await self.close(code=1011)
            return

        if self.pipeline_id not in ragui.pipelines:
            await self.close(code=1011)
            return

        await self.accept()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            ragui = ChatsConfig.get_ragui()

            async for chunk in ragui.pipelines[self.pipeline_id].function(
                data["input"],
                [(m["type"], m["content"]) for m in data["chat_history"]],
                {},
            ):
                await self.send(text_data=chunk)

            await self.send(json.dumps({"status": "complete"}))

        except Exception as e:
            await self.send(json.dumps({"error": str(e)}))
            await self.close(code=1011)


class ConfigView(View):
    def get(self, request, pipeline_id):
        ragui = ChatsConfig.get_ragui()

        if ragui is None:
            return JsonResponse({"error": "RagUI not initialized"})

        if pipeline_id not in ragui.pipelines:
            return JsonResponse({"error": "Pipeline not found"})

        pipeline_config = ragui.pipelines[pipeline_id].dict()
        pipeline_config.pop("function")
        return JsonResponse(pipeline_config)


class PipelinesView(View):
    def get(self, request):
        ragui = ChatsConfig.get_ragui()
        return JsonResponse({k: v.title for k, v in ragui.pipelines.items()})


class HealthCheckView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"})
