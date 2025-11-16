"""
MÓDULO 2: Comunicación Entre Agentes
Ejemplo 1: Comunicación Básica Síncrona y Asíncrona

Demuestra diferentes paradigmas de comunicación:
- Síncrona (bloqueante): Emisor espera respuesta
- Asíncrona (no-bloqueante): Emisor continúa sin esperar
- Request-Reply: Modelo cliente-servidor
- Publish-Subscribe: Desacoplamiento total
"""

import sys
sys.path.insert(0, '../utilidades')

from agent_base import Agent
from ollama_client import OllamaClient
from typing import Any, List, Callable, Optional
from collections import defaultdict
from datetime import datetime
import time
import json


class MessageBroker:
    """
    Corredor de mensajes (Message Broker) simple.
    Intermediario para comunicación entre agentes.
    """

    def __init__(self):
        """Inicializa el broker de mensajes"""
        self.messages_queue = []  # Cola de mensajes
        self.subscribers = defaultdict(list)  # Suscriptores por tópico
        self.message_log = []  # Log de todos los mensajes

    def enviar_sincrono(self, sender: str, recipient: str, content: str) -> dict:
        """
        Envío síncrono (bloqueante)
        El emisor espera una respuesta inmediata
        """
        message = {
            "id": len(self.message_log),
            "timestamp": datetime.now().isoformat(),
            "type": "sync",
            "sender": sender,
            "recipient": recipient,
            "content": content,
            "status": "entregado"
        }
        self.message_log.append(message)
        print(f"  [{datetime.now().strftime('%H:%M:%S')}] SINC: {sender} → {recipient}")
        print(f"    Mensaje: {content}")
        return message

    def enviar_asincrono(self, sender: str, recipient: str, content: str):
        """
        Envío asíncrono (no-bloqueante)
        El emisor continúa sin esperar respuesta
        """
        message = {
            "id": len(self.message_log),
            "timestamp": datetime.now().isoformat(),
            "type": "async",
            "sender": sender,
            "recipient": recipient,
            "content": content,
            "status": "en_cola"
        }
        self.messages_queue.append(message)
        self.message_log.append(message)
        print(f"  [{datetime.now().strftime('%H:%M:%S')}] ASINC: {sender} → {recipient} (en cola)")

    def publicar(self, publisher: str, topico: str, contenido: str):
        """
        Publicación en tópico (Publish-Subscribe)
        Todos los suscritos reciben automáticamente
        """
        message = {
            "id": len(self.message_log),
            "timestamp": datetime.now().isoformat(),
            "type": "publish_subscribe",
            "publisher": publisher,
            "topico": topico,
            "contenido": contenido,
            "suscritos": len(self.subscribers[topico])
        }
        self.message_log.append(message)

        print(f"  [{datetime.now().strftime('%H:%M:%S')}] PUBL-SUB: {publisher} → [{topico}]")
        print(f"    Mensaje: {contenido}")
        print(f"    Entregado a {len(self.subscribers[topico])} suscriptores")

        # Entregar a todos los suscritos
        for callback in self.subscribers[topico]:
            callback(publisher, topico, contenido)

    def suscribirse(self, agente_name: str, topico: str, callback: Callable):
        """Un agente se suscribe a un tópico"""
        self.subscribers[topico].append(callback)
        print(f"  ✓ {agente_name} suscrito a [{topico}]")

    def procesar_cola(self, max_mensajes: int = 5):
        """
        Procesa mensajes de la cola asíncrona
        """
        procesados = 0
        while self.messages_queue and procesados < max_mensajes:
            mensaje = self.messages_queue.pop(0)
            mensaje["status"] = "procesado"
            procesados += 1
            print(f"  Procesando cola: {mensaje['sender']} → {mensaje['recipient']}")
            time.sleep(0.1)  # Simular procesamiento

    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas del broker"""
        total_msgs = len(self.message_log)
        sincronos = sum(1 for m in self.message_log if m.get("type") == "sync")
        asincronos = sum(1 for m in self.message_log if m.get("type") == "async")
        pubsub = sum(1 for m in self.message_log if m.get("type") == "publish_subscribe")

        return {
            "total_mensajes": total_msgs,
            "sincronos": sincronos,
            "asincronos": asincronos,
            "publish_subscribe": pubsub,
            "cola_pendiente": len(self.messages_queue),
            "suscripciones_activas": sum(len(v) for v in self.subscribers.values())
        }


class AgenteConComunicacion(Agent):
    """Agente que sabe comunicarse con otros agentes"""

    def __init__(self, name: str, broker: MessageBroker):
        super().__init__(name=name, role="communicative")
        self.model = OllamaClient(model="mistral")
        self.broker = broker
        self.objective = "Comunicarse efectivamente"
        self.received_messages = []

    def enviar_mensaje_sincrono(self, recipient: str, contenido: str) -> dict:
        """Envía mensaje y espera respuesta (síncrono)"""
        return self.broker.enviar_sincrono(self.name, recipient, contenido)

    def enviar_mensaje_asincrono(self, recipient: str, contenido: str):
        """Envía mensaje sin esperar respuesta (asíncrono)"""
        self.broker.enviar_asincrono(self.name, recipient, contenido)

    def publicar_mensaje(self, topico: str, contenido: str):
        """Publica mensaje en un tópico"""
        self.broker.publicar(self.name, topico, contenido)

    def suscribirse_topico(self, topico: str):
        """Se suscribe a un tópico para recibir mensajes"""
        def callback(publisher, topic, content):
            msg = {
                "timestamp": datetime.now().isoformat(),
                "publisher": publisher,
                "topico": topic,
                "content": content
            }
            self.received_messages.append(msg)
            print(f"    ✓ {self.name} recibió: {content[:50]}...")

        self.broker.suscribirse(self.name, topico, callback)

    def _execute_action(self, action: str) -> Any:
        return {"agente": self.name, "accion": action}


def demostrar_comunicacion_sincrona():
    """
    Comunicación Síncrona:
    - Emisor espera respuesta inmediata
    - Bloqueante: ambas partes deben estar listas
    - Baja latencia pero requiere sincronización
    """
    print("\n" + "=" * 70)
    print("COMUNICACIÓN SÍNCRONA (Bloqueante)")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("• El emisor espera respuesta antes de continuar")
    print("• Ambos agentes deben estar disponibles")
    print("• Ventaja: Confirmación inmediata")
    print("• Desventaja: Puede causar bloqueos")

    broker = MessageBroker()

    # Crear agentes
    agente_a = AgenteConComunicacion("Alice", broker)
    agente_b = AgenteConComunicacion("Bob", broker)

    print("\nSecuencia de comunicación síncrona:")
    print("─" * 50)

    # Diálogo síncrono (simulado)
    agente_a.enviar_mensaje_sincrono("Bob", "Hola Bob, ¿cómo estás?")
    time.sleep(0.5)
    agente_b.enviar_mensaje_sincrono("Alice", "Hola Alice, estoy bien! 😊")
    time.sleep(0.5)
    agente_a.enviar_mensaje_sincrono("Bob", "Excelente, nos vemos pronto")

    return broker


def demostrar_comunicacion_asincrona():
    """
    Comunicación Asíncrona:
    - Emisor NO espera respuesta
    - No-bloqueante: cada agente continúa su trabajo
    - Mensajes se encolan para procesamiento posterior
    """
    print("\n" + "=" * 70)
    print("COMUNICACIÓN ASÍNCRONA (No-bloqueante)")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("• El emisor NO espera respuesta")
    print("• Los mensajes se encolan")
    print("• Cada agente continúa trabajando")
    print("• Ventaja: Mayor rendimiento")
    print("• Desventaja: Menor garantía de entrega")

    broker = MessageBroker()

    agente_a = AgenteConComunicacion("Charlie", broker)
    agente_b = AgenteConComunicacion("Diana", broker)
    agente_c = AgenteConComunicacion("Eve", broker)

    print("\nEnvío asíncrono (agentes continúan trabajando):")
    print("─" * 50)

    # Envío asíncrono - múltiples mensajes rápidamente
    agente_a.enviar_mensaje_asincrono("Diana", "Tarea 1: Procesar datos")
    agente_a.enviar_mensaje_asincrono("Eve", "Tarea 2: Validar resultados")
    agente_b.enviar_mensaje_asincrono("Charlie", "Info: Base de datos actualizada")

    print("\nAhora los agentes continúan haciendo otras cosas...")
    print("(Mientras la cola procesa los mensajes)\n")

    # Procesar la cola
    broker.procesar_cola(max_mensajes=5)

    return broker


def demostrar_publish_subscribe():
    """
    Publish-Subscribe:
    - Productores publican en tópicos
    - Suscriptores reciben automáticamente
    - Desacoplamiento total entre productor y consumidor
    """
    print("\n" + "=" * 70)
    print("PUBLISH-SUBSCRIBE (Desacoplamiento total)")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("• Productores publican en tópicos sin conocer suscriptores")
    print("• Suscriptores reciben automáticamente")
    print("• Escalabilidad horizontal")
    print("• Ventaja: Máximo desacoplamiento")
    print("• Desventaja: Menos control directo")

    broker = MessageBroker()

    # Crear agentes
    sensor = AgenteConComunicacion("Sensor-Temperatura", broker)
    logger = AgenteConComunicacion("Logger-Sistema", broker)
    alertas = AgenteConComunicacion("Sistema-Alertas", broker)
    dashboard = AgenteConComunicacion("Dashboard", broker)

    print("\nSuscripciones:")
    print("─" * 50)

    # Suscribirse a tópicos
    logger.suscribirse_topico("sensores/temperatura")
    alertas.suscribirse_topico("sensores/temperatura")
    dashboard.suscribirse_topico("sensores/temperatura")

    print("\nPublicaciones del sensor:")
    print("─" * 50)

    # El sensor publica datos
    sensor.publicar_mensaje("sensores/temperatura", "Temperatura: 25°C")
    time.sleep(0.3)
    sensor.publicar_mensaje("sensores/temperatura", "Temperatura: 26°C")
    time.sleep(0.3)
    sensor.publicar_mensaje("sensores/temperatura", "Temperatura: 30°C - ¡ALERTA!")

    print(f"\n✓ 1 productor entregó a {len(broker.subscribers['sensores/temperatura'])} suscriptores")

    return broker


def comparar_paradigmas():
    """Compara los paradigmas de comunicación"""
    print("\n" + "=" * 70)
    print("COMPARACIÓN DE PARADIGMAS")
    print("=" * 70)

    comparacion = {
        "SÍNCRONA": {
            "Bloqueante": "✓ Sí",
            "Latencia": "Baja",
            "Escalabilidad": "Limitada",
            "Desacoplamiento": "Nulo",
            "Casos de uso": "RPC, consultas directas"
        },
        "ASÍNCRONA": {
            "Bloqueante": "✗ No",
            "Latencia": "Alta",
            "Escalabilidad": "Media",
            "Desacoplamiento": "Temporal",
            "Casos de uso": "Colas de trabajo, tareas en background"
        },
        "PUBLISH-SUBSCRIBE": {
            "Bloqueante": "✗ No",
            "Latencia": "Variable",
            "Escalabilidad": "Alta",
            "Desacoplamiento": "Total",
            "Casos de uso": "Event streaming, notificaciones, IoT"
        }
    }

    for paradigma, props in comparacion.items():
        print(f"\n{paradigma}:")
        for prop, valor in props.items():
            print(f"  {prop:20} {valor}")


def mostrar_estadisticas(brokers: dict):
    """Muestra estadísticas de todos los brokers"""
    print("\n" + "=" * 70)
    print("ESTADÍSTICAS DE COMUNICACIÓN")
    print("=" * 70)

    for nombre, broker in brokers.items():
        stats = broker.obtener_estadisticas()
        print(f"\n{nombre}:")
        for key, value in stats.items():
            print(f"  {key:25} {value}")


if __name__ == "__main__":
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║    COMUNICACIÓN ENTRE AGENTES                             ║")
    print("║                                                            ║")
    print("║  1. SÍNCRONA: Emisor espera respuesta                     ║")
    print("║  2. ASÍNCRONA: Mensajes en cola                           ║")
    print("║  3. PUBLISH-SUBSCRIBE: Desacoplamiento total              ║")
    print("╚════════════════════════════════════════════════════════════╝\n")

    try:
        brokers = {}

        # Demostrar paradigmas
        brokers["Síncrona"] = demostrar_comunicacion_sincrona()
        brokers["Asíncrona"] = demostrar_comunicacion_asincrona()
        brokers["Publish-Subscribe"] = demostrar_publish_subscribe()

        # Comparar
        comparar_paradigmas()

        # Mostrar estadísticas
        mostrar_estadisticas(brokers)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
