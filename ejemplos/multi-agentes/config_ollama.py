"""
config_ollama.py
Configuración centralizada para LangChain + Ollama
"""

import os
from typing import Optional
from langchain_ollama import OllamaLLM

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

# URL del servidor Ollama local
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Modelos disponibles (en orden de peso: más ligero → más pesado)
MODELOS = {
    "tinyllama": {
        "nombre": "TinyLlama (1.1B)",
        "descripcion": "Ultraligero, muy rápido",
        "recomendado_para": "tests rápidos, desarrollo",
        "ram_minima": 2,  # GB
    },
    "orca-mini": {
        "nombre": "Orca Mini (3.3B)",
        "descripcion": "Ligero, buen balance",
        "recomendado_para": "desarrollo normal",
        "ram_minima": 4,
    },
    "neural-chat": {
        "nombre": "Neural Chat (7B)",
        "descripcion": "Conversacional, bueno para diálogos",
        "recomendado_para": "agentes conversacionales",
        "ram_minima": 8,
    },
    "mistral": {
        "nombre": "Mistral (7B)",
        "descripcion": "Rápido, muy capaz",
        "recomendado_para": "producción pequeña",
        "ram_minima": 8,
    },
    "llama2": {
        "nombre": "Llama 2 (7B/13B)",
        "descripcion": "Potente, versatil",
        "recomendado_para": "tareas complejas",
        "ram_minima": 12,
    },
}

# Modelo por defecto
MODELO_DEFECTO = os.getenv("OLLAMA_MODEL", "mistral")

# Parámetros de generación
GENERATION_PARAMS = {
    "temperature": 0.7,  # Creatividad (0=determinista, 1=aleatorio)
    "top_p": 0.9,  # Nucleus sampling
    "num_ctx": 2048,  # Tamaño contexto
}

# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def obtener_llm(modelo: Optional[str] = None, temperatura: float = 0.7) -> OllamaLLM:
    """
    Factory para obtener instancia de LLM configurada.
    
    Args:
        modelo: nombre del modelo (si None, usa default)
        temperatura: valor entre 0 y 1
    
    Returns:
        OllamaLLM configurado y conectado
    
    Ejemplo:
        >>> llm = obtener_llm()
        >>> respuesta = llm.invoke("Hola mundo")
    """
    modelo_a_usar = modelo or MODELO_DEFECTO
    
    if modelo_a_usar not in MODELOS:
        modelos_disponibles = ", ".join(MODELOS.keys())
        raise ValueError(
            f"Modelo '{modelo_a_usar}' no reconocido.\n"
            f"Opciones: {modelos_disponibles}"
        )
    
    return OllamaLLM(
        model=modelo_a_usar,
        base_url=OLLAMA_BASE_URL,
        temperature=temperatura,
    )

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def listar_modelos() -> None:
    """Muestra modelos disponibles con información."""
    print("\n" + "="*70)
    print("MODELOS DISPONIBLES EN OLLAMA")
    print("="*70)
    
    for key, info in MODELOS.items():
        print(f"\n📦 {key.upper()}")
        print(f"   Nombre: {info['nombre']}")
        print(f"   Descripción: {info['descripcion']}")
        print(f"   Recomendado: {info['recomendado_para']}")
        print(f"   RAM mínima: {info['ram_minima']} GB")
        
        if key == MODELO_DEFECTO:
            print("   ⭐ MODELO POR DEFECTO")
    
    print("\n" + "="*70 + "\n")

def obtener_info_modelo(modelo: str) -> dict:
    """Retorna información de un modelo específico."""
    if modelo not in MODELOS:
        raise ValueError(f"Modelo '{modelo}' no encontrado")
    return MODELOS[modelo]

# ============================================================================
# PROMPTS REUTILIZABLES
# ============================================================================

PROMPTS = {
    "respuesta_corta": (
        "Responde de forma concisa en máximo 2 frases. "
        "Pregunta: {pregunta}"
    ),
    
    "respuesta_estructurada": (
        "Responde estructuradamente:\n"
        "1. Resumen en 1 línea\n"
        "2. Detalles clave (3-5 puntos)\n"
        "3. Conclusión\n\n"
        "Pregunta: {pregunta}"
    ),
    
    "razonamiento_paso_a_paso": (
        "Razona paso a paso:\n"
        "1. Analiza el problema\n"
        "2. Identifica pasos necesarios\n"
        "3. Explica cada paso\n"
        "4. Conclusión\n\n"
        "Problema: {pregunta}"
    ),
    
    "rol_agente": (
        "Eres un {rol}. Tu objetivo es {objetivo}.\n"
        "Responde mantiendo este rol.\n\n"
        "Pregunta: {pregunta}"
    ),
    
    "decision_agente": (
        "Eres un agente autónomo que debe tomar una decisión.\n"
        "Contexto: {contexto}\n"
        "Opciones: {opciones}\n"
        "Criterios: {criterios}\n\n"
        "¿Cuál es tu decisión y por qué?"
    ),
}

def obtener_prompt(template: str, **kwargs) -> str:
    """
    Obtiene prompt personalizado del diccionario.
    
    Args:
        template: clave del prompt en PROMPTS
        **kwargs: variables para reemplazar en el template
    
    Returns:
        Prompt formateado
    
    Ejemplo:
        >>> prompt = obtener_prompt("respuesta_corta", pregunta="¿Qué es IA?")
    """
    if template not in PROMPTS:
        plantillas_disponibles = ", ".join(PROMPTS.keys())
        raise ValueError(
            f"Template '{template}' no encontrado.\n"
            f"Opciones: {plantillas_disponibles}"
        )
    
    return PROMPTS[template].format(**kwargs)

# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    print("🧪 TEST: config_ollama.py\n")
    
    # Test 1: Listar modelos
    print("✅ Test 1: Listar modelos")
    listar_modelos()
    
    # Test 2: Obtener LLM
    print("✅ Test 2: Obtener LLM (esto tomará unos segundos...)")
    try:
        llm = obtener_llm()
        print(f"   LLM obtenido: {MODELO_DEFECTO}")
        
        # Test 3: Invocar modelo
        print("\n✅ Test 3: Invocar modelo")
        respuesta = llm.invoke("Di 'Hola mundo' en una sola línea")
        print(f"   Respuesta: {respuesta}\n")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("\n   💡 Asegúrate de que Ollama está corriendo:")
        print("      ollama serve")
        print("      (en otra terminal)")
        print("\n   💡 Y que el modelo está descargado:")
        print(f"      ollama pull {MODELO_DEFECTO}")
    
    # Test 4: Prompts reutilizables
    print("✅ Test 4: Prompts reutilizables")
    prompt = obtener_prompt("respuesta_corta", pregunta="¿Qué es machine learning?")
    print(f"   Template 'respuesta_corta':\n   {prompt}\n")
    
    print("✅ Todos los tests completados")
