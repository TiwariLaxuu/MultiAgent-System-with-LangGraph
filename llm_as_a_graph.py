from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Create the state to capture the messages
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Create the graph state
graph_builder = StateGraph(State)

import os
from langchain_openai import ChatOpenAI

# Define an OpenAI LLM
llm = ChatOpenAI(model = "gpt-4o-mini")

# Takes the state, and appends the new messages to it
def llm_node(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# Create a node called "llm" that calls the llm_node function
graph_builder.add_node('llm', llm_node)

# Connect the "llm" node to the START and END of the graph
graph_builder.add_edge(START, 'llm')
graph_builder.add_edge('llm', END)

# Compile the graph
graph = graph_builder.compile()

from course_helper_functions import pretty_print_messages

for chunk in graph.stream(
    {"messages": [{"role": "user", "content": "Tell me about Apple Inc."}]}
):
    pretty_print_messages(chunk)


'''
Update from node llm:


================================== Ai Message ==================================

Apple Inc. is an American multinational technology company headquartered in Cupertino, California. It was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne. Apple is renowned for its innovative products, software, and services, which have significantly influenced the technology industry and pop culture.

### Key Products and Services:

1. **Hardware**:
   - **iPhone**: Launched in 2007, the iPhone transformed the smartphone market, blending phone, internet, and media capabilities into a single device.
   - **iPad**: Introduced in 2010, the iPad popularized tablet computing.
   - **Mac**: Apple's line of personal computers includes the MacBook Air, MacBook Pro, iMac, and Mac Mini.
   - **Apple Watch**: Launched in 2015, the Apple Watch has become a leader in the smartwatch category.
   - **AirPods**: These wireless earbuds debuted in 2016 and quickly gained popularity for their convenience and integration with other Apple devices.

2. **Software**:
   - **iOS and iPadOS**: Operating systems for the iPhone and iPad, respectively.
   - **macOS**: The operating system for Mac computers.
   - **watchOS**: The operating system for the Apple Watch.
   - **tvOS**: The operating system for the Apple TV.
'''