from typing import Annotated
from typing_extensions import TypedDict

import wikipedia
import yfinance as yf
import pandas as pd

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_experimental.utilities import PythonREPL

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


# =====================================================
# STATE
# =====================================================

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# =====================================================
# TOOL 1 : WIKIPEDIA
# =====================================================

@tool
def wikipedia_tool(query: str) -> str:
    """
    Search Wikipedia and return a summary.
    """

    try:
        results = wikipedia.search(query)

        if not results:
            return "No results found."

        title = results[0]

        summary = wikipedia.summary(
            title,
            sentences=5,
            auto_suggest=False,
            redirect=True
        )

        return summary

    except Exception as e:
        return f"Error: {str(e)}"


# =====================================================
# TOOL 2 : STOCK DATA (YFINANCE)
# =====================================================

@tool
def stock_data_tool(
    ticker: str,
    period: str = "6mo"
) -> str:
    """
    Download stock data using yfinance.

    Examples:
        ticker="AAPL"
        period="1mo", "3mo", "6mo", "1y", "2y"
    """

    try:
        stock = yf.Ticker(ticker)

        df = stock.history(period=period)

        if df.empty:
            return f"No stock data found for {ticker}"

        return (
            f"Stock Data for {ticker}\n\n"
            f"{df.tail(20).to_markdown()}"
        )

    except Exception as e:
        return f"Error retrieving stock data: {str(e)}"


# =====================================================
# TOOL 3 : PYTHON EXECUTOR
# =====================================================

repl = PythonREPL()

@tool
def python_repl_tool(code: str) -> str:
    """
    Execute Python code.
    """

    try:
        result = repl.run(code)

        return f"""
Execution Successful

Code:
{code}

Output:
{result}
"""

    except Exception as e:
        return f"Execution failed: {str(e)}"


# =====================================================
# TOOLS
# =====================================================

TOOLS = [
    wikipedia_tool,
    stock_data_tool,
    python_repl_tool
]


# =====================================================
# LLM NODE
# =====================================================

def create_llm():

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    return llm.bind_tools(TOOLS)


def assistant_node(state: AgentState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# =====================================================
# BUILD GRAPH
# =====================================================

def build_graph():

    builder = StateGraph(AgentState)

    builder.add_node(
        "assistant",
        assistant_node
    )

    builder.add_node(
        "tools",
        ToolNode(TOOLS)
    )

    builder.add_edge(
        START,
        "assistant"
    )

    builder.add_conditional_edges(
        "assistant",
        tools_condition,
        {
            "tools": "tools",
            END: END
        }
    )

    builder.add_edge(
        "tools",
        "assistant"
    )

    return builder.compile()


# =====================================================
# MAIN
# =====================================================

def main():

    graph = build_graph()

    query = input("Ask something: ")

    result = graph.invoke(
        {
            "messages": [
                ("user", query)
            ]
        }
    )

    print("\n" + "=" * 80)

    for msg in result["messages"]:
        if hasattr(msg, "content"):
            print(msg.content)
            print()


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":

    llm_with_tools = create_llm()

    main()