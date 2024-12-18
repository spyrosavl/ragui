# RagUI

RagUI is a Python framework that transforms your RAG (Retrieval Augmented Generation) pipelines into production-ready web applications. It's framework-agnostic and works seamlessly with popular LLM frameworks like LangChain and LlamaIndex.

## Features

- **Instant Web Interface**: Get a polished chat UI for your RAG pipeline with zero frontend code
- **Production Ready**: Built on FastAPI and async Python for high performance
- **Developer Focused**: Focus on your RAG logic while we handle the infrastructure
- **Framework Agnostic**: Works with LangChain, LlamaIndex, or your custom LLM implementation
- **Flexible Integration**: Adapt any existing RAG pipeline with minimal changes

**Coming Soon:**
- 🔒 Authentication & User Management
- 📊 Admin Dashboard
- 💾 Conversation History & Analytics
- 💰 Subscription Management
- 🔄 Feedback Collection & Fine-tuning
- 📈 Usage Metrics & Monitoring

## Quick Start

```bash
pip install ragui
```

Create a pipeline (`main.py`):

```python
from ragui import RagUI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

ragui = RagUI()

# Define your LangChain components
prompt = ChatPromptTemplate.from_messages([
    ("user", "Context: {context}\nQuestion: {user_message}")
])
chain = prompt | ChatOpenAI() | StrOutputParser()

@ragui.pipeline("RAG Pipeline")
async def rag_pipeline(query, message_history, user_context):
    async for chunk in chain.astream({
        "context": "Your retrieved context here",
        "user_message": query
    }):
        yield chunk
```

Launch your application:

```bash
ragui main.py
```

Visit `http://localhost:8000` to interact with your pipeline.

## Why RagUI?

- **Save Development Time**: Focus on your RAG logic instead of building UI/infrastructure
- **Production Ready**: Built with production use-cases in mind
- **Future Proof**: As we add features, your application automatically gets upgrades
- **Full Control**: Customize and extend any aspect of the framework

## Roadmap
- [ ] Simple UI for text input/output
- [ ] Feedback collection
- [ ] Support files input
- [ ] Support for multiple pipelines
- [ ] Support for audio input
- [ ] Messages persistence (database)
- [ ] Conversation history
- [ ] User authentication
- [ ] Admin dashboard
- [ ] Add to website support (little chat bubble on the corner)
- [ ] Usage metrics
- [ ] Subscription management
