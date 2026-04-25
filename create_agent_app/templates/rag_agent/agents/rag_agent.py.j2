"""LangGraph RAG agent using retrieval tool-calling."""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from config import get_chat_model
from memory.state import AgentState
from tools.retriever_tool import retrieve_knowledge

SYSTEM_PROMPT = (
    "You are a RAG assistant. Always call retrieve_knowledge for factual questions "
    "before finalizing your answer. Use only retrieved context when possible."
)


def _agent_node(state: AgentState) -> dict[str, list[AIMessage]]:
    model = get_chat_model().bind_tools([retrieve_knowledge])
    messages = state["messages"]
    if not messages or messages[0].type != "system":
        messages = [SystemMessage(content=SYSTEM_PROMPT), *messages]
    response = model.invoke(messages)
    return {"messages": [response]}


def _route_after_agent(state: AgentState) -> str:
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    return END


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("agent", _agent_node)
    graph.add_node("tools", ToolNode([retrieve_knowledge]))

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", _route_after_agent, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile()


def ask_rag_agent(query: str) -> str:
    app = build_graph()
    result = app.invoke({"messages": [HumanMessage(content=query)]})

    for message in reversed(result["messages"]):
        if isinstance(message, AIMessage) and message.content:
            return str(message.content)
    return "No answer generated."