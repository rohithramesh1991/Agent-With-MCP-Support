import os
import json
import asyncio
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import gradio as gr

load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

# Load MCP servers config
config_file = "configure_mcp.json"
with open(config_file) as f:
    mcp_config = json.load(f)
mcp_servers = ", ".join(mcp_config.get("mcpServers", {}).keys())

# System message
system_message_content = f"""
You are an assistant that helps users interact with Model Context Protocol (MCP) servers.

- Available MCP servers: {mcp_servers}.
- Provide accurate information about the system's servers and capabilities, using the current configuration.
- Keep responses relevant to the configured system.
"""

llm = ChatGroq(
    model="qwen-qwq-32b",
)

client = MCPClient.from_config_file(config_file)
agent = MCPAgent(
    llm=llm,
    client=client,
    max_steps=15,
    memory_enabled=True,
)

def remove_think_tag(response_text: str) -> str:
    cleaned_response = re.sub(r'<think>.*?</think>\n?', '', response_text, flags=re.DOTALL)
    return cleaned_response.strip()

async def gradio_chat(user_input, history):
    print(f"User input: {user_input}")
    print(f"History: {history}")

    # Build the conversation messages for the LLM
    messages = [SystemMessage(content=system_message_content)]
    # Replay previous exchanges
    for msg in history:
        if msg.get("role") == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg.get("role") == "assistant":
            # We treat all non-user messages as assistant/model replies
            messages.append(AIMessage(content=msg["content"]))
    # Add latest user input
    messages.append(HumanMessage(content=user_input))

    print(f"Messages for LLM: {messages}")

    try:
        response_obj = await llm.ainvoke(messages)
        print(f"LLM response_obj: {response_obj}")

        # Extract string response
        if hasattr(response_obj, "content"):
            result = response_obj.content
        else:
            result = str(response_obj)
        
        response = remove_think_tag(result)
        print(f"Response:\n{response}")

        # Gradio expects return value to be a string, which becomes the assistant's reply
        return response
    except Exception as e:
        print(f"Exception during LLM invocation: {e}")
        return f"Error: {e}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>🤖 MCP Chat Assistant</h1>")
    chat = gr.ChatInterface(
        gradio_chat,
        chatbot=gr.Chatbot(height=500, type="messages"),
        theme="soft",
        # type="messages"  # you can leave this commented if gradio is new enough
    )

if __name__ == "__main__":
    demo.queue().launch()
