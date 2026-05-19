from langchain.tools import tool


@tool
def execute_python(code: str) -> str:
    """Execute Python code in a sandbox and return stdout or errors."""
    # Stub: use a real sandbox (e.g. E2B, Docker) in production
    if "print" in code:
        return "stdout: Code executed successfully (sandbox stub)."
    return "stdout: (no output)"


@tool
def search_code_snippets(query: str, language: str = "python") -> str:
    """Search for code examples matching a query."""
    return (
        f"[{language} snippets for: {query}]\n"
        "```python\n"
        "from langgraph.prebuilt import create_react_agent\n"
        "agent = create_react_agent(model, tools=[my_tool])\n"
        "```"
    )
