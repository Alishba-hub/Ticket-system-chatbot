from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import os


embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=20)

base_folder = "knowledgefiles"
category_files={
    'billing': f"{base_folder}/billing.txt",
    'technical':f'{base_folder}/technical.txt',
    'security': f'{base_folder}/security.txt',
    'general':f"{base_folder}/general.txt"

}

os.makedirs("vectorstores", exist_ok=True)

for category,f_path in category_files.items():
    loader=TextLoader(f_path)
    docs=loader.load_and_split(text_splitter)
    vectorstore = FAISS.from_documents(docs, embedding)
    vectorstore.save_local(f"vectorstores/{category}")