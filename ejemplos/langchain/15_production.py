#!/usr/bin/env python3
"""
15_production.py - Prácticas de Producción

Demuestra:
- Error handling robusto
- Logging estructurado
- Health checks
- Caching
"""

import logging
import json
from datetime import datetime
from typing import Optional
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain import cache


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============ EJEMPLOS ============

def ejemplo_error_handling():
    """Error handling robusto"""
    print("=" * 60)
    print("EJEMPLO 1: Error Handling Robusto")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    def invocar_seguro(prompt_text: str) -> Optional[str]:
        """Invocar con manejo completo de errores"""
        try:
            resultado = llm.invoke(prompt_text)
            logger.info(f"✓ Éxito: {len(resultado)} caracteres")
            return resultado

        except TimeoutError:
            logger.error("⏱️  Timeout: La respuesta tardó demasiado")
            return "Disculpa, el sistema tardó demasiado"

        except ValueError as e:
            logger.error(f"❌ Error de validación: {e}")
            return f"Error: Input inválido"

        except ConnectionError as e:
            logger.error(f"🔌 Error de conexión: {e}")
            return "No se pudo conectar con el servidor"

        except Exception as e:
            logger.critical(f"💥 Error inesperado: {e}", exc_info=True)
            return "Error inesperado. El equipo ha sido notificado"

    print("\nProbando diferentes escenarios:")

    escenarios = [
        "¿Qué es Python?",
        "Cuéntame un chiste",
        "¿Cómo funciona la gravedad?",
    ]

    for pregunta in escenarios:
        print(f"\n❓ {pregunta}")
        respuesta = invocar_seguro(pregunta)
        print(f"✓ {respuesta[:80]}...")

    print()


def ejemplo_logging_estructurado():
    """Logging estructurado en JSON"""
    print("=" * 60)
    print("EJEMPLO 2: Logging Estructurado")
    print("=" * 60)

    class StructuredLogger:
        """Logger que genera logs estructurados en JSON"""

        def __init__(self, name):
            self.logger = logging.getLogger(name)

        def log_event(self, event_type: str, **kwargs):
            """Log un evento con contexto"""
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                **kwargs
            }
            self.logger.info(json.dumps(log_data))

        def log_invoke(self, input_text: str, output_text: str, duration_ms: float):
            """Log de una invocación"""
            self.log_event(
                "invoke",
                input_length=len(input_text),
                output_length=len(output_text),
                duration_ms=duration_ms
            )

        def log_error(self, error_type: str, error_msg: str, context: dict = None):
            """Log de un error"""
            self.log_event(
                "error",
                error_type=error_type,
                error_msg=error_msg,
                context=context or {}
            )

    slog = StructuredLogger("produccion")

    print("\nGenerando logs estructurados:")

    # Simular eventos
    slog.log_invoke(
        input_text="¿Qué es Python?",
        output_text="Python es un lenguaje...",
        duration_ms=245
    )

    slog.log_error(
        error_type="TimeoutError",
        error_msg="La respuesta tardó más de 30 segundos",
        context={"retry": 1, "model": "mistral"}
    )

    slog.log_event(
        "health_check",
        ollama_status="healthy",
        model_loaded=True
    )

    print("✓ Logs registrados\n")


def ejemplo_health_check():
    """Health checks del sistema"""
    print("=" * 60)
    print("EJEMPLO 3: Health Checks")
    print("=" * 60)

    import requests

    def check_ollama() -> bool:
        """Verifica que Ollama está activo"""
        try:
            response = requests.get(
                "http://localhost:11434/api/tags",
                timeout=2
            )
            return response.status_code == 200
        except:
            return False

    def check_llm() -> bool:
        """Verifica que el LLM responde"""
        try:
            llm = Ollama(model="mistral", base_url="http://localhost:11434")
            respuesta = llm.invoke("test")
            return len(respuesta) > 0
        except:
            return False

    def check_memory() -> bool:
        """Verifica disponibilidad de memoria"""
        try:
            import psutil
            memoria_libre = psutil.virtual_memory().available / (1024**3)
            return memoria_libre > 0.5  # Al menos 500MB
        except:
            return True  # Si no se puede verificar, asumir OK

    def health_check() -> dict:
        """Health check completo"""
        checks = {
            "ollama": check_ollama(),
            "llm": check_llm(),
            "memory": check_memory(),
        }

        all_ok = all(checks.values())

        return {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy" if all_ok else "degraded",
            "checks": checks
        }

    print("\nEjecutando health checks:")

    health = health_check()

    print(f"\nEstado: {health['status']}")
    for check_name, result in health['checks'].items():
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")

    print()


def ejemplo_caching():
    """Caching de respuestas"""
    print("=" * 60)
    print("EJEMPLO 4: Caching de Respuestas")
    print("=" * 60)

    from langchain.cache import InMemoryCache
    import time

    # Activar caching
    cache.llm_cache = InMemoryCache()

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    print("\nDemostrando caching:")

    pregunta = "¿Cuál es la capital de Francia?"

    # Primera llamada (sin caché)
    print(f"\n1️⃣  Primera llamada (sin caché):")
    print(f"   Pregunta: {pregunta}")

    try:
        inicio = time.time()
        respuesta1 = llm.invoke(pregunta)
        tiempo1 = time.time() - inicio

        print(f"   Tiempo: {tiempo1:.2f}s")
        print(f"   Respuesta: {respuesta1.strip()[:80]}...")

        # Segunda llamada (con caché)
        print(f"\n2️⃣  Segunda llamada (con caché):")
        print(f"   Pregunta: {pregunta}")

        inicio = time.time()
        respuesta2 = llm.invoke(pregunta)
        tiempo2 = time.time() - inicio

        print(f"   Tiempo: {tiempo2:.2f}s")
        print(f"   Respuesta: {respuesta2.strip()[:80]}...")

        print(f"\n📊 Mejora: {tiempo1/tiempo2:.1f}x más rápido\n")

    except Exception as e:
        print(f"   Error: {e}\n")

    # Desactivar caching
    cache.llm_cache = None


def ejemplo_batch_processing():
    """Procesamiento en batch"""
    print("=" * 60)
    print("EJEMPLO 5: Batch Processing")
    print("=" * 60)

    llm = Ollama(model="mistral", base_url="http://localhost:11434")
    template = "¿Cuál es la capital de {pais}?"
    prompt = PromptTemplate.from_template(template)
    cadena = prompt | llm

    print("\nProcesamiento en batch:")

    paises = [
        {"pais": "Francia"},
        {"pais": "Japón"},
        {"pais": "Brasil"},
        {"pais": "Canadá"},
    ]

    try:
        print(f"\nProcesando {len(paises)} items...")

        # Batch es más eficiente que invoke individual
        respuestas = cadena.batch(paises)

        print("\nResultados:")
        for pais, respuesta in zip(paises, respuestas):
            print(f"  {pais['pais']:12} → {respuesta.strip()[:60]}...")

    except Exception as e:
        print(f"Error: {e}")

    print()


def ejemplo_configuracion_dinamica():
    """Configuración dinámica según modo"""
    print("=" * 60)
    print("EJEMPLO 6: Configuración Dinámica")
    print("=" * 60)

    class LLMFactory:
        """Factory para crear LLMs con diferentes configuraciones"""

        MODELOS = {
            "desarrollo": {
                "model": "neural-chat",
                "temperature": 0.7,
                "description": "Rápido para desarrollo"
            },
            "produccion": {
                "model": "mistral",
                "temperature": 0.3,
                "description": "Estable para producción"
            },
            "creativo": {
                "model": "mistral",
                "temperature": 0.9,
                "description": "Para tareas creativas"
            }
        }

        @staticmethod
        def create_llm(modo: str = "desarrollo") -> Ollama:
            """Crear LLM según modo"""
            if modo not in LLMFactory.MODELOS:
                logger.warning(f"Modo {modo} desconocido, usando desarrollo")
                modo = "desarrollo"

            config = LLMFactory.MODELOS[modo]
            logger.info(f"Creando LLM en modo {modo}: {config['description']}")

            return Ollama(
                model=config["model"],
                base_url="http://localhost:11434",
                temperature=config["temperature"]
            )

    print("\nModos disponibles:")
    for modo, config in LLMFactory.MODELOS.items():
        print(f"  • {modo:15} - {config['description']}")

    # Crear LLMs en diferentes modos
    llm_dev = LLMFactory.create_llm("desarrollo")
    llm_prod = LLMFactory.create_llm("produccion")

    print("\nLLMs creados correctamente ✓\n")


if __name__ == "__main__":
    try:
        ejemplo_error_handling()
        ejemplo_logging_estructurado()
        ejemplo_health_check()
        ejemplo_caching()
        ejemplo_batch_processing()
        ejemplo_configuracion_dinamica()

        print("=" * 60)
        print("✅ Todos los ejemplos de producción completados")
        print("=" * 60)

    except Exception as e:
        logger.critical(f"Error fatal: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
