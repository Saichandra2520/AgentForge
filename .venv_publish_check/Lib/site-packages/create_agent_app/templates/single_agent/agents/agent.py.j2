"""LangGraph single-agent workflow with tool-calling."""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from config import get_chat_model
from memory.state import AgentState
from tools.sample_tool import calculator

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Use tools when they improve correctness, "
    "especially for arithmetic. Keep answers concise and clear."
)


def _agent_node(state: AgentState) -> dict[str, list[AIMessage]]:
    model = get_chat_model().bind_tools([calculator])
    messages = state["messages"]
    if not messages or messages[0].type != "system":
        messages = [SystemMessage(content=SYSTEM_PROMPT), *messages]
    response = model.invoke(messages)
    return {"messages": [response]}


def _route_after_agent(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return END


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("agent", _agent_node)
    graph.add_node("tools", ToolNode([calculator]))

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", _route_after_agent, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile()


def invoke_agent(query: str) -> str:
    app = build_graph()
    result = app.invoke({"messages": [HumanMessage(content=query)]})

    for message in reversed(result["messages"]):
        if isinstance(message, AIMessage) and message.content:
            return str(message.content)
    return "I could not produce a response."