"""
LangGraph handoffs pattern: agents transfer control via Command tools.
Research -> Writer -> Reviewer pipeline with optional handoffs.
"""

from typing import Literal

from langchain.agents import AgentState, create_agent
from langchain.messages import AIMessage, ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command
from typing_extensions import NotRequired

from multi_agent_system.config import get_model
from multi_agent_system.tools.research_tools import search_web, summarize_text
from multi_agent_system.tools.writer_tools import format_markdown, save_document


class PipelineState(AgentState):
    active_agent: NotRequired[str]
    draft: NotRequired[str]


def build_handoff_graph():
    model = get_model()

    @tool
    def transfer_to_writer(runtime: ToolRuntime) -> Command:
        """Hand off to the writer after research is complete."""
        last_ai = next(
            msg for msg in reversed(runtime.state["messages"]) if isinstance(msg, AIMessage)
        )
        return Command(
            goto="writer",
            update={
                "active_agent": "writer",
                "messages": [
                    last_ai,
                    ToolMessage(
                        content="Research complete. Transferred to writer.",
                        tool_call_id=runtime.tool_call_id,
                    ),
                ],
            },
            graph=Command.PARENT,
        )

    @tool
    def transfer_to_reviewer(runtime: ToolRuntime) -> Command:
        """Hand off to the reviewer after writing is complete."""
        last_ai = next(
            msg for msg in reversed(runtime.state["messages"]) if isinstance(msg, AIMessage)
        )
        draft = last_ai.content if isinstance(last_ai.content, str) else str(last_ai.content)
        return Command(
            goto="reviewer",
            update={
                "active_agent": "reviewer",
                "draft": draft,
                "messages": [
                    last_ai,
                    ToolMessage(
                        content="Draft ready. Transferred to reviewer.",
                        tool_call_id=runtime.tool_call_id,
                    ),
                ],
            },
            graph=Command.PARENT,
        )

    @tool
    def transfer_to_research(runtime: ToolRuntime) -> Command:
        """Return to research if more information is needed."""
        last_ai = next(
            msg for msg in reversed(runtime.state["messages"]) if isinstance(msg, AIMessage)
        )
        return Command(
            goto="research",
            update={
                "active_agent": "research",
                "messages": [
                    last_ai,
                    ToolMessage(
                        content="More research needed. Transferred back to research.",
                        tool_call_id=runtime.tool_call_id,
                    ),
                ],
            },
            graph=Command.PARENT,
        )

    research_node_agent = create_agent(
        model,
        tools=[search_web, summarize_text, transfer_to_writer],
        system_prompt=(
            "You are the research phase of a content pipeline. "
            "Use search_web and summarize_text to gather facts, then call transfer_to_writer "
            "when you have enough material for a document."
        ),
    )

    writer_node_agent = create_agent(
        model,
        tools=[format_markdown, save_document, transfer_to_reviewer, transfer_to_research],
        system_prompt=(
            "You are the writing phase. Use format_markdown to produce a polished document. "
            "Call transfer_to_reviewer when done, or transfer_to_research if more facts are needed."
        ),
    )

    reviewer_node_agent = create_agent(
        model,
        tools=[],
        system_prompt=(
            "You are the final reviewer. Score the content 1-10, list improvements, "
            "and say APPROVED if it meets quality standards."
        ),
    )

    def call_research(state: PipelineState) -> dict:
        return research_node_agent.invoke(state)

    def call_writer(state: PipelineState) -> dict:
        return writer_node_agent.invoke(state)

    def call_reviewer(state: PipelineState) -> dict:
        return reviewer_node_agent.invoke(state)

    def route_after_agent(
        state: PipelineState,
    ) -> Literal["research", "writer", "reviewer", "__end__"]:
        messages = state.get("messages", [])
        if messages:
            last = messages[-1]
            if isinstance(last, AIMessage) and not last.tool_calls:
                return "__end__"
        return state.get("active_agent") or "research"

    def route_initial(state: PipelineState) -> Literal["research", "writer", "reviewer"]:
        return state.get("active_agent") or "research"

    builder = StateGraph(PipelineState)
    builder.add_node("research", call_research)
    builder.add_node("writer", call_writer)
    builder.add_node("reviewer", call_reviewer)

    builder.add_conditional_edges(START, route_initial, ["research", "writer", "reviewer"])
    builder.add_conditional_edges(
        "research", route_after_agent, ["research", "writer", "reviewer", END]
    )
    builder.add_conditional_edges(
        "writer", route_after_agent, ["research", "writer", "reviewer", END]
    )
    builder.add_conditional_edges(
        "reviewer", route_after_agent, ["research", "writer", "reviewer", END]
    )

    return builder.compile()
