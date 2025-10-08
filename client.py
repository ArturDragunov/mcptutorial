from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
# **Before running the code, make sure that you host the tool servers.**


# The MCP client automatically discovers all @mcp.tool() decorated functions in calculator.py and their signatures
#  (parameters, types, docstrings). The LLM gets the full tool schema without you manually listing each tool.
# MCP handles the discovery and introspection automatically.
async def main():
    """_summary_
    """
    # This code is setting up a MultiServerMCPClient that can talk to multiple MCP servers simultaneously
    # Summary: You're setting up one client that can use tools from both servers:
    #  - math operations from the calculator (via subprocess)
    #  - weather data from the weather server (via HTTP).
    client = MultiServerMCPClient(
         # we are writing configuration for the servers
        {
            "calculator":{ # Name/key for this server (python file)
                "command":"python", # Run the calculator server by executing Python
                 "args":["calculator.py"], # Pass calculator.py as argument to Python
                  "transport":"stdio" # Use stdio (standard input/output) for communication
                 
                },
            
            
            "weather": { # Name/key for this server
                "url": "http://localhost:8000/mcp", # Connect to a server already running at this URL
                "transport": "streamable_http" # Use HTTP for communication
                # use stdio for local development and for internet use http
                
            }
            
        }
        
    )
    tools = await client.get_tools() # initialize tools from the servers
    
    model = ChatGroq(model="deepseek-r1-distill-llama-70b")
    
    agent = create_react_agent(model, tools)
    
        # ainvoke -> async invoke. We need await because it's an async function.
        # Without await, you’d just get a coroutine object and the code wouldn’t actually execute.
        # So this line means:
        # “Run agent.ainvoke() asynchronously, and wait until it finishes.
        # When it does, store the result in response.”
    response = await agent.ainvoke( 
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    
    print(response) # we take last message from the state



asyncio.run(main())