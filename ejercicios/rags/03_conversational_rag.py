import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Configuración
MODEL_NAME = "llama3.2:3b"
EMBEDDING_MODEL = "nomic-embed-text"
PERSIST_DIRECTORY = "./chroma_db"

def main():
    print(f"--- Ejemplo 03: RAG Conversacional (Chat con Memoria) ---")
    
    # 1. Cargar Vector Store existente
    if not os.path.exists(PERSIST_DIRECTORY):
        print("Error: Ejecuta primero el ejemplo 02 para crear la base de datos.")
        return

    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY, 
        embedding_function=embeddings,
        collection_name="course_knowledge"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatOllama(model=MODEL_NAME)

    # 2. Crear History Aware Retriever
    # Este componente reescribe la pregunta actual basándose en el historial
    # para que sea una pregunta independiente (standalone question)
    
    contextualize_q_system_prompt = """Given a chat history and the latest user question 
    which might reference context in the chat history, formulate a standalone question 
    which can be understood without the chat history. Do NOT answer the question, 
    just reformulate it if needed and otherwise return it as is."""
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # 3. Crear la cadena de respuesta (QA Chain)
    qa_system_prompt = """You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise.

    {context}"""
    
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    # 4. Cadena Final: Recuperación + Respuesta
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    # 5. Loop de Chat
    chat_history = []
    
    print("\n--- Chat Iniciado. Escribe 'salir' para terminar. ---")
    while True:
        query = input("\nTú: ")
        if query.lower() in ["salir", "exit", "quit"]:
            break
            
        print("Pensando...")
        result = rag_chain.invoke({"input": query, "chat_history": chat_history})
        
        answer = result["answer"]
        print(f"Asistente: {answer}")
        
        # Actualizar historial
        chat_history.append(HumanMessage(content=query))
        chat_history.append(AIMessage(content=answer))

if __name__ == "__main__":
    main()
