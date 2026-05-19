"""
LangGraph supervisor pattern using create_react_agent + langgraph-supervisor.
Each worker is a ReAct agent; the supervisor routes between them.
"""

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

from multi_agent_system.config import get_model
from multi_agent_system.tools.code_tools import execute_python, search_code_snippets
from multi_agent_system.tools.research_tools import search_web, summarize_text
from multi_agent_system.tools.writer_tools import format_markdown, save_document

RESEARCH_PROMPT = (
    "You are a research agent. Use search_web and summarize_text. "
    "Return concise factual findings."
)
WRITER_PROMPT = (
    "You are a writer agent. Use format_markdown and save_document. "
    "Produce polished Markdown output."
)
CODER_PROMPT = (
    "You are a coder agent. Use search_code_snippets and execute_python. "
    "Write and explain Python code."
)


def build_supervisor_graph():
    model = get_model()
    # langgraph-supervisor expects a model object with bind_tools support
    if not isinstance(model, ChatOpenAI):
        llm = ChatOpenAI(model="gpt-4o-mini")
    else:
        llm = model

    research_agent = create_react_agent(
        model=llm,
        tools=[search_web, summarize_text],
        name="research_agent",
        prompt=RESEARCH_PROMPT,
    )

    writer_agent = create_react_agent(
        model=llm,
        tools=[format_markdown, save_document],
        name="writer_agent",
        prompt=WRITER_PROMPT,
    )

    coder_agent = create_react_agent(
        model=llm,
        tools=[execute_python, search_code_snippets],
        name="coder_agent",
        prompt=CODER_PROMPT,
    )

    workflow = create_supervisor(
        agents=[research_agent, writer_agent, coder_agent],
        model=llm,
        prompt=(
            "You are a supervisor managing a research, writer, and coder team. "
            "Assign work to the best agent. For reports: research first, then writer. "
            "For code tasks: use coder_agent. Respond with the team's final output."
        ),
    )

    return workflow.compile()
