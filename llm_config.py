from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from typing_extensions import Annotated  

load_dotenv()

llm=init_chat_model("google_genai:gemini-2.0-flash")

