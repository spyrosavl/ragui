# RagUI

RagUI is a Python framework that transforms your RAG (Retrieval Augmented Generation) pipelines into production-ready web applications. It's framework-agnostic and works seamlessly with popular LLM frameworks like LangChain and LlamaIndex.

## Features

- **Instant Web Interface**: Get a polished chat UI for your RAG pipeline with zero frontend code
- **Production Ready**: Built on FastAPI and async Python for high performance
- **Framework Agnostic**: Works with LangChain, LlamaIndex, or your custom LLM implementation
- **Fast Onboarding**: Adapt any existing RAG pipeline with minimal changes

**Coming Soon:**
- 💾 Conversation History & Analytics
- 🔄 Feedback Collection & Fine-tuning
- 🔒 Authentication & User Management
- 📊 Admin Dashboard
- 💰 Subscription Management

## Alternatives
| **Feature**                           | **RagUI**               | **Streamlit**                     | **Gradio**                        |
|--------------------------------------|:-----------------------:|:---------------------------------:|:---------------------------------:|
| **Production Focus**                 | ✅ Built on FastAPI     | ⚠️ Possible but manual setup      | ⚠️ Commonly used for demos          |
| **RAG-Centric**                      | ✅ Purpose-built        | ❌ General-purpose                | ❌ General-purpose                |
| **Multiple Pipelines**               | 🚧 On roadmap           | ❌ Must wire manually             | ❌ Must wire manually             |
| **Conversation Persistence**         | 🚧 On roadmap           | ❌ Manual DB integration          | ❌ Manual DB integration          |
| **Feedback Collection**              | 🚧 On roadmap           | ❌ Custom coding                  | ❌ Custom coding                  |
| **User Authentication**              | 🚧 On roadmap           | ❌ No built-in                    | ❌ No built-in                    |
| **Usage Metrics**                    | 🚧 On roadmap           | ❌ Need external services         | ❌ Need external services         |
| **Admin Dashboard**                  | 🚧 On roadmap           | ❌ Custom or third-party          | ❌ Custom or third-party          |


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

### Phase 1: Core Functionality (MVP)
- [ ] **Simple UI for text input/output**
  - The essential starting point: a user-friendly interface for sending and receiving messages.

- [ ] **Messages Persistence (Database)**
  - Store chat data for future reference, analytics, and advanced features.

- [ ] **Conversation History**
  - Enable users to review previous messages and maintain context across sessions.

### Phase 2: Feature Expansion
- [ ] **Support for Multiple Pipelines**
  - Allow different RAG flows or LLM backends within a single deployment.

- [ ] **Feedback Collection**
  - Gather user feedback for iterative improvements and model fine-tuning.

- [ ] **Support for File Input**
  - Accept documents, PDFs, or other file types as context sources for RAG.

- [ ] **Support for Audio Input**
  - Expand interaction possibilities by handling voice-based queries.

### Phase 3: Production Hardening
- [ ] **User Authentication**
  - Secure access control, user profiles, and personalized interactions.

- [ ] **Usage Metrics**
  - Track requests, errors, response times, and user engagement to guide scaling.

- [ ] **Admin Dashboard**
  - Centralize management of pipelines, users, and overall system health.

### Phase 4: Monetization & Advanced Integrations
- [ ] **Subscription Management**
  - Implement billing, tiered plans, and payment handling for monetized deployments.

- [ ] **Add to Website Support (Chat Bubble)**
  - Easily embed RagUI as a widget on external websites for broader audience reach.
