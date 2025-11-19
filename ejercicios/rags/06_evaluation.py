import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from datasets import Dataset

# Configuración
MODEL_NAME = "llama3.2:3b"
EMBEDDING_MODEL = "nomic-embed-text"
PERSIST_DIRECTORY = "./chroma_db"

def main():
    print(f"--- Ejemplo 06: Evaluación RAG con RAGAS ---")
    
    if not os.path.exists(PERSIST_DIRECTORY):
        print("Error: Ejecuta primero el ejemplo 02 para crear la base de datos.")
        return

    # 1. Configurar Componentes RAG
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY, 
        embedding_function=embeddings,
        collection_name="course_knowledge"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    llm = ChatOllama(model=MODEL_NAME)

    # 2. Dataset de Evaluación (Ground Truth)
    # Definimos preguntas y las respuestas que ESPERAMOS (ground_truth)
    # En un caso real, esto lo harían humanos expertos.
    eval_data = {
        "question": [
            "¿Qué es LangChain?",
            "¿Para qué sirve CrewAI?",
        ],
        "ground_truth": [
            "LangChain es un framework para desarrollar aplicaciones impulsadas por modelos de lenguaje.",
            "CrewAI es una herramienta para orquestar agentes autónomos y automatizar tareas complejas.",
        ],
        "answer": [], # Aquí guardaremos las respuestas generadas
        "contexts": [] # Aquí guardaremos los contextos recuperados
    }

    # 3. Generar Respuestas y Contextos con nuestro RAG
    print("Generando respuestas para el dataset de evaluación...")
    
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.output_parsers import StrOutputParser

    template = """Responde a la pregunta basándote en el contexto:
    {context}
    Pregunta: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()} 
        | RunnablePassthrough.assign(formatted_context=lambda x: format_docs(x["context"]))
        | RunnablePassthrough.assign(answer=lambda x: prompt | llm | StrOutputParser())
    )

    for q in eval_data["question"]:
        # Ejecutamos la cadena y capturamos contexto y respuesta
        result = rag_chain.invoke(q)
        
        # Guardamos la respuesta generada
        # Nota: result['answer'] es un Runnable, necesitamos invocarlo o ajustar la cadena
        # Ajuste: La cadena arriba devuelve un dict con 'context', 'formatted_context' y 'answer' (que es un string ya parseado)
        # Espera, mi cadena arriba tiene un pequeño bug en la definición lambda.
        # Vamos a simplificar el loop para ser explícitos.
        
        docs = retriever.invoke(q)
        context_text = format_docs(docs)
        
        # Generar respuesta
        msg = prompt.invoke({"context": context_text, "question": q})
        ans = llm.invoke(msg).content
        
        eval_data["answer"].append(ans)
        eval_data["contexts"].append([doc.page_content for doc in docs])

    # 4. Convertir a Dataset de HuggingFace
    dataset = Dataset.from_dict(eval_data)

    # 5. Ejecutar Evaluación con RAGAS
    # RAGAS usa OpenAI por defecto para evaluar. Para usar Ollama como juez, 
    # necesitamos configurarlo explícitamente.
    
    # Configuración de LLM/Embeddings para RAGAS
    # Nota: RAGAS puede ser complejo de configurar con modelos locales pequeños 
    # porque requiere que el modelo juez devuelva JSON estructurado fiable.
    # Llama 3.2 puede tener dificultades.
    
    print("Iniciando evaluación (esto puede tardar)...")
    try:
        # Importamos las clases wrapper de RAGAS para LangChain
        from ragas.llms import LangchainLLMWrapper
        from ragas.embeddings import LangchainEmbeddingsWrapper
        
        evaluator_llm = LangchainLLMWrapper(llm)
        evaluator_embeddings = LangchainEmbeddingsWrapper(embeddings)

        results = evaluate(
            dataset=dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
            ],
            llm=evaluator_llm,
            embeddings=evaluator_embeddings,
        )

        print("\n--- Resultados de la Evaluación ---")
        print(results)
        
        # Exportar a Pandas para ver mejor
        df = results.to_pandas()
        print(df.head())
        
    except Exception as e:
        print(f"Error en evaluación RAGAS: {e}")
        print("Nota: RAGAS requiere modelos robustos para actuar como jueces.")

if __name__ == "__main__":
    main()
