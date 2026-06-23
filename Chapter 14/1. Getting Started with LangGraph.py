from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    task: str
    notes: str
    analysis: str
    result: str

graph = StateGraph(AgentState)

def analysis_agent(state: AgentState):
    return {
        "analysis": f"Analysing task: {state['task']}"
    }

graph.add_node("analysis", analysis_agent)

def decide_next_step(state: AgentState):
    if "missing" in state["analysis"]:
        return "analysis"
    return "execute"

graph.add_conditional_edges(
    "analysis",
    decide_next_step
)


def execute_agent(state: AgentState):
    return {
        "result": f"Task completed: {state['task']}"
    }

graph.add_node("execute", execute_agent)


graph.set_entry_point("analysis")

app = graph.compile()

initial_state: AgentState = {
    "task": "Summarise cell division",
    "notes": "",
    "analysis": "",
    "result": ""
}

final_state = app.invoke(initial_state)
print(final_state)
