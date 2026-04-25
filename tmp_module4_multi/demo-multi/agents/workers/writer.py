"""Writer worker node."""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from config import get_chat_model
from memory.state import MultiAgentState


def writer_node(state: MultiAgentState) -> dict[str, object]:
    model = get_chat_model()

    user_task = ""
    for message in state["messages"]:
        if isinstance(message, HumanMessage):
            user_task = str(message.content)
            break

    prompt = [
        SystemMessage(content="You are the writer worker. Convert research notes into a polished answer."),
        HumanMessage(
            content=(
                "Task:\n"
                f"{user_task}\n\n"
                "Research notes:\n"
                f"{state.get('research_notes', '')}\n\n"
                "Write a clear final response with a short summary and action points."
            )
        ),
    ]

    response = model.invoke(prompt)
    final_answer = str(response.content)

    return {
        "final_answer": final_answer,
        "next": "finish",
        "messages": [AIMessage(content=f"[Writer Draft]\n{final_answer}")],
    }