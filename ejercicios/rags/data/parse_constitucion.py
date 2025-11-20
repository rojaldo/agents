import re
import json
import sys

def parse_constitucion(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"DEBUG: Read {len(lines)} lines from {file_path}")
    sys.stdout.flush()

    structure = {
        "preambulo": "",
        "titulo_preliminar": {"articulos": []},
        "titulos": [],
        "disposiciones": {
            "adicionales": [],
            "transitorias": [],
            "derogatoria": [],
            "final": []
        }
    }

    current_state = "START" # START, PREAMBULO, TITULO_PRELIMINAR, TITULO, DISPOSICIONES
    current_titulo = None
    current_capitulo = None
    current_seccion = None
    current_articulo = None
    current_apartado = None
    
    # Regex patterns
    re_titulo_preliminar = re.compile(r'^TÍTULO PRELIMINAR', re.IGNORECASE)
    re_titulo = re.compile(r'^TÍTULO\s+(?!PRELIMINAR)(.*)', re.IGNORECASE)
    re_capitulo = re.compile(r'^CAPÍTULO\s+(.*)', re.IGNORECASE)
    re_seccion = re.compile(r'^Sección\s+(.*)', re.IGNORECASE)
    re_articulo = re.compile(r'^Artículo\s+(\d+)\.', re.IGNORECASE)
    re_apartado = re.compile(r'^(\d+)\.\s+(.*)')
    re_subapartado = re.compile(r'^([a-z])\)\s+(.*)')
    re_disposicion_adicional = re.compile(r'^DISPOSICI[OÓ]NE?S?\s+ADICIONAL', re.IGNORECASE)
    re_disposicion_transitoria = re.compile(r'^DISPOSICI[OÓ]NE?S?\s+TRANSITORIA', re.IGNORECASE)
    re_disposicion_derogatoria = re.compile(r'^DISPOSICI[OÓ]NE?S?\s+(DEROGATORIA|DOGATORIA)', re.IGNORECASE)
    re_disposicion_final = re.compile(r'^DISPOSICI[OÓ]NE?S?\s+FINAL', re.IGNORECASE)
    re_preambulo = re.compile(r'^PREÁMBULO', re.IGNORECASE)
    re_indice = re.compile(r'^ÍNDICE', re.IGNORECASE)

    # Helper to clean text
    def clean(text):
        return text.strip()

    buffer_text = []

    def flush_buffer_to_last_element():
        nonlocal buffer_text, current_articulo, current_apartado, current_state
        text = " ".join([l.strip() for l in buffer_text if l.strip()]).strip()
        buffer_text = []
        if not text:
            return

        if current_state == "PREAMBULO":
            structure["preambulo"] += text + " "
        elif current_apartado:
            # Append to current apartado content if it's just text continuation
            # But wait, apartados usually start with "1. Text".
            # If we have text in buffer that didn't match a new structure, it belongs to the last active element.
            if "contenido" in current_apartado:
                 current_apartado["contenido"] += " " + text
            else:
                 current_apartado["contenido"] = text
        elif current_articulo:
             # If article has no apartados yet, this text belongs to the article body (intro text)
             if "contenido" in current_articulo:
                 current_articulo["contenido"] += " " + text
             else:
                 current_articulo["contenido"] = text
        # Handle other states if necessary

    # We need a more robust state machine.
    # The file has an index at the beginning which we should skip.
    # The actual content starts after "PREÁMBULO" (the second time it appears, or check context).
    # Actually, the file starts with "Constitución Española...". Then "ÍNDICE". Then "PREÁMBULO".
    
    # Let's iterate and switch context.
    
    iterator = iter(lines)
    
    # Skip until first PREÁMBULO after ÍNDICE
    # Or just look for the headers.
    
    # Reset state variables
    current_context = "ROOT" # ROOT, PREAMBULO, BODY, DISPOSICIONES
    
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check for Index
        if re_indice.match(line):
            current_context = "INDEX"
            continue

        if current_context == "INDEX":
            if re_preambulo.match(line):
                current_context = "PREAMBULO"
                continue
            else:
                continue
            
        if "DISPOSICIONES" in line:
            print(f"DEBUG: Found DISPOSICIONES: '{line}'")
            if re_disposicion_adicional.match(line):
                print("DEBUG: Matched ADICIONAL")
            else:
                print("DEBUG: Did NOT match ADICIONAL")
            sys.stdout.flush()

        # Check for headers
        if re_preambulo.match(line):
            # There might be one in the index. The real one is followed by text.
            # Let's assume the last one or the one after INDICE is the real one.
            # Given the file structure, "PREÁMBULO" appears, then text.
            # If we are already in BODY, ignore (it shouldn't happen).
            if current_context == "ROOT":
                current_context = "PREAMBULO"
                continue
        
        if re_titulo_preliminar.match(line):
            current_context = "BODY"
            current_state = "TITULO_PRELIMINAR"
            current_titulo = structure["titulo_preliminar"]
            current_capitulo = None
            current_seccion = None
            current_articulo = None
            current_apartado = None
            continue
            
        if re_titulo.match(line):
            current_context = "BODY"
            current_state = "TITULO"
            current_titulo = {"nombre": line, "capitulos": [], "articulos": []} # articulos directly if no chapters
            structure["titulos"].append(current_titulo)
            current_capitulo = None
            current_seccion = None
            current_articulo = None
            current_apartado = None
            continue
            
        if re_capitulo.match(line):
            if current_titulo:
                current_capitulo = {"nombre": line, "secciones": [], "articulos": []}
                if "capitulos" not in current_titulo:
                    current_titulo["capitulos"] = []
                current_titulo["capitulos"].append(current_capitulo)
                current_seccion = None
                current_articulo = None
                current_apartado = None
            continue

        if re_seccion.match(line):
            if current_capitulo:
                current_seccion = {"nombre": line, "articulos": []}
                current_capitulo["secciones"].append(current_seccion)
                current_articulo = None
                current_apartado = None
            elif current_titulo:
                # Section directly under Title? Rare but possible if parsing fails
                pass
            continue

        match_articulo = re_articulo.match(line)
        if match_articulo:
            current_articulo = {"numero": line, "contenido": "", "apartados": []}
            current_apartado = None
            
            # Add to correct parent
            if current_seccion:
                current_seccion["articulos"].append(current_articulo)
            elif current_capitulo:
                current_capitulo["articulos"].append(current_articulo)
            elif current_titulo:
                if "articulos" not in current_titulo:
                     current_titulo["articulos"] = []
                current_titulo["articulos"].append(current_articulo)
            elif current_state == "TITULO_PRELIMINAR":
                structure["titulo_preliminar"]["articulos"].append(current_articulo)
            continue

        # Check for Disposiciones
        if re_disposicion_adicional.match(line):
            current_context = "DISPOSICIONES"
            current_state = "ADICIONAL"
            # Logic for dispositions... they are like articles but different structure
            continue
        if re_disposicion_transitoria.match(line):
            current_context = "DISPOSICIONES"
            current_state = "TRANSITORIA"
            continue
        if re_disposicion_derogatoria.match(line):
            current_context = "DISPOSICIONES"
            current_state = "DEROGATORIA"
            continue
        if re_disposicion_final.match(line):
            current_context = "DISPOSICIONES"
            current_state = "FINAL"
            continue

        # Content processing
        if current_context == "PREAMBULO":
            # Avoid capturing "CONSTITUCIÓN" or "TÍTULO PRELIMINAR" if they appear
            if "CONSTITUCIÓN" in line or "TÍTULO PRELIMINAR" in line:
                continue
            structure["preambulo"] += line + " "
            continue

        if current_context == "BODY":
            if current_articulo:
                # Check for apartados
                match_apartado = re_apartado.match(line)
                match_subapartado = re_subapartado.match(line)
                
                if match_apartado:
                    current_apartado = {"numero": match_apartado.group(1), "contenido": match_apartado.group(2), "subapartados": []}
                    current_articulo["apartados"].append(current_apartado)
                elif match_subapartado and current_apartado:
                    current_apartado["subapartados"].append(line)
                else:
                    # Continuation of text
                    if current_apartado:
                        current_apartado["contenido"] += " " + line
                    else:
                        current_articulo["contenido"] += " " + line
        
        if current_context == "DISPOSICIONES":
            # Just collect text for now as list of strings
            if current_state == "ADICIONAL":
                structure["disposiciones"]["adicionales"].append(line)
            elif current_state == "TRANSITORIA":
                structure["disposiciones"]["transitorias"].append(line)
            elif current_state == "DEROGATORIA":
                structure["disposiciones"]["derogatoria"].append(line)
            elif current_state == "FINAL":
                structure["disposiciones"]["final"].append(line)

    # Clean up preambulo
    structure["preambulo"] = structure["preambulo"].strip()
    
    with open('constitucion.json', 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    parse_constitucion(sys.argv[1])
