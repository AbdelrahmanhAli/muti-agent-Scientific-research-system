from langchain.tools import tool


@tool
def format_markdown(content: str, title: str = "Document") -> str:
    """Format content as a structured Markdown document with a title and sections."""
    return f"# {title}\n\n{content.strip()}\n"


@tool
def save_document(content: str, filename: str = "output.md") -> str:
    """Save content to a file (stub). Returns confirmation."""
    return f"Document saved to {filename} ({len(content)} characters)"
