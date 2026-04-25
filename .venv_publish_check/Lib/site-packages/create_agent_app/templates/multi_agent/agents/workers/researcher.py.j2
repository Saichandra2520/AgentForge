"""Research worker node."""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from config import get_chat_model
from memory.state import MultiAgentState
from tools.search_tool import search_web


def researcher_node(state: MultiAgentState) -> dict[str, object]:
    model = get_chat_model()

    user_task = ""
    for message in state["messages"]:
        if isinstance(message, HumanMessage):
            user_task = str(message.content)
            break

    tool_context = search_web.invoke(user_task or "general research")
    prompt = [
        SystemMessage(content="You are the researcher worker. Produce concise factual notes."),
        HumanMessage(
            content=(
                "Task:\n"
                f"{user_task}\n\n"
                "Search context:\n"
                f"{tool_context}\n\n"
                "Write 5-8 bullet style notes the writer can use."
            )
        ),
    ]

    response = model.invoke(prompt)
    notes = str(response.content)

    return {
        "research_notes": notes,
        "next": "writer",
        "messages": [AIMessage(content=f"[Researcher Notes]\n{notes}")],
    }