from langchain.agents import create_agent

from multi_agent_system.config import get_model
from multi_agent_system.tools.writer_tools import format_markdown, save_document

WRITER_PROMPT = (
    "You are a technical writer. "
    "Transform research or raw notes into polished Markdown documents. "
    "Use format_markdown for structure and save_document when the user wants output saved. "
    "Write clearly for developers. Always deliver the final document in your response."
)


def create_writer_agent():
  return create_agent(
      get_model(),
      tools=[format_markdown, save_document],
      system_prompt=WRITER_PROMPT,
  )
