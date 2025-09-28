# RAG System for EY Data

This repository contains a **Retrieval-Augmented Generation (RAG) system** designed to answer questions about EY employees, roles, and company information. It combines **dense embeddings**, **sparse retrieval**, and a **Telegram bot interface** for interactive querying.

---

## Features

- **Corpus Construction**
  - Combines multiple data sources including:
    - Excel sheets with employee roles
    - PDF resumes and company documents
    - TXT files with general information
  - Data is consolidated into a single text file (`data.txt`) with section headers to improve retrieval accuracy.

- **Chunking and Metadata**
  - Text is split into chunks using a `RecursiveCharacterTextSplitter`.
  - Each chunk is annotated with metadata (`section`, `file`, `page`) for fine-grained retrieval.

- **Embeddings & Vector Store**
  - Dense embeddings are generated using `all-MiniLM-L6-v2` via `HuggingFaceEmbeddings`.
  - Chunks are stored in a **Chroma vector database** for efficient similarity search.

- **Hybrid Retrieval**
  - Combines **dense semantic search** with **sparse keyword-based retrieval** (BM25) for better recall.
  - Results from both retrievers are merged to produce high-quality context for the model.

- **LLM Integration**
  - Uses Google’s **Gemini-2.5** LLM to generate responses based on the retrieved context.
  - System prompt is tailored for EY-related questions, instructing the model to answer only from the provided context.

- **Telegram Bot Interface**
  - Users can interact with the RAG system via a Telegram bot.
  - Supports natural questions about employees, roles, and company policies.
  - Retrieves relevant chunks and answers in a conversational manner.

---

## How It Works

1. **Corpus Preparation:** Extract text from Excel, PDFs, and TXT files → combine into `data.txt` with clear headers.  
2. **Text Splitting:** Split the corpus into chunks of 1000–1500 tokens with some overlap. Each chunk is assigned metadata.  
3. **Embedding & Storage:** Generate embeddings and store chunks in Chroma.  
4. **Query Handling:**  
   - On a question, retrieve relevant chunks using **hybrid retrieval**.  
   - Feed chunks into the LLM with a system prompt to produce grounded answers.  
5. **Interactive Mode:** Users can send questions through the Telegram bot and receive context-aware responses.

<img width="529" height="1026" alt="image" src="https://github.com/user-attachments/assets/eb655a5a-c65c-4c94-896e-aef2957c6405" />

### Project Structure
.
├── agregate.txt            # Builds data corpus by extracting text from files in Data/
├── data.txt                # Consolidated text corpus
├── database.py             # Builds a Chroma Vector DB
├── Data/                   # Original data files (Excel, PDFs, TXT)
├── query.py                # Query processing and RAG
├── telegram_bot.py         # Telegram bot interface
├── README.md

### Technologies Used

- Python 3.10+
- LangChain: Text splitting, memory, retrieval pipelines
- ChromaDB: Vector database for storing embeddings
- HuggingFace: Embedding generation (all-MiniLM-L6-v2)
- Google Gemini LLM: Generative responses
- BM25: Sparse retrieval for hybrid search
- Telegram API: Interactive chat interface
