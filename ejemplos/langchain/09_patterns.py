#!/usr/bin/env python3
"""
09_patterns.py - Patrones Comunes en LangChain

Demuestra:
- Sequential processing
- Branching logic
- Fallbacks
- Conditional routing
"""

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda


def ejemplo_secuencial():
    """Procesamiento secuencial: cadena 1 -> cadena 2 -> cadena 3"""
    print("=" * 60)
    print("EJEMPLO 1: Sequential Processing")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    parser = StrOutputParser()

    # Paso 1: Simplificar texto
    template1 = "Simplifica este texto en una línea: {texto}"
    prompt1 = PromptTemplate.from_template(template1)
    cadena1 = prompt1 | llm | parser

    # Paso 2: Clasificar por tono
    template2 = "¿Es este texto positivo, negativo o neutral? {texto}\nRespuesta:"
    prompt2 = PromptTemplate.from_template(template2)
    cadena2 = prompt2 | llm | parser

    # Paso 3: Generar emoji
    template3 = "¿Qué emoji representa mejor este tono: {tono}?"
    prompt3 = PromptTemplate.from_template(template3)
    cadena3 = prompt3 | llm | parser

    print("\nProcesamiento secuencial:")

    texto_original = "El nuevo producto de la empresa es excelente y revolucionario"

    try:
        print(f"\nTexto original: {texto_original}")

        # Paso 1
        print("\n1️⃣  Simplificar:")
        texto_simple = cadena1.invoke({"texto": texto_original})
        print(f"   {texto_simple.strip()}")

        # Paso 2
        print("\n2️⃣  Clasificar tono:")
        tono = cadena2.invoke({"texto": texto_simple})
        print(f"   {tono.strip()}")

        # Paso 3
        print("\n3️⃣  Emoji:")
        emoji = cadena3.invoke({"tono": tono})
        print(f"   {emoji.strip()}\n")

    except Exception as e:
        print(f"Error: {e}\n")


def ejemplo_branching():
    """Lógica condicional: diferentes flujos según entrada"""
    print("=" * 60)
    print("EJEMPLO 2: Branching Logic")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    parser = StrOutputParser()

    # Rama 1: Pregunta técnica
    template_tecnica = """Eres experto en programación.
Responde esta pregunta técnica: {pregunta}"""
    prompt_tecnica = PromptTemplate.from_template(template_tecnica)
    rama_tecnica = prompt_tecnica | llm | parser

    # Rama 2: Pregunta general
    template_general = """Eres un asistente amable.
Responde: {pregunta}"""
    prompt_general = PromptTemplate.from_template(template_general)
    rama_general = prompt_general | llm | parser

    # Rama 3: Default
    template_default = """Simplemente responde: {pregunta}"""
    prompt_default = PromptTemplate.from_template(template_default)
    rama_default = prompt_default | llm | parser

    # Crear rama principal
    rama = RunnableBranch(
        (lambda x: "código" in x["pregunta"].lower() or "programa" in x["pregunta"].lower(),
         rama_tecnica),
        (lambda x: "cómo" in x["pregunta"].lower() or "qué es" in x["pregunta"].lower(),
         rama_general),
        rama_default
    )

    print("\nBranching según tipo de pregunta:")

    preguntas = [
        "¿Cómo escribo una función en Python?",
        "¿Qué es la felicidad?",
        "Dame 3 colores"
    ]

    for pregunta in preguntas:
        try:
            print(f"\n❓ {pregunta}")

            # Determinar rama
            if "código" in pregunta.lower() or "programa" in pregunta.lower():
                rama_usada = "Técnica"
            elif "cómo" in pregunta.lower() or "qué es" in pregunta.lower():
                rama_usada = "General"
            else:
                rama_usada = "Default"

            print(f"   Rama: {rama_usada}")

            respuesta = rama.invoke({"pregunta": pregunta})
            print(f"   ✓ {respuesta.strip()[:80]}...")

        except Exception as e:
            print(f"   Error: {e}")

    print()


def ejemplo_fallback():
    """Fallback: usar cadena alternativa si la principal falla"""
    print("=" * 60)
    print("EJEMPLO 3: Fallbacks")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    parser = StrOutputParser()

    # Cadena principal (compleja)
    template_principal = """Eres un experto en {tema}.
    Analiza profundamente: {pregunta}
    Proporciona un análisis detallado con conclusiones."""
    prompt_principal = PromptTemplate.from_template(template_principal)
    cadena_principal = prompt_principal | llm | parser

    # Cadena respaldo (simple)
    template_respaldo = """Responde brevemente: {pregunta}"""
    prompt_respaldo = PromptTemplate.from_template(template_respaldo)
    cadena_respaldo = prompt_respaldo | llm | parser

    # Crear cadena con fallback
    cadena_segura = cadena_principal.with_fallbacks([cadena_respaldo])

    print("\nUsando fallback:")

    pregunta = "¿Cuál es el impacto de la IA en la sociedad?"
    tema = "tecnología"

    try:
        print(f"\nPregunta: {pregunta}")
        print("Tema: {tema}")
        print("\n(Intenta cadena principal primero, luego respaldo si falla)")

        respuesta = cadena_segura.invoke({
            "pregunta": pregunta,
            "tema": tema
        })

        print(f"\n✓ Respuesta: {respuesta.strip()[:150]}...\n")

    except Exception as e:
        print(f"Error: {e}\n")


def ejemplo_condicional_avanzado():
    """Routing condicional más complejo"""
    print("=" * 60)
    print("EJEMPLO 4: Conditional Routing Avanzado")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    parser = StrOutputParser()

    # Definir cadenas para cada caso
    cadenas = {
        "matematica": PromptTemplate.from_template(
            "Resuelve: {pregunta}"
        ) | llm | parser,

        "historia": PromptTemplate.from_template(
            "Como historiador, explica: {pregunta}"
        ) | llm | parser,

        "filosofia": PromptTemplate.from_template(
            "Desde una perspectiva filosófica: {pregunta}"
        ) | llm | parser,

        "ciencia": PromptTemplate.from_template(
            "Explicación científica de: {pregunta}"
        ) | llm | parser,
    }

    def detectar_categoria(pregunta):
        """Detecta la categoría de la pregunta"""
        palabras_clave = {
            "matematica": ["número", "suma", "ecuación", "calcula"],
            "historia": ["cuando", "pasado", "guerra", "imperio"],
            "filosofia": ["sentido", "razón", "existencia", "bien", "mal"],
            "ciencia": ["qué es", "cómo funciona", "leyes", "átomos"],
        }

        pregunta_lower = pregunta.lower()
        for categoria, palabras in palabras_clave.items():
            if any(palabra in pregunta_lower for palabra in palabras):
                return categoria

        return "ciencia"  # Default

    print("\nRouting basado en categoría detectada:")

    preguntas = [
        "¿Cuánto es 5 multiplicado por 3?",
        "¿Qué pasó en 1492?",
        "¿Cuál es el sentido de la vida?"
    ]

    for pregunta in preguntas:
        try:
            categoria = detectar_categoria(pregunta)
            print(f"\n❓ {pregunta}")
            print(f"   📂 Categoría: {categoria}")

            respuesta = cadenas[categoria].invoke({"pregunta": pregunta})
            print(f"   ✓ {respuesta.strip()[:80]}...")

        except Exception as e:
            print(f"   Error: {e}")

    print()


def ejemplo_pipeline_completo():
    """Pipeline completo combinando varios patrones"""
    print("=" * 60)
    print("EJEMPLO 5: Pipeline Completo")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    parser = StrOutputParser()

    # PASO 1: Validar entrada
    def validar_entrada(texto):
        if not texto or len(texto) < 5:
            raise ValueError("Entrada demasiado corta")
        return {"texto": texto}

    # PASO 2: Procesar según tipo
    template_pregunta = "¿De qué trata la pregunta? {texto}"
    cadena_analizar = PromptTemplate.from_template(template_pregunta) | llm | parser

    # PASO 3: Expandir respuesta
    template_expandir = "Explica más sobre: {tema}"
    cadena_expandir = PromptTemplate.from_template(template_expandir) | llm | parser

    print("\nPipeline (validar → analizar → expandir):")

    entrada = "¿Qué es un LLM?"

    try:
        print(f"\nEntrada: {entrada}")

        # Validar
        print("\n1️⃣  Validando...")
        datos = validar_entrada(entrada)
        print("   ✓ Válida")

        # Analizar
        print("\n2️⃣  Analizando...")
        analisis = cadena_analizar.invoke(datos)
        print(f"   Tema: {analisis.strip()[:50]}...")

        # Expandir
        print("\n3️⃣  Expandiendo...")
        expansion = cadena_expandir.invoke({"tema": analisis})
        print(f"   {expansion.strip()[:100]}...\n")

    except Exception as e:
        print(f"Error: {e}\n")


if __name__ == "__main__":
    try:
        ejemplo_secuencial()
        ejemplo_branching()
        ejemplo_fallback()
        ejemplo_condicional_avanzado()
        ejemplo_pipeline_completo()

        print("=" * 60)
        print("✅ Todos los ejemplos de patrones completados")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
