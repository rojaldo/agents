"""
Ejemplo 2: Cliente MCP con LangChain

Este ejemplo demuestra cómo crear un cliente MCP que se conecta
a un servidor y utiliza sus herramientas de manera interactiva.
"""

import json
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime


class ClienteMCPLangChain:
    """
    Cliente MCP que se conecta a un servidor y utiliza sus herramientas.
    """

    def __init__(self, nombre_cliente: str = "Cliente MCP"):
        """
        Inicializa el cliente MCP.

        Args:
            nombre_cliente: Nombre identificador del cliente
        """
        self.nombre = nombre_cliente
        self.servidor = None
        self.conectado = False
        self.herramientas_disponibles = []
        self.historial_cliente = []
        print(f"✓ Cliente MCP '{nombre_cliente}' inicializado")

    async def conectar(self, servidor) -> bool:
        """
        Conecta el cliente a un servidor MCP.

        Args:
            servidor: Instancia del servidor MCP

        Returns:
            True si la conexión fue exitosa
        """
        try:
            self.servidor = servidor
            self.conectado = True

            # Descubrir capacidades del servidor
            info_servidor = self.servidor.obtener_info()
            self.herramientas_disponibles = info_servidor.get("herramientas", [])

            print(f"✓ Conectado a servidor: {info_servidor['nombre']}")
            print(f"  Versión: {info_servidor['version']}")
            print(f"  Modelo: {info_servidor['modelo']}")
            print(f"  Herramientas disponibles: {len(self.herramientas_disponibles)}")

            return True

        except Exception as e:
            print(f"✗ Error al conectar: {e}")
            self.conectado = False
            return False

    def desconectar(self):
        """Desconecta del servidor."""
        if self.conectado:
            self.servidor = None
            self.conectado = False
            print("✓ Desconectado del servidor")

    async def listar_herramientas(self) -> Optional[list]:
        """
        Lista las herramientas disponibles en el servidor.

        Returns:
            Lista de nombres de herramientas o None si no está conectado
        """
        if not self.conectado:
            print("✗ No conectado al servidor")
            return None

        print("\n📋 Herramientas disponibles:")
        for i, herramienta in enumerate(self.herramientas_disponibles, 1):
            print(f"  {i}. {herramienta}")

        return self.herramientas_disponibles

    async def invocar_herramienta(
        self,
        nombre: str,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Invoca una herramienta del servidor.

        Args:
            nombre: Nombre de la herramienta a invocar
            **kwargs: Argumentos para la herramienta

        Returns:
            Resultado de la herramienta o None si hay error
        """
        if not self.conectado:
            print("✗ No conectado al servidor")
            return None

        if nombre not in self.herramientas_disponibles:
            print(f"✗ Herramienta '{nombre}' no disponible")
            return None

        try:
            # Obtener la herramienta del servidor
            herramienta = self.servidor.herramientas[nombre]

            # Invocar la herramienta
            print(f"\n⚙️  Invocando herramienta: {nombre}")
            resultado = herramienta(**kwargs)

            # Registrar en historial del cliente
            self.historial_cliente.append({
                "herramienta": nombre,
                "argumentos": kwargs,
                "resultado": resultado,
                "timestamp": datetime.now().isoformat()
            })

            return resultado

        except Exception as e:
            print(f"✗ Error al invocar herramienta: {e}")
            return None

    async def flujo_generacion_contenido(self, tema: str) -> Dict[str, Any]:
        """
        Flujo completo: generar contenido y analizarlo.

        Args:
            tema: Tema sobre el cual generar contenido

        Returns:
            Diccionario con los resultados del flujo
        """
        print(f"\n{'='*60}")
        print(f"🔄 Iniciando flujo de generación de contenido sobre: {tema}")
        print("="*60)

        resultados = {}

        # Paso 1: Generar texto
        print("\n1️⃣  Generando texto...")
        texto_generado = await self.invocar_herramienta(
            "generar_texto",
            prompt=f"Escribe un párrafo informativo sobre {tema}"
        )

        if texto_generado and "texto_generado" in texto_generado:
            resultados["texto_original"] = texto_generado["texto_generado"]
            print(f"   ✓ Texto generado ({len(resultados['texto_original'])} caracteres)")

            # Paso 2: Resumir el texto
            print("\n2️⃣  Resumiendo texto...")
            resumen = await self.invocar_herramienta(
                "resumir_texto",
                texto=resultados["texto_original"]
            )

            if resumen and "resumen" in resumen:
                resultados["resumen"] = resumen["resumen"]
                print(f"   ✓ Resumen creado ({len(resultados['resumen'])} caracteres)")

            # Paso 3: Analizar sentimiento
            print("\n3️⃣  Analizando sentimiento...")
            sentimiento = await self.invocar_herramienta(
                "analizar_sentimiento",
                texto=resultados["texto_original"]
            )

            if sentimiento and "sentimiento" in sentimiento:
                resultados["sentimiento"] = sentimiento["sentimiento"]
                print(f"   ✓ Sentimiento detectado: {resultados['sentimiento']}")

        return resultados

    async def flujo_qa_interactivo(self, preguntas: list, contexto: str = "") -> list:
        """
        Flujo de preguntas y respuestas interactivo.

        Args:
            preguntas: Lista de preguntas a responder
            contexto: Contexto para las respuestas

        Returns:
            Lista de diccionarios con preguntas y respuestas
        """
        print(f"\n{'='*60}")
        print("❓ Iniciando flujo de Q&A")
        print("="*60)

        if contexto:
            print(f"\n📖 Contexto proporcionado:")
            print(f"   {contexto[:100]}...")

        resultados = []

        for i, pregunta in enumerate(preguntas, 1):
            print(f"\n{i}. Pregunta: {pregunta}")

            respuesta = await self.invocar_herramienta(
                "responder_pregunta",
                pregunta=pregunta,
                contexto=contexto
            )

            if respuesta and "respuesta" in respuesta:
                print(f"   Respuesta: {respuesta['respuesta'][:100]}...")
                resultados.append({
                    "pregunta": pregunta,
                    "respuesta": respuesta["respuesta"]
                })

        return resultados

    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de uso del cliente.

        Returns:
            Diccionario con estadísticas
        """
        if not self.historial_cliente:
            return {"total_operaciones": 0}

        herramientas_usadas = {}
        for item in self.historial_cliente:
            herramienta = item["herramienta"]
            herramientas_usadas[herramienta] = herramientas_usadas.get(herramienta, 0) + 1

        return {
            "total_operaciones": len(self.historial_cliente),
            "herramientas_usadas": herramientas_usadas,
            "primera_operacion": self.historial_cliente[0]["timestamp"],
            "ultima_operacion": self.historial_cliente[-1]["timestamp"]
        }

    def mostrar_historial(self):
        """Muestra el historial de operaciones del cliente."""
        print(f"\n{'='*60}")
        print("📊 Historial de operaciones del cliente")
        print("="*60)

        if not self.historial_cliente:
            print("No hay operaciones registradas")
            return

        for i, item in enumerate(self.historial_cliente, 1):
            print(f"\n{i}. {item['herramienta']} - {item['timestamp']}")
            print(f"   Argumentos: {list(item['argumentos'].keys())}")


# Ejemplo de uso
async def main():
    from servidor_basico_langchain import ServidorMCPLangChain

    print("=" * 60)
    print("Cliente MCP con LangChain y Ollama")
    print("=" * 60)

    # Crear servidor
    servidor = ServidorMCPLangChain(modelo="llama3.2")

    # Crear cliente
    cliente = ClienteMCPLangChain("Cliente Demo")

    # Conectar al servidor
    await cliente.conectar(servidor)

    # Listar herramientas disponibles
    await cliente.listar_herramientas()

    # Ejemplo 1: Flujo de generación de contenido
    resultados_flujo = await cliente.flujo_generacion_contenido(
        "las energías renovables"
    )

    print(f"\n{'='*60}")
    print("📋 Resultados del flujo")
    print("="*60)
    print(json.dumps(resultados_flujo, indent=2, ensure_ascii=False))

    # Ejemplo 2: Flujo de Q&A
    contexto_qa = """
    LangChain es un framework de código abierto diseñado para facilitar la creación
    de aplicaciones con modelos de lenguaje grandes (LLMs). Proporciona herramientas
    para encadenar diferentes componentes, gestionar prompts y conectar con diversas
    fuentes de datos.
    """

    preguntas = [
        "¿Qué es LangChain?",
        "¿Para qué se usa LangChain?",
        "¿Qué ventajas ofrece?"
    ]

    resultados_qa = await cliente.flujo_qa_interactivo(preguntas, contexto_qa)

    # Mostrar estadísticas
    print(f"\n{'='*60}")
    print("📊 Estadísticas del cliente")
    print("="*60)
    stats = cliente.obtener_estadisticas()
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    # Mostrar historial
    cliente.mostrar_historial()

    # Desconectar
    cliente.desconectar()


if __name__ == "__main__":
    asyncio.run(main())
