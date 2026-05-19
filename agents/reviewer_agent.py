from langchain.agents import create_agent

from multi_agent_system.config import get_model

REVIEWER_PROMPT = (
    "You are a quality reviewer. "
    "Evaluate content for accuracy, clarity, completeness, and structure. "
    "Provide a score from 1-10 and specific improvement suggestions. "
    "If the content is ready, say APPROVED; otherwise list required changes."
)


def create_reviewer_agent():
  return create_agent(
      get_model(),
      tools=[],
      system_prompt=REVIEWER_PROMPT,
  )
