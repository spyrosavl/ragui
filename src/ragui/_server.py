import os
from pathlib import Path
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI()
ragui = None


@app.on_event("startup")
def load_ragui():
    global ragui
    script_path = os.getenv("RAGUI_SCRIPT")
    if not script_path:
        raise RuntimeError("RAGUI_SCRIPT environment variable not set")

    namespace = {}
    with open(script_path) as f:
        exec(f.read(), namespace)

    if "ragui" not in namespace:
        raise RuntimeError("No RagUI instance found in script")

    ragui = namespace["ragui"]


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Since we're serving UI from same origin, this is less critical
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    type: str = Field(..., title="Message type", description="Type of message")
    content: str = Field(..., title="Message content", description="Content of message")


class ChatInput(BaseModel):
    input: str = Field(..., title="User input", description="User input message")
    chat_history: List[Message] = Field(
        ..., title="Chat history", description="Chat history messages"
    )


@app.get("/api/config/{pipeline_id}")
async def get_config(pipeline_id: str):
    if ragui is None:
        return {"error": "RagUI not initialized"}

    if pipeline_id not in ragui.pipelines:
        return {"error": "Pipeline not found"}

    # Remove the `function` attribute from the pipeline config
    pipeline_config = ragui.pipelines[pipeline_id].dict()
    pipeline_config.pop("function")

    return pipeline_config


@app.websocket("/ws/chat/{pipeline_id}")
async def websocket_chat(websocket: WebSocket, pipeline_id: str):
    await websocket.accept()

    if ragui is None:
        await websocket.close(code=1011, reason="RagUI not initialized")
        return

    if pipeline_id not in ragui.pipelines:
        await websocket.close(code=1011, reason="Pipeline not found")
        return

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message = ChatInput(**data)

            # Process message through pipeline
            async for chunk in ragui.pipelines[pipeline_id].function(
                message.input,
                [(m.type, m.content) for m in message.chat_history],
                {},  # empty context for now
            ):
                await websocket.send_text(chunk)

    except WebSocketDisconnect:
        # Handle client disconnect
        pass
    except Exception as e:
        # Handle other errors
        await websocket.send_json({"error": str(e)})
        await websocket.close(code=1011)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/pipelines")
async def pipelines():
    return {k: v.title for k, v in ragui.pipelines.items()}


@app.get("/", response_class=HTMLResponse)
async def test_page():
    html_file = Path(__file__).parent / "templates" / "websocket_test.html"
    html_content = html_file.read_text()
    pipeline_id = "mypipeline"  # Or however you want to determine the default pipeline
    return html_content.replace("{{PIPELINE_ID}}", pipeline_id)
