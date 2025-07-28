from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from State_of_node import State
import os



embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def retrieve_context(state: State) -> State:
    category = state.get("category")
    query = f"{state.get('subject', '')}\n{state.get('description', '')}"
    path = f"vectorstores/{category}"

    if not os.path.exists(path):
        return {
            **state,
            "context": "No knowledge base found for this category."
        }

    vectorstore = FAISS.load_local(
        folder_path=path,
        embeddings=embedding,
        allow_dangerous_deserialization=True  
    )
    #seaching for 3 relevant chunks
    try:
        docs = vectorstore.similarity_search(query, k=3)
        context = "\n---\n".join([doc.page_content for doc in docs])
    except Exception as e:
        context = f"Error during context retrieval: {e}"

    return {
        **state,
        "context": context
    }

