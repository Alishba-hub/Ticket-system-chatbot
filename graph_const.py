from langgraph.graph import StateGraph, END
from State_of_node import State, log_escalation
from classifier_node import classify_ticket
from retrieve_context import retrieve_context
from generate_draft import generate_draft
from review_draft import review_draft
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

def graph_compile(state_dict: State):
    builder = StateGraph(State)

    builder.add_node("classify", classify_ticket)
    builder.add_node("retrieve", retrieve_context)
    builder.add_node("draft", generate_draft)
    builder.add_node("review", review_draft)
    builder.add_node("escalate", log_escalation)

    builder.set_entry_point("classify")
    builder.add_edge("classify", "retrieve")
    builder.add_edge("retrieve", "draft")
    builder.add_edge("draft", "review")

    def route_review(state: State) -> str:
        if state["status_of_feedback"].lower() == "approved":
            return END
        if state["no_of_try"] >= 2:
            return "escalate"
        return "draft"

    builder.add_conditional_edges("review", route_review, {
        "escalate": "escalate",
        "draft": "draft",
        END: END,
    })

    builder.add_edge("review", END)
    builder.add_edge("escalate", END)

    graph = builder.compile(checkpointer=memory)
    return graph,state_dict
    
    
