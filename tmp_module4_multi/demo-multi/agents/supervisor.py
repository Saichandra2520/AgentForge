"""Supervisor graph for researcher + writer workflow."""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph

from config import get_chat_model
from memory.state import MultiAgentState
from agents.workers.researcher import researcher_node
from agents.workers.writer import writer_node


def supervisor_node(state: MultiAgentState) -> dict[str, object]:
    model = get_chat_model()

    has_research = bool(state.get("research_notes", "").strip())
    has_final = bool(state.get("final_answer", "").strip())

    user_task = ""
    for message in state["messages"]:
        if isinstance(message, HumanMessage):
            user_task = str(message.content)
            break

    prompt = [
        SystemMessage(
            content=(
                "You are a supervisor orchestrating two workers: researcher and writer. "
                "Respond with exactly one token: researcher, writer, or finish."
            )
        ),
        HumanMessage(
            content=(
                f"Task: {user_task}\n"
                f"Has research notes: {has_research}\n"
                f"Has final answer: {has_final}\n"
                "Choose the next worker."
            )
        ),
    ]

    decision_text = str(model.invoke(prompt).content).strip().lower()

    if "researcher" in decision_text and not has_research:
        nxt = "researcher"
    elif "writer" in decision_text and has_research and not has_final:
        nxt = "writer"
    elif has_final:
        nxt = "finish"
    else:
        nxt = "researcher" if not has_research else "writer"

    return {"next": nxt, "messages": [AIMessage(content=f"[Supervisor] next={nxt}")]}


def _route(state: MultiAgentState) -> str:
    nxt = state.get("next", "finish")
    return nxt if nxt in {"researcher", "writer", "finish"} else "finish"


def build_graph():
    graph = StateGraph(MultiAgentState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges(
        "supervisor",
        _route,
        {
            "researcher": "researcher",
            "writer": "writer",
            "finish": END,
        },
    )
    graph.add_edge("researcher", "supervisor")
    graph.add_edge("writer", "supervisor")

    return graph.compile()


def run_supervisor_workflow(task: str) -> str:
    app = build_graph()
    result = app.invoke(
        {
            "messages": [HumanMessage(content=task)],
            "research_notes": "",
            "final_answer": "",
            "next": "researcher",
        }
    )

    final_answer = str(result.get("final_answer", "")).strip()
    if final_answer:
        return final_answer

    for message in reversed(result["messages"]):
        if isinstance(message, AIMessage) and message.content:
            return str(message.content)
    return "No response generated."