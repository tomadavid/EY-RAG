Basic RAG system using chromadb

A corpus data.txt is built by extracting text from multiple data sources.

Chunks of that corpus are stored in a vector database.

On each question, the question is embedded and compared to the vector db embeddings. The returned chunks will be used to respond.
