# Agent-With-MCP-Support

## MCP Chat Assistant
A conversational AI agent that interacts dynamically with Model Context Protocol (MCP) servers. This assistant leverages LangChain Groq for efficient large language model inference accelerated by Groq’s hardware, and uses the mcp-use framework for seamless MCP server integration and conversational memory management.

### Getting Started
Installation
This project uses poetry for dependency management. To install dependencies, run:

```
poetry install
```
If you don’t have Poetry installed, you can get it from [Poetry Download](https://python-poetry.org/docs/#installation).

### Configuration:
- **Place your MCP server configuration in configure_mcp.json.

- **Add your Groq API key to a .env file as GROQ_API_KEY.

### Learn More
For detailed insights and explanations, see the Medium article:
[Chat Agent with MCP Support](https://medium.com/@rohithramesh1991/building-an-intelligent-chat-agent-with-mcp-support-smarter-conversations-1948b96270db)
