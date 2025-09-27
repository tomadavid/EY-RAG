from langchain_chroma import Chroma
from api import api_key
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

def process_query(query):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_store = Chroma(collection_name="ey_data",
                        embedding_function=embeddings,
                        persist_directory="./chroma_db")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "És um assistente que reponde a perguntas de trabalhadores da \
                EY sobre assuntos relacionados com a empresa em geral, dados sobre outros trabalhadores como cargos e dados do seu CV, \
                algumas notícias sobre mudanças na empresa e funcionamento/políticas da empresa. \
                Se o utilizador fizer uma nova pergunta sem especificar claramente o que quer, \
                assume que ele está a pedir a mesma informação da pergunta anterior.Usa o contexto \
                retornado abaixo como suporte para fundamentar as tuas rezpostas. Se não souberes responder diz apenas: \"Não sei responder.\": \
                {context}",
            ),
            ("human", "{question}"),
        ]
    )

    dense_retriever = vector_store.as_retriever(kwargs={"k":3})

    data = vector_store.get(include=["documents"])
    docs = [Document(page_content=doc) for doc in data["documents"]]
    bm25_retriever = BM25Retriever.from_documents(docs)
    bm25_retriever.k = 3

    hybrid_retriever = EnsembleRetriever(
        retrievers=[dense_retriever, bm25_retriever],
        weights=[0.5, 0.5]
    )

    retrieved_docs = hybrid_retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    chain = prompt | llm
    message = chain.invoke({"context": context, "question": query})
    return message.content

def main():
    print(process_query(input("Olá, em que posso ajudar?\n")))
    while True:
        print(process_query(input("\nEm que mais posso ajudar?\n")))

if __name__ == "__main__":
    main()
