# Support Ticket Resolution Agent

AI-powered support system with LangGraph that classifies tickets, retrieves context, generates responses, and includes quality review with retry logic.

To watch running tutorial download langgraph_chatbot.mp4 from given repository

## Technologies Used

**Core Framework:**
- **LangGraph**: Workflow orchestration with state management and conditional routing
- **LangChain**: Document processing, text splitting, and LLM integrations
- **Google Gemini 2.0 Flash**: Primary LLM for classification, generation, and review

**RAG & Embeddings:**
- **FAISS**: Vector database for similarity search and document retrieval
- **HuggingFace Transformers**: sentence-transformers/all-MiniLM-L6-v2 for embeddings
- **Category-specific vector stores**: Isolated knowledge bases per support category

**Observability & Memory:**
- **LangSmith**: Distributed tracing for all LLM calls and workflow steps
- **MemorySaver**: LangGraph checkpointing for conversation persistence
- **Thread-based memory**: Maintains context across follow-up interactions

**Web Framework:**
- **Flask**: REST API backend with CORS support
- **Frontend**: HTML/CSS/JavaScript interface for ticket submission

**Data Processing:**
- **CSV logging**: Escalation tracking for human review
- **Text processing**: CharacterTextSplitter for document chunking

## Architecture

```
Ticket → Classify → Retrieve → Draft → Review → Response/Retry/Escalate
```

**Components:**
- **Classifier**: Categorizes into billing/technical/security/general
- **RAG**: FAISS vector stores per category with HuggingFace embeddings
- **Generator**: Creates responses using LLM + context
- **Reviewer**: QA check with 80% approval rate
- **Retry**: Max 2 attempts with refined context
- **Escalation**: Failed cases logged to CSV

## Quick Setup

1. **Install dependencies**
   ```bash
   pip install langchain-community langchain-huggingface langgraph faiss-cpu flask flask-cors google-generativeai python-dotenv
   ```

2. **Environment setup**
   ```bash
   # .env file
   GOOGLE_API_KEY=your_gemini_api_key
   LANGSMITH_TRACING="true"
   LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
   LANGSMITH_API_KEY="your_key"
   LANGSMITH_PROJECT="project name"
   ```

3. **Create knowledge base**
   ```
   knowledgefiles/
   ├── billing.txt
   ├── technical.txt  
   ├── security.txt
   └── general.txt
   ```

4. **Run vector store setup** (embedded in code)
   ```bash
   python vectorstore.py
   ```

6. **Start application and Watch tutorial**
   ```bash
   python backend.py
   # Access: http://localhost:5000
   ```

   
   To watch running tutorial download langgraph_chatbot.mp4 from given repository
   and for detailed tutorial use drive link:
   https://drive.google.com/file/d/1NRUON-VyhGVkHkWzrenon5suZPAQ0WOx/view?usp=drive_link

## Workflow & Tracing

**LangSmith Integration:**
All critical functions decorated with `@traceable` for complete observability:
- Classification decisions and confidence scores
- Context retrieval results and similarity scores  
- Draft generation with prompt templates
- Review outcomes with detailed feedback
- Retry attempts and refinement strategies

**Memory Management:**
- **MemorySaver**: Persistent checkpointing across workflow steps
- **Thread-based sessions**: Each conversation maintains independent state
- **State persistence**: Full conversation history available for follow-ups
- **Graceful recovery**: System resumes from last checkpoint on failures

**Workflow Paths:**

1. **Happy Path**: Ticket → Classify → Context → Draft → Approve → Response
2. **Retry Path**: Draft → Reject → Refine Context → New Draft → Review (max 2x)
3. **Escalation**: After 2 failures → Log to `escalation_log.csv`

## Configuration

- **LLM**: Google Gemini 2.0 Flash
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Chunks**: 300 chars, 20 overlap
- **Retrieval**: Top 3 similar docs
- **Review**: ~80% approval rate

## Key Files

```
├── backend.py                 # Flask API & frontend
├── graph_const.py         # LangGraph workflow
├── classifier_node.py     # Ticket classification
├── retrieve_context.py    # RAG implementation
├── generate_draft.py      # Response generation
├── review_draft.py        # Quality review
├── State_of_node.py       # State management & logging
└── llm_config.py          # LLM configuration
```

## Features

- Multi-category classification with confidence scoring
- RAG with category-specific knowledge bases  
- Automated quality review with policy compliance
- Intelligent retry with targeted feedback refinement
- Human escalation logging with detailed context
- Web interface with REST API endpoints
- Complete LangSmith tracing and observability
- Persistent memory across conversation threads
- Graceful error handling and recovery mechanisms

## Error Handling

- Missing vector stores → Error context
- LLM failures → Graceful degradation  
- Invalid input → Validation & sanitization
- Review loops → Max attempt limits
