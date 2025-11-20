import gradio as gr
import chromadb
import os
import json
import numpy as np
import re
from sklearn.metrics.pairwise import cosine_similarity

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chroma_db_constitucion")

# Initialize ChromaDB
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection("constitucion_espanola")

def calculate_mmr(query_embedding, doc_embeddings, doc_ids, k, lambda_mult):
    """
    Maximal Marginal Relevance (MMR) implementation.
    """
    if isinstance(query_embedding, list):
        query_embedding = np.array(query_embedding)
    if isinstance(doc_embeddings, list):
        doc_embeddings = np.array(doc_embeddings)
        
    # Ensure 2D arrays
    if query_embedding.ndim == 1:
        query_embedding = query_embedding.reshape(1, -1)
        
    # Calculate similarities between query and all docs
    # Assuming embeddings are normalized, cosine similarity is dot product
    # But let's use sklearn to be safe
    sims_to_query = cosine_similarity(query_embedding, doc_embeddings)[0]
    
    selected_indices = []
    candidate_indices = list(range(len(doc_ids)))
    
    for _ in range(min(k, len(doc_ids))):
        best_mmr = -float('inf')
        best_idx = -1
        
        for idx in candidate_indices:
            # Similarity to query
            sim_query = sims_to_query[idx]
            
            # Max similarity to already selected docs
            if not selected_indices:
                max_sim_selected = 0
            else:
                selected_embeddings = doc_embeddings[selected_indices]
                current_embedding = doc_embeddings[idx].reshape(1, -1)
                sims_selected = cosine_similarity(current_embedding, selected_embeddings)[0]
                max_sim_selected = np.max(sims_selected)
                
            # MMR score
            mmr_score = (lambda_mult * sim_query) - ((1 - lambda_mult) * max_sim_selected)
            
            if mmr_score > best_mmr:
                best_mmr = mmr_score
                best_idx = idx
        
        if best_idx != -1:
            selected_indices.append(best_idx)
            candidate_indices.remove(best_idx)
            
    return selected_indices

def search_function(query, k, fetch_k, lambda_mult, where_str, score_threshold):
    try:
        # Parse 'where' filter
        where_filter = None
        if where_str and where_str.strip():
            try:
                where_filter = json.loads(where_str)
            except json.JSONDecodeError:
                return f"Error: Invalid JSON in 'where' filter. Example: {{\"tipo\": \"TÍTULO\"}}"

        # Auto-detect Article intent if no explicit filter
        detected_filter_msg = ""
        if not where_filter:
            # Regex to find "articulo X" or "artículo X"
            match = re.search(r'\bart[íi]culo\s+(\d+)\b', query, re.IGNORECASE)
            if match:
                art_num = match.group(1)
                # Construct the expected metadata value, e.g., "Artículo 14"
                where_filter = {"articulo": f"Artículo {art_num}"}
                detected_filter_msg = f"ℹ️ Filtro automático aplicado: {json.dumps(where_filter, ensure_ascii=False)}\n\n"

        # 1. Get embeddings for the query

        # 1. Get embeddings for the query
        # We can use the collection's embedding function implicitly by querying
        # But to do MMR properly we need the query embedding. 
        # A trick is to query for 1 result and ask for the embedding? No.
        # We rely on collection.query to generate embeddings for the documents.
        # But we need the query embedding.
        # Let's use the internal embedding function of the collection if possible.
        
        embedding_function = collection._embedding_function
        if embedding_function:
            query_embeddings = embedding_function([query])
        else:
            # Fallback if no embedding function is set (shouldn't happen with default)
            return "Error: No embedding function found in collection."

        # 2. Initial Fetch (fetch_k)
        # We need embeddings to calculate MMR
        results = collection.query(
            query_texts=[query],
            n_results=int(fetch_k),
            where=where_filter,
            include=['documents', 'metadatas', 'distances', 'embeddings']
        )
        
        if not results['ids'] or not results['ids'][0]:
            return "No results found."

        # Extract data from the first (and only) query
        ids = results['ids'][0]
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]
        embeddings = results['embeddings'][0]
        
        # 3. Filter by Score Threshold (Distance)
        # Chroma returns L2 distance by default. Lower is better.
        # User asked for "score_threshold" (usually similarity, higher is better).
        # Let's assume user inputs a distance threshold for now or convert.
        # If we treat it as similarity (0 to 1), we need to convert L2.
        # For now, let's just filter if distance > threshold (if threshold is distance)
        # OR if similarity < threshold.
        # Let's assume the user means "Similarity Threshold" (0.0 to 1.0).
        # L2 distance for normalized vectors ranges from 0 to 4 (usually 0 to 2).
        # Cosine Similarity = 1 - L2^2 / 2 (approx).
        # Let's use the distances returned.
        
        # Let's just return the raw results first and filter later if needed.
        # But for MMR we need to select indices.
        
        # 4. Apply MMR or Standard Selection
        if lambda_mult >= 1.0:
            # Pure relevance (just take top k from the sorted results)
            # Chroma results are already sorted by distance (relevance)
            selected_indices = list(range(min(int(k), len(ids))))
        else:
            # Apply MMR
            selected_indices = calculate_mmr(
                query_embeddings[0], 
                embeddings, 
                ids, 
                k=int(k), 
                lambda_mult=lambda_mult
            )

        # 5. Format Output
        output_text = []
        if detected_filter_msg:
            output_text.append(detected_filter_msg)

        for idx in selected_indices:
            dist = distances[idx]
            # Simple similarity conversion for display
            similarity = 1.0 / (1.0 + dist) 
            
            # Check threshold
            if similarity < score_threshold:
                continue
                
            doc = documents[idx]
            meta = metadatas[idx]
            
            output_text.append(f"--- Resultado (Sim: {similarity:.4f}, Dist: {dist:.4f}) ---")
            output_text.append(f"ID: {ids[idx]}")
            output_text.append(f"Contenido: {doc}")
            output_text.append(f"Metadatos: {json.dumps(meta, indent=2, ensure_ascii=False)}")
            output_text.append("\n")
            
        if not output_text:
            return "No results met the criteria (check score threshold)."
            
        return "\n".join(output_text)

    except Exception as e:
        return f"Error during search: {str(e)}"

# Gradio Interface
with gr.Blocks(title="Buscador Constitución Española (ChromaDB)") as demo:
    gr.Markdown("# Buscador Semántico - Constitución Española")
    gr.Markdown("Base de datos vectorial: ChromaDB")
    
    with gr.Row():
        with gr.Column(scale=1):
            query_input = gr.Textbox(label="Consulta", placeholder="Escribe tu pregunta aquí...", lines=2)
            
            with gr.Accordion("Parámetros de Búsqueda", open=True):
                k_slider = gr.Slider(minimum=1, maximum=20, value=4, step=1, label="k (Resultados finales)")
                fetch_k_slider = gr.Slider(minimum=1, maximum=50, value=10, step=1, label="fetch_k (Candidatos iniciales)")
                lambda_slider = gr.Slider(minimum=0.0, maximum=1.0, value=0.5, step=0.1, label="lambda_mult (0=Diversidad, 1=Relevancia)")
                threshold_slider = gr.Slider(minimum=0.0, maximum=1.0, value=0.0, step=0.05, label="Score Threshold (Min Similitud)")
                where_input = gr.Textbox(label="Filtro Metadata (JSON)", placeholder='{"tipo_seccion": "TÍTULO"}', value="")
            
            search_btn = gr.Button("Buscar", variant="primary")
            
        with gr.Column(scale=2):
            results_output = gr.Textbox(label="Resultados", lines=20, show_copy_button=True)

    search_btn.click(
        fn=search_function,
        inputs=[query_input, k_slider, fetch_k_slider, lambda_slider, where_input, threshold_slider],
        outputs=results_output
    )

if __name__ == "__main__":
    demo.launch()
