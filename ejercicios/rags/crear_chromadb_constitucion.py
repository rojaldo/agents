import json
import chromadb
import os
import uuid

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "notebookllm_constitucion.json")
DB_PATH = os.path.join(BASE_DIR, "chroma_db_constitucion")

def main():
    print(f"Reading data from: {DATA_FILE}")
    print(f"Creating ChromaDB at: {DB_PATH}")

    # Initialize ChromaDB
    client = chromadb.PersistentClient(path=DB_PATH)
    
    # Create or get collection
    # Using get_or_create_collection to avoid errors if it exists
    collection = client.get_or_create_collection(name="constitucion_espanola")
    
    # Load JSON
    if not os.path.exists(DATA_FILE):
        print(f"Error: File not found at {DATA_FILE}")
        return

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    root_data = data.get("Constitución Española", {})
    fecha_promulgacion = root_data.get("Fecha_Promulgación", "")
    fuente_boe = root_data.get("Fuente_BOE", "")
    
    partes = root_data.get("partes_estructurales", [])
    
    documents = []
    metadatas = []
    ids = []
    
    count = 0
    
    for parte in partes:
        # Case 1: Content (Preámbulo, Disposiciones)
        if "contenido" in parte:
            contenido = parte["contenido"]
            
            if isinstance(contenido, str):
                # Simple string content
                text = contenido
                meta = {
                    "tipo_seccion": parte.get("nombre", "Desconocido"),
                    "fecha_promulgacion": fecha_promulgacion,
                    "fuente_boe": fuente_boe
                }
                documents.append(text)
                metadatas.append(meta)
                ids.append(f"seccion_{uuid.uuid4().hex[:8]}")
                count += 1
            elif isinstance(contenido, list):
                # List of content items (e.g. Disposiciones)
                tipo_seccion = parte.get("nombre", "Desconocido")
                tipo = parte.get("tipo", "")
                
                for item in contenido:
                    text = item.get("texto", "")
                    if text:
                        meta = {
                            "tipo_seccion": tipo_seccion,
                            "tipo": tipo,
                            "orden": item.get("orden", ""),
                            "fecha_promulgacion": fecha_promulgacion,
                            "fuente_boe": fuente_boe
                        }
                        documents.append(text)
                        metadatas.append(meta)
                        ids.append(f"disp_{uuid.uuid4().hex[:8]}")
                        count += 1
            
        # Case 2: Structured parts (Titles with Articles)
        elif "artículos" in parte:
            titulo_tipo = parte.get("tipo", "")
            titulo_orden = parte.get("orden", "")
            
            for articulo in parte["artículos"]:
                art_numero = articulo.get("número", "")
                
                if "apartados" in articulo:
                    for apartado in articulo["apartados"]:
                        text = apartado.get("texto", "")
                        if text:
                            meta = {
                                "titulo_tipo": titulo_tipo,
                                "titulo_orden": titulo_orden,
                                "articulo": art_numero,
                                "apartado": apartado.get("orden", ""),
                                "fecha_promulgacion": fecha_promulgacion,
                                "fuente_boe": fuente_boe
                            }
                            documents.append(text)
                            metadatas.append(meta)
                            # Create a unique ID
                            # Cleaning strings for ID
                            safe_titulo = "".join(c for c in titulo_orden if c.isalnum())
                            safe_art = "".join(c for c in art_numero if c.isalnum())
                            safe_ap = "".join(c for c in apartado.get('orden', '') if c.isalnum())
                            
                            ids.append(f"{safe_titulo}_{safe_art}_{safe_ap}_{uuid.uuid4().hex[:8]}")
                            count += 1

    # Add to collection
    if documents:
        print(f"Adding {len(documents)} documents to ChromaDB...")
        # Adding in batches to be safe, though not strictly necessary for small datasets
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            end = min(i + batch_size, len(documents))
            print(f"Processing batch {i} to {end}...")
            collection.add(
                documents=documents[i:end],
                metadatas=metadatas[i:end],
                ids=ids[i:end]
            )
        print("Done.")
    else:
        print("No documents found to add.")

if __name__ == "__main__":
    main()
