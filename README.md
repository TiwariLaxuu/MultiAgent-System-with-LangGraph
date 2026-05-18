# MultiAgent-System-with-LangGraph

What you'll build ..............

Give me the last 10 days of Apple stock prices? 

                    |-------->>>Call if required (python, csv, api)
user --> Agent ------
                    |<<<--------Tool output


# LangGraph 
LangGraph is a part of the Langchain ecosystem, specifically designing for building and orchestratiing production-ready agents. These agents are constructed as a nodes and edges and this approach provides  high-degree of control and customizability over the workflow. 

# Limitation of LLMs 
1. Knowledge cutoff based on training data
2. Trained to generate specific modalities (text, images, etc). it cannot interate with the outside world, an LLM on its own is not an agent.
        # LLM != AGENT
3. Agents = LLM + TOOLS

Tools can interact with the real-world, such as pulling real-time data from databases, APIs, documents, or search engines, triggering events in third party applications like Google Calender, or running code to perform calculation or analyze data. The capabilities of tools are really only bounded by what can be programmed into a function. 

# Orchestration Layer : 
Orchestration Layer maps out how these interactions take place, and handle things like memory. Using LangGraph for the Orchestration 

# Nodes and Edges 
Nodes indicate a component in the workflow, and edges represent paths in which messages can be exchanged. A node is built for the LLM, and another for the tools it has access to. Edges are added to define where information should travel and depending on what conditions! 
