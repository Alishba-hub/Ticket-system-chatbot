from State_of_node import State
from langsmith import traceable
from llm_config import llm


@traceable
def generate_draft(state:State)->State:
    prompt = f"""
        You are a customer support agent. Your job is to write a helpful, polite, and policy-compliant response to the user based on:

        1. The support ticket:
        Subject: {state['subject']}
        Description: {state['description']}

        2. The following context retrieved from internal knowledge base:
        {state['context']}

        Instructions:
        - Your answer must be clear and customer-facing.
        - Avoid technical jargon unless necessary.
        - Be concise but thorough.
        -musttttt be accurate,helpful and compliant with support guidelines 
        
        Compose your response below:
        """

    response = llm.invoke(prompt)

    return {
        **state,
        "draft": response.content,
    }

#checkingggg