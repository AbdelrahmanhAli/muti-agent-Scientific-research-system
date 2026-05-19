import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


def get_model():
    """Return the configured chat model."""
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return init_chat_model(model_name, model_provider="openai")
