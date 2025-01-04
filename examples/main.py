import os
from typing import List, Tuple

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from ragui import RagUI

# Load environment variables from .env file
load_dotenv()

# Verify API key is present
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY not found in environment variables. Export it first: `export OPENAI_API_KEY=your_key`"
    )

ragui = RagUI()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "user",
            """
            Based on the following context, answer the user's question.
            Context: {context}
            User question: {user_message}
            """,
        )
    ]
)

chain = prompt | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()

streaming_chain = prompt


@ragui.pipeline("My Pipeline")
async def mypipeline(
    query: str,
    message_history: List[Tuple[str, str]],
    user_context: dict,
):
    """
    RAG pipeline that retrieves relevant context and generates an answer.
    """
    async for chunk in chain.astream(
        {"context": message_history, "user_message": query}
    ):
        yield chunk
