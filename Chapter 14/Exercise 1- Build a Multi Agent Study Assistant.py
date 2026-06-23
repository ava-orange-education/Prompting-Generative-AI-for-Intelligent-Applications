from typing import TypedDict
from langgraph.graph import StateGraph, END

class StudyState(TypedDict):
    topic: str
    notes: str
    weak_areas: str
    practice_tasks: str
    review_feedback: str
    decision: str


def planner_agent(state: StudyState):
    return {
        "notes": f"Create a focused study plan for the topic {state['topic']}"
    }

def analysis_agent(state: StudyState):
    return {
        "weak_areas": f"Identify weak areas in topic {state['topic']} based on study notes"
    }

def execution_agent(state: StudyState):
    return {
        "practice_tasks": f"Generate practice tasks for weak areas: {state['weak_areas']}"
    }

def analysis_agent(state: StudyState):
    if state["review_feedback"]:
        return {
            "weak_areas": f"All weak areas in {state['topic']} have been addressed"
        }

    return {
        "weak_areas": f"No remaining gaps in {state['topic']}"
    }

def review_agent(state: StudyState):
    feedback = "Some gaps still remain"
    decision = "LOOP" if "weak" in state["weak_areas"].lower() else "STOP"
    return {
        "review_feedback": feedback,
        "decision": decision
    }

def decide_next_step(state: StudyState):
    if state["decision"] == "STOP":
        return END
    return "analysis"

graph = StateGraph(StudyState)
graph.add_node("planner", planner_agent)
graph.add_node("analysis", analysis_agent)
graph.add_node("execute", execution_agent)
graph.add_node("review", review_agent)

graph.set_entry_point("planner")
graph.add_edge("planner", "analysis")
graph.add_edge("analysis", "execute")
graph.add_edge("execute", "review")
graph.add_conditional_edges(
    "review",
    decide_next_step
)
app = graph.compile()

initial_state: StudyState = {
    "topic": "Operating Systems",
    "notes": "",
    "weak_areas": "",
    "practice_tasks": "",
    "review_feedback": "",
    "decision": "LOOP"
}

final_state = app.invoke(initial_state)
print(final_state)
