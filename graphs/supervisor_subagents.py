"""
LangChain subagents pattern: supervisor coordinates specialists wrapped as tools.
"""

from langchain.agents import create_agent
from langchain.tools import tool

from multi_agent_system.agents.coder_agent import create_coder_agent
from multi_agent_system.agents.research_agent import create_research_agent
from multi_agent_system.agents.reviewer_agent import create_reviewer_agent
from multi_agent_system.agents.writer_agent import create_writer_agent
from multi_agent_system.config import get_model

SUPERVISOR_PROMPT = (
    "You are a project coordinator managing a team of specialists. "
    "Delegate tasks to the right expert:\n"
    "- research_expert: gather information, facts, and summaries\n"
    "- writer_expert: create documents, articles, and formatted content\n"
    "- coder_expert: write and run Python code\n"
    "- reviewer_expert: review and score final deliverables\n"
    "For complex requests, use multiple tools in sequence. "
    "Synthesize all results into one coherent final answer."
)


def build_subagent_supervisor():
    research = create_research_agent()
    writer = create_writer_agent()
    coder = create_coder_agent()
    reviewer = create_reviewer_agent()

    @tool
    def research_expert(request: str) -> str:
        """Gather information and research on any topic.

        Use for fact-finding, literature review, or summarizing sources.
        Input: natural language research request.
        """
        result = research.invoke({"messages": [{"role": "user", "content": request}]})
        return result["messages"][-1].text

    @tool
    def writer_expert(request: str) -> str:
        """Write and format documents in Markdown.

        Use for articles, reports, tutorials, or documentation.
        Input: natural language writing request with any source material.
        """
        result = writer.invoke({"messages": [{"role": "user", "content": request}]})
        return result["messages"][-1].text

    @tool
    def coder_expert(request: str) -> str:
        """Write and execute Python code.

        Use for scripts, examples, debugging, or code generation.
        Input: natural language coding request.
        """
        result = coder.invoke({"messages": [{"role": "user", "content": request}]})
        return result["messages"][-1].text

    @tool
    def reviewer_expert(content: str) -> str:
        """Review content for quality, accuracy, and completeness.

        Use after research or writing is done to validate deliverables.
        Input: the content to review.
        """
        result = reviewer.invoke(
            {"messages": [{"role": "user", "content": f"Review this:\n\n{content}"}]}
        )
        return result["messages"][-1].text

    return create_agent(
        get_model(),
        tools=[research_expert, writer_expert, coder_expert, reviewer_expert],
        system_prompt=SUPERVISOR_PROMPT,
    )
