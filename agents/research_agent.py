from langchain.agents import create_agent

from multi_agent_system.config import get_model
from multi_agent_system.tools.research_tools import search_web, summarize_text

RESEARCH_PROMPT = (
    "You are a research specialist. "
    "Use search_web to gather information and summarize_text to condense findings. "
    "Return clear, factual bullet points with sources when available. "
    "Always confirm what you found in your final response."
)


def create_research_agent():
    return create_agent(
        get_model(),
        tools=[search_web, summarize_text],
        system_prompt=RESEARCH_PROMPT,
    )
