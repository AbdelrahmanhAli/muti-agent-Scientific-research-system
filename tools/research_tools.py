from langchain.tools import tool


@tool
def search_web(query: str) -> str:
    """Search the web for information on a topic. Returns summarized findings."""
    # Stub: replace with Tavily, DuckDuckGo, or SerpAPI in production
    return (
        f"[Research results for: {query}]\n"
        "- LangGraph enables stateful multi-agent workflows with cycles and persistence.\n"
        "- LangChain agents use tools in a loop until the task is complete.\n"
        "- Supervisor patterns route tasks to specialized sub-agents.\n"
        "- Handoffs transfer control between agents via Command updates."
    )


@tool
def summarize_text(text: str, max_sentences: int = 3) -> str:
    """Summarize a block of text into key bullet points."""
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    summary = sentences[:max_sentences]
    return "\n".join(f"- {s}." for s in summary)
