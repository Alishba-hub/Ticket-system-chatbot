from typing_extensions import TypedDict
from State_of_node import State
from langsmith import traceable
from llm_config import llm

@traceable
def classify_ticket(state:State)->str:

    prompt = f"""
        You are a support ticket classifier. Categorize the incoming ticket on basis of its subject and description into one of the following:
        - billing
        - technical
        - security
        - general

        Return Onlyyyy the category name and write only category nothing else no extra words.

        Subject: {state['subject']}
        Description: {state['description']}
        """

    response = llm.invoke(prompt)
    category = response.content.strip().lower()

    return {
        **state,
        "category": category
    }

