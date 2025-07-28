import csv
from typing import TypedDict
import os
from langsmith import traceable
from typing import TypedDict, Optional, List, Dict

class State(TypedDict):
    subject: str
    description: str
    category: str
    context: str
    draft: str
    review_feedback: str
    status_of_feedback: str
    final_response: str
    no_of_try: int
    

#writing in file
def log_escalation(state: State):
    file_path = "escalation_log.csv"
    file_exists = os.path.exists(file_path)

    def clean(text):
        return text.strip().replace("\r", "")

    with open(file_path, mode="a", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)

        
        if not file_exists:
            writer.writerow(["--- Escalation Log Start ---"])

        
        writer.writerow(["Subject:", clean(state["subject"])])
        writer.writerow(["Description:", clean(state["description"])])
        writer.writerow(["Category:", clean(state["category"])])
        writer.writerow(["Failed Draft:", clean(state["draft"])])
        writer.writerow(["Review Feedback:", clean(state["review_feedback"])])
        
        
        writer.writerow([])



