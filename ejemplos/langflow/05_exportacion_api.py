#!/usr/bin/env python3
"""
05_exportacion_api.py - Exportación y Despliegue de Langflow

Demuestra cómo exportar flujos de Langflow a APIs ejecutables:
- Crear servidores FastAPI
- Agregar autenticación
- Health checks y monitoring
- Configuración de producción
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import logging
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# EJEMPLO 1: Crear un servidor FastAPI simple
# ============================================================================

def ejemplo_1_api_simple():
    """Ejemplo 1: Servidor FastAPI basado en Langflow"""
    print("=" * 60)
    print("EJEMPLO 1: FastAPI Simple Server")
    print("=" * 60)

    app = FastAPI(title="Langflow Chat API", version="1.0.0")

    # Modelos de request/response
    class ChatRequest(BaseModel):
        message: str
        user_id: str = "anónimo"

    class ChatResponse(BaseModel):
        user_id: str
        input_message: str
        bot_response: str
        timestamp: str
        status: str

    # LLM
    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente útil y amable"),
        ("user", "{message}")
    ])

    cadena = prompt | llm

    @app.post("/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest):
        """Endpoint de chat"""
        try:
            respuesta = cadena.invoke({"message": request.message})
            logger.info(f"Chat completado para usuario: {request.user_id}")

            return ChatResponse(
                user_id=request.user_id,
                input_message=request.message,
                bot_response=respuesta,
                timestamp=datetime.now().isoformat(),
                status="success"
            )
        except Exception as e:
            logger.error(f"Error en chat: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/health")
    async def health():
        """Health check endpoint"""
        return {"status": "ok", "timestamp": datetime.now().isoformat()}

    print("\n📱 Servidor creado con endpoints:")
    print("   POST /chat - Procesa mensajes de chat")
    print("   GET /health - Verifica salud del servidor\n")

    # Simular requests (en lugar de ejecutar el servidor)
    print("🔄 Simulando requests al API:")

    try:
        # Simular chat request
        test_request = ChatRequest(
            message="¿Cuál es la capital de Francia?",
            user_id="usuario_123"
        )

        print(f"\n   📤 Request: {test_request.message}")
        respuesta = cadena.invoke({"message": test_request.message})
        print(f"   📥 Response: {respuesta[:80]}...")
        logger.info(f"Simulación completada")

    except Exception as e:
        print(f"   ❌ Error: {e}")


# ============================================================================
# EJEMPLO 2: Autenticación con tokens
# ============================================================================

def ejemplo_2_autenticacion():
    """Ejemplo 2: API con autenticación por tokens"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: API con Autenticación")
    print("=" * 60)

    # Token válido (en producción usar JWT)
    VALID_TOKEN = "langflow-secret-token-12345"

    def verificar_token(token: str) -> bool:
        """Verifica el token de autenticación"""
        return token == VALID_TOKEN

    class QueryRequest(BaseModel):
        query: str
        token: str

    class QueryResponse(BaseModel):
        success: bool
        result: str
        error: str = None

    llm = Ollama(model="mistral", base_url="http://localhost:11434")

    prompt = ChatPromptTemplate.from_template(
        "Responde brevemente: {query}"
    )
    cadena = prompt | llm

    print("\n🔐 Configuración de autenticación:")
    print(f"   Token válido: {VALID_TOKEN}")

    # Simular requests autenticadas
    test_cases = [
        ("token-invalido", "¿Qué es Langflow?"),
        (VALID_TOKEN, "¿Qué es Langflow?"),
    ]

    print(f"\n🔄 Probando {len(test_cases)} requests:\n")

    for token, query in test_cases:
        print(f"   Query: {query}")
        print(f"   Token: {token[:15]}...")

        if verificar_token(token):
            try:
                respuesta = cadena.invoke({"query": query})
                print(f"   ✅ Autenticado - Respuesta: {respuesta[:60]}...")
                logger.info(f"Request autenticado: {query}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Token inválido - Acceso denegado")
            logger.warning(f"Intento de acceso con token inválido")

        print()


# ============================================================================
# EJEMPLO 3: Rate limiting y monitoreo
# ============================================================================

def ejemplo_3_rate_limiting():
    """Ejemplo 3: Control de rate limiting y monitoreo"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Rate Limiting y Monitoreo")
    print("=" * 60)

    class RateLimiter:
        """Control simple de rate limiting"""
        def __init__(self, max_requests=10, window_seconds=60):
            self.max_requests = max_requests
            self.window_seconds = window_seconds
            self.requests = {}

        def is_allowed(self, user_id: str) -> bool:
            """Verifica si el usuario puede hacer otra request"""
            now = datetime.now().timestamp()

            if user_id not in self.requests:
                self.requests[user_id] = []

            # Limpiar requests antiguas
            self.requests[user_id] = [
                req_time for req_time in self.requests[user_id]
                if now - req_time < self.window_seconds
            ]

            if len(self.requests[user_id]) < self.max_requests:
                self.requests[user_id].append(now)
                return True
            return False

        def get_remaining(self, user_id: str) -> int:
            """Obtiene requests restantes"""
            now = datetime.now().timestamp()
            if user_id not in self.requests:
                return self.max_requests

            # Limpiar antiguas
            self.requests[user_id] = [
                req_time for req_time in self.requests[user_id]
                if now - req_time < self.window_seconds
            ]
            return self.max_requests - len(self.requests[user_id])

    limiter = RateLimiter(max_requests=5, window_seconds=60)

    print("\n⏱️ Configuración:")
    print("   Max requests: 5")
    print("   Ventana: 60 segundos\n")

    # Simular múltiples requests
    usuario = "usuario_001"
    print(f"🔄 Simulando requests del usuario: {usuario}\n")

    for i in range(8):
        permitido = limiter.is_allowed(usuario)
        restantes = limiter.get_remaining(usuario)

        status = "✅ PERMITIDO" if permitido else "❌ RECHAZADO"
        print(f"   Request {i+1}: {status} - Restantes: {restantes}")

        if permitido:
            logger.info(f"Request {i+1} permitida para {usuario}")
        else:
            logger.warning(f"Request {i+1} rechazada por rate limit")


# ============================================================================
# EJEMPLO 4: Monitoreo y logging detallado
# ============================================================================

def ejemplo_4_monitoring():
    """Ejemplo 4: Sistema de monitoreo y logging"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Monitoreo y Logging")
    print("=" * 60)

    class APIMonitor:
        """Monitor para API Langflow"""
        def __init__(self):
            self.requests_total = 0
            self.requests_exitosas = 0
            self.requests_fallidas = 0
            self.tiempos_respuesta = []

        def registrar_request(self, exitosa: bool, tiempo_ms: float):
            """Registra una request"""
            self.requests_total += 1
            if exitosa:
                self.requests_exitosas += 1
            else:
                self.requests_fallidas += 1
            self.tiempos_respuesta.append(tiempo_ms)

        def obtener_metricas(self) -> dict:
            """Obtiene métricas del monitor"""
            if self.tiempos_respuesta:
                tiempo_promedio = sum(self.tiempos_respuesta) / len(self.tiempos_respuesta)
                tiempo_max = max(self.tiempos_respuesta)
                tiempo_min = min(self.tiempos_respuesta)
            else:
                tiempo_promedio = tiempo_max = tiempo_min = 0

            tasa_exito = (self.requests_exitosas / self.requests_total * 100) if self.requests_total > 0 else 0

            return {
                "total_requests": self.requests_total,
                "exitosas": self.requests_exitosas,
                "fallidas": self.requests_fallidas,
                "tasa_exito_pct": round(tasa_exito, 2),
                "tiempo_promedio_ms": round(tiempo_promedio, 2),
                "tiempo_max_ms": round(tiempo_max, 2),
                "tiempo_min_ms": round(tiempo_min, 2)
            }

    monitor = APIMonitor()

    print("\n📊 Simulando requests y monitoreando:\n")

    # Simular requests
    datos_simulados = [
        (True, 245),
        (True, 187),
        (False, 500),
        (True, 203),
        (True, 195),
        (False, 1200),
        (True, 156),
        (True, 289),
    ]

    for i, (exitosa, tiempo) in enumerate(datos_simulados, 1):
        monitor.registrar_request(exitosa, tiempo)
        status = "✅" if exitosa else "❌"
        print(f"   Request {i}: {status} - {tiempo}ms")

    # Mostrar métricas
    print("\n📈 Métricas finales:")
    metricas = monitor.obtener_metricas()

    for clave, valor in metricas.items():
        print(f"   {clave}: {valor}")

    logger.info(f"Monitoreo completado - {metricas['total_requests']} requests procesadas")


# ============================================================================
# EJEMPLO 5: Configuración de producción
# ============================================================================

def ejemplo_5_config_produccion():
    """Ejemplo 5: Configuración para producción"""
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Configuración de Producción")
    print("=" * 60)

    class ConfigProduccion:
        """Configuración para despliegue en producción"""

        def __init__(self):
            # Configuración de servidor
            self.HOST = "0.0.0.0"
            self.PORT = 8000
            self.WORKERS = 4
            self.TIMEOUT = 60

            # Configuración de LLM
            self.LLM_MODEL = "mistral"
            self.LLM_BASE_URL = "http://localhost:11434"
            self.LLM_TIMEOUT = 30

            # Seguridad
            self.ENABLE_CORS = True
            self.CORS_ORIGINS = ["*"]
            self.SECRET_KEY = "your-secret-key-change-in-prod"

            # Base de datos
            self.DB_URL = "postgresql://user:pass@localhost/langflow_db"

            # Monitoreo
            self.ENABLE_METRICS = True
            self.LOG_LEVEL = "INFO"
            self.LOG_FILE = "/var/log/langflow-api.log"

        def obtener_configuracion(self):
            """Retorna configuración como diccionario"""
            return {
                "servidor": {
                    "host": self.HOST,
                    "port": self.PORT,
                    "workers": self.WORKERS,
                    "timeout": self.TIMEOUT
                },
                "llm": {
                    "modelo": self.LLM_MODEL,
                    "url": self.LLM_BASE_URL,
                    "timeout": self.LLM_TIMEOUT
                },
                "seguridad": {
                    "cors_habilitado": self.ENABLE_CORS,
                    "log_level": self.LOG_LEVEL
                },
                "base_datos": {
                    "url": self.DB_URL
                },
                "monitoreo": {
                    "metricas_habilitadas": self.ENABLE_METRICS,
                    "archivo_log": self.LOG_FILE
                }
            }

    config = ConfigProduccion()

    print("\n⚙️  Configuración para Producción:\n")

    config_dict = config.obtener_configuracion()

    for seccion, valores in config_dict.items():
        print(f"   📦 {seccion.upper()}:")
        for clave, valor in valores.items():
            print(f"      {clave}: {valor}")

    # Guardar configuración
    config_json = json.dumps(config_dict, indent=2, ensure_ascii=False)
    print(f"\n   ✅ Configuración generada")
    logger.info("Configuración de producción lista para despliegue")


def main():
    """Función principal"""
    try:
        ejemplo_1_api_simple()
        ejemplo_2_autenticacion()
        ejemplo_3_rate_limiting()
        ejemplo_4_monitoring()
        ejemplo_5_config_produccion()

        print("\n" + "=" * 60)
        print("✅ Todos los ejemplos de exportación completados")
        print("=" * 60)

    except Exception as e:
        logger.critical(f"Error fatal: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
