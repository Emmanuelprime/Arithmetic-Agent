import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain.mcp import MCPAdapter
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated, Sequence
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from typing_extensions import TypedDict
import logging
logging.getLogger("langchain_google_genai").setLevel(logging.ERROR)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL_NAME")

SYSTEM_PROMPT = """You are a precise arithmetic assistant called Sinelo.
Use the available tools (add, subtract, multiply, divide) to compute every result.
Never do arithmetic in your head; always call the appropriate tool.
If the user asks for multiple operations, chain the tool calls in order.
Keep answers short: state the expression and the computed result."""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

config = {
    "mcpServers": {
        "calculator": {
            "url": "http://localhost:8085/mcp"
        },
        # "ddg-search": {
        #     "command": "uvx",
        #     "args": ["duckduckgo-mcp-server"]
        # }
    }
}

async def main():
    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools()
        print(f"Loaded {len(tools)} tools: {[t.name for t in tools]}")

        llm = ChatGoogleGenerativeAI(model=MODEL, api_key=API_KEY)
        llm_with_tools = llm.bind_tools(tools)

        def agent_node(state: AgentState):
            return {"messages": [llm_with_tools.invoke(state["messages"])]}

        graph = StateGraph(AgentState)
        graph.add_node("agent", agent_node)
        graph.add_node("tools", ToolNode(tools))
        graph.add_edge(START, "agent")
        graph.add_conditional_edges("agent", tools_condition)
        graph.add_edge("tools", "agent")
        graph = graph.compile()

        history = [SystemMessage(content=SYSTEM_PROMPT)]

        print("Interactive arithmetic agent. Type 'quit' or 'exit' to leave.\n")
        while True:
            user_input = await asyncio.to_thread(input, "You: ")
            user_input = user_input.strip()

            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("Bye.")
                break

            history.append(HumanMessage(content=user_input))
            result = await graph.ainvoke({"messages": history})

            history = result["messages"]

            final = history[-1]
            if isinstance(final.content, list):
                text = "".join(
                    block.get("text", "") for block in final.content
                    if isinstance(block, dict) and block.get("type") == "text"
                )
            else:
                text = final.content
            print(f"Agent: {text}\n")

if __name__ == "__main__":
    asyncio.run(main())