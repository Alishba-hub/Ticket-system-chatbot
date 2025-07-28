from State_of_node import State
from langsmith import traceable
from llm_config import llm

@traceable
def review_draft(state: State) -> dict:
    prompt = f"""
        You are a senior support QA reviewer. Your job is to assess the following draft response.

        1)
        Subject: {state['subject']}
        Description: {state['description']}

        2)
        {state['context']}
        {state['draft']}

        Instructions:
        most of the times the ans should be approved only 20% percent the and should be as rejected 
        Evaluate whether the response is accurate, helpful, and compliant with support
        guidelines (e.g., don’t overpromise, don’t provide refunds without approval, don’t
        advise on sensitive security issues).

        in start of ans write either "approved" or "rejected" then after space remaining answer
    """

    try:
        result = llm.invoke(prompt).content.strip()

        if result.lower().startswith("approved"):
            return {
                **state,
                "review_feedback": result,
                "status_of_feedback": "approved",
                "final_response": state["draft"]
            }
        else:
            return {
                **state,
                "review_feedback": result,
                "status_of_feedback": "rejected",
                "final_response": state["draft"],
                "no_of_try": state["no_of_try"] + 1
        }

    except Exception as e:
        return {
            **state,
            "review_feedback": f"Error during review: {str(e)}",
            "status_of_feedback": "error",
            "final_response": state.get("draft", ""),
            "no_of_try": state.get("no_of_try", 0)
        }
