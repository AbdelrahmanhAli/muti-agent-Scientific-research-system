from langchain.agents import create_agent

from multi_agent_system.config import get_model
from multi_agent_system.tools.code_tools import execute_python, search_code_snippets

CODER_PROMPT = (
    "You are a Python coding specialist. "
    "Use search_code_snippets to find examples and execute_python to run code. "
    "Write clean, idiomatic code with brief explanations. "
    "Always show the final code in your response."
)


def create_coder_agent():
  return create_agent(
      get_model(),
      tools=[execute_python, search_code_snippets],
      system_prompt=CODER_PROMPT,
  )
