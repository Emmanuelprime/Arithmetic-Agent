# Arithmetic Agent

Arithmetic Agent is an interactive assistant that uses a Google Gemini model and
a local Model Context Protocol (MCP) server to perform arithmetic. The agent
routes calculations through the server's `add`, `subtract`, `multiply`, and
`divide` tools rather than doing the arithmetic itself.

## Requirements

- Python 3.10 or later
- A Google Gemini API key
- Python packages: `python-dotenv`, `langchain`, `langchain-google-genai`,
  `langgraph`, `fastmcp`, and `typing-extensions`

The project does not currently include a dependency lockfile or pinned package
versions.

## Setup

From the project directory, install the dependencies:

```bash
python3 -m pip install python-dotenv langchain langchain-google-genai langgraph fastmcp typing-extensions
```

Create a `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your-google-gemini-api-key
MODEL_NAME=your-supported-gemini-model
```

Keep the API key private. The `.env` file is excluded from Git.

## Run

Start the MCP calculator server in one terminal:

```bash
python3 server/server.py
```

The server uses Streamable HTTP on port `8085`, with the MCP endpoint at
`http://localhost:8085/mcp`.

In a second terminal, start the interactive agent:

```bash
python3 agent/agent.py
```

Enter an arithmetic question at the `You:` prompt. Type `quit`, `exit`, or `q`
to stop the agent. Both processes must be running while you use the agent.

## Project layout

```text
agent/agent.py       Interactive LangGraph agent and MCP client
server/server.py     FastMCP server with arithmetic tools
```
