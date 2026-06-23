from typing import TypedDict
from langgraph.graph import StateGraph, END


class DocumentState(TypedDict):
    document_text: str
    summary: str
    issues: str
    recommendations: str
    decision: str


def reader_agent(state: DocumentState):
    return {
        "summary": "Summarise the document and capture the main intent"
    }


def analysis_agent(state: DocumentState):
    if state["decision"] == "REVISE":
        return {
            "issues": "All major concerns have been addressed"
        }

    return {
        "issues": "Several risks and unclear sections exist in the document"
    }


def execution_agent(state: DocumentState):
    return {
        "recommendations": f"Suggest actions based on issues: {state['issues']}"
    }


def review_agent(state: DocumentState):
    decision = "REVISE" if "risk" in state["issues"].lower() else "APPROVE"
    return {
        "decision": decision
    }


def decide_next_step(state: DocumentState):
    if state["decision"] == "APPROVE":
        return END
    return "analysis"


graph = StateGraph(DocumentState)

graph.add_node("reader", reader_agent)
graph.add_node("analysis", analysis_agent)
graph.add_node("execute", execution_agent)
graph.add_node("review", review_agent)

graph.set_entry_point("reader")
graph.add_edge("reader", "analysis")
graph.add_edge("analysis", "execute")
graph.add_edge("execute", "review")

graph.add_conditional_edges(
    "review",
    decide_next_step
)

app = graph.compile()

initial_state: DocumentState = {
    "document_text": "Policy document text goes here",
    "summary": "",
    "issues": "",
    "recommendations": "",
    "decision": ""
}

final_state = app.invoke(initial_state)
print(final_state)
