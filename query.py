from langchain_chroma import Chroma
from api import api_key
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings

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
                EY sobre assuntos relacionados com a empresa, outros trabalhadores, \
                algumas notícias e funcionamento/políticas da empresa. Usa o contexto \
                retornado abaixo para responder às perguntas. Se não souberes responder diz apenas: \"Não sei responder.\": \
                {context}",
            ),
            ("human", "{question}"),
        ]
    )

    retrieved_docs = vector_store.similarity_search(query, k=4)
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