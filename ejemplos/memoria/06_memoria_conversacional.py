"""
06_MEMORIA_CONVERSACIONAL.PY
=============================

Ejemplo didáctico: Memoria en Agentes Conversacionales

Demuestra:
- Historial de conversación con contexto acumulativo
- Seguimiento de entidades (Named Entity Recognition básico)
- Resolución de referencias anafóricas (pronombres)
- Personalización basada en memoria
- Privacidad y sensibilidad de datos

REQUISITOS PREVIOS:
- pip install langchain ollama
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple
from enum import Enum
from datetime import datetime
import re


# ============================================================================
# TIPOS Y ESTRUCTURAS
# ============================================================================

class RolMensaje(Enum):
    """Rol del remitente del mensaje"""
    USUARIO = "usuario"
    ASISTENTE = "asistente"
    SISTEMA = "sistema"


class TipoEntidad(Enum):
    """Tipos de entidades reconocidas"""
    PERSONA = "persona"
    ORGANIZACION = "organizacion"
    PRODUCTO = "producto"
    UBICACION = "ubicacion"
    NUMERO = "numero"
    FECHA = "fecha"
    EMAIL = "email"
    TELEFONO = "telefono"
    DESCONOCIDO = "desconocido"


@dataclass
class Entidad:
    """Representa una entidad reconocida"""
    valor: str
    tipo: TipoEntidad
    mencionada_en_turno: int  # en qué turno fue mencionada
    cantidad_menciones: int = 1
    propiedades: Dict = field(default_factory=dict)

    def marcar_como_sensible(self) -> None:
        """Marca la entidad como sensible (PII)"""
        self.propiedades["sensible"] = True

    def es_sensible(self) -> bool:
        """Revisa si es dato sensible"""
        return self.propiedades.get("sensible", False)


@dataclass
class Mensaje:
    """Representa un mensaje en la conversación"""
    id: str
    rol: RolMensaje
    contenido: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    turno: int = 0
    entidades: List[Entidad] = field(default_factory=list)
    referencias_resueltas: Dict[str, str] = field(default_factory=dict)


# ============================================================================
# SEGUIMIENTO DE ENTIDADES
# ============================================================================

class SeguimientoEntidades:
    """
    Rastrea entidades mencionadas en la conversación.
    Implementa Named Entity Recognition (NER) básica.
    """

    # Patrones simples para reconocimiento
    PATRONES = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "telefono": r"\+?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}",
        "numero": r"\b\d+(?:,\d{3})*(?:\.\d+)?\b",
        "fecha": r"\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}",
    }

    PALABRAS_CLAVE_PRODUCTOS = {
        "laptop", "computadora", "tablet", "monitor", "teclado",
        "mouse", "auriculares", "impresora", "webcam"
    }

    def __init__(self):
        self.entidades: Dict[str, Entidad] = {}
        self.coreferences: Dict[str, List[str]] = {}  # pronombre -> entidades
        self.historial_menciones: List[Tuple[int, str, str]] = []  # (turno, entidad, tipo)

    def extraer_entidades(self, texto: str, turno: int) -> List[Entidad]:
        """Extrae entidades del texto"""
        entidades = []

        # Buscar patrones de correo
        for match in re.finditer(self.PATRONES["email"], texto):
            entidad = Entidad(
                valor=match.group(),
                tipo=TipoEntidad.EMAIL,
                mencionada_en_turno=turno
            )
            entidad.marcar_como_sensible()
            entidades.append(entidad)

        # Buscar patrones de teléfono
        for match in re.finditer(self.PATRONES["telefono"], texto):
            entidad = Entidad(
                valor=match.group(),
                tipo=TipoEntidad.TELEFONO,
                mencionada_en_turno=turno
            )
            entidad.marcar_como_sensible()
            entidades.append(entidad)

        # Buscar productos
        palabras = texto.lower().split()
        for palabra in palabras:
            palabra_limpia = palabra.rstrip(".,!?;")
            if palabra_limpia in self.PALABRAS_CLAVE_PRODUCTOS:
                entidad = Entidad(
                    valor=palabra,
                    tipo=TipoEntidad.PRODUCTO,
                    mencionada_en_turno=turno
                )
                entidades.append(entidad)

        # Buscar números
        for match in re.finditer(self.PATRONES["numero"], texto):
            valor = match.group()
            # Evitar duplicados con otros tipos
            if not any(e.valor == valor for e in entidades):
                entidades.append(Entidad(
                    valor=valor,
                    tipo=TipoEntidad.NUMERO,
                    mencionada_en_turno=turno
                ))

        return entidades

    def actualizar_seguimiento(self, entidades: List[Entidad]) -> None:
        """Actualiza seguimiento de entidades"""
        for entidad in entidades:
            if entidad.valor in self.entidades:
                # Incrementar menciones
                self.entidades[entidad.valor].cantidad_menciones += 1
            else:
                # Registrar nueva entidad
                self.entidades[entidad.valor] = entidad

            # Historial
            self.historial_menciones.append(
                (entidad.mencionada_en_turno, entidad.valor, entidad.tipo.value)
            )

    def resolver_coreference(
        self,
        pronombre: str,
        turno_actual: int
    ) -> Optional[str]:
        """
        Resuelve referencias anafóricas (pronombres).
        Busca la entidad mencionada más recientemente del tipo correcto.
        """
        # Mapeo simplificado pronombre -> tipo
        tipo_esperado = None

        if pronombre in ["él", "su"]:
            # Probablemente persona masculina
            tipo_esperado = TipoEntidad.PERSONA
        elif pronombre in ["ella"]:
            tipo_esperado = TipoEntidad.PERSONA
        elif pronombre in ["lo", "los"]:
            # Objeto (producto, etc)
            tipo_esperado = TipoEntidad.PRODUCTO
        elif pronombre in ["la", "las"]:
            tipo_esperado = TipoEntidad.PRODUCTO

        # Buscar entidad más recientemente mencionada
        if tipo_esperado:
            menciones_recientes = [
                (turno, valor)
                for turno, valor, tipo in sorted(
                    self.historial_menciones,
                    reverse=True
                )
                if tipo == tipo_esperado.value
            ]

            if menciones_recientes:
                return menciones_recientes[0][1]

        return None

    def obtener_resumen(self) -> Dict:
        """Resumen de entidades rastreadas"""
        entidades_sensibles = {
            valor: info.tipo.value
            for valor, info in self.entidades.items()
            if info.es_sensible()
        }

        entidades_normales = {
            valor: info.tipo.value
            for valor, info in self.entidades.items()
            if not info.es_sensible()
        }

        return {
            "entidades_normales": entidades_normales,
            "entidades_sensibles": len(entidades_sensibles),
            "total_entidades": len(self.entidades),
            "menciones_totales": len(self.historial_menciones)
        }


# ============================================================================
# HISTORIAL DE CONVERSACIÓN
# ============================================================================

class HistorialConversacion:
    """
    Mantiene el historial de una conversación con contexto acumulativo.
    Sigue referencias anafóricas y resuelve entidades.
    """

    def __init__(self, usuario_id: str):
        self.usuario_id = usuario_id
        self.mensajes: List[Mensaje] = []
        self.seguimiento = SeguimientoEntidades()
        self.contador_turnos = 0
        self.contexto_personalizado: Dict = {}  # preferencias del usuario

    def agregar_mensaje(
        self,
        rol: RolMensaje,
        contenido: str
    ) -> Mensaje:
        """Agrega mensaje al historial"""
        self.contador_turnos += 1

        # Extraer entidades
        entidades = self.seguimiento.extraer_entidades(contenido, self.contador_turnos)
        self.seguimiento.actualizar_seguimiento(entidades)

        # Crear mensaje
        mensaje = Mensaje(
            id=f"msg_{self.usuario_id}_{self.contador_turnos}",
            rol=rol,
            contenido=contenido,
            turno=self.contador_turnos,
            entidades=entidades
        )

        # Resolver referencias anafóricas
        self._resolver_referencias(mensaje)

        self.mensajes.append(mensaje)
        return mensaje

    def _resolver_referencias(self, mensaje: Mensaje) -> None:
        """Resuelve pronombres y referencias en el mensaje"""
        # Palabras que típicamente referencia
        pronombres = ["él", "ella", "lo", "la", "los", "las", "su", "sus"]

        palabras = mensaje.contenido.split()
        for palabra_limpia in palabras:
            palabra = palabra_limpia.rstrip(".,!?;").lower()
            if palabra in pronombres:
                referente = self.seguimiento.resolver_coreference(
                    palabra,
                    mensaje.turno
                )
                if referente:
                    mensaje.referencias_resueltas[palabra] = referente

    def obtener_contexto_conversacional(
        self,
        ultimos_n: int = 5,
        incluir_sensibles: bool = False
    ) -> str:
        """
        Obtiene el contexto de los últimos N turnos para pasar al LLM.
        Opcionalmente filtra datos sensibles.
        """
        lineas = []

        # Tomar últimos N mensajes
        mensajes_recientes = self.mensajes[-ultimos_n:]

        for mensaje in mensajes_recientes:
            # Filtrar datos sensibles si se solicita
            contenido = mensaje.contenido

            if not incluir_sensibles:
                for entidad in mensaje.entidades:
                    if entidad.es_sensible():
                        # Reemplazar con placeholder
                        contenido = contenido.replace(
                            entidad.valor,
                            f"[{entidad.tipo.value.upper()}]"
                        )

            lineas.append(f"{mensaje.rol.value.upper()}: {contenido}")

        return "\n".join(lineas)

    def obtener_personalidad_usuario(self) -> Dict:
        """Extrae preferencias y características del usuario"""
        # Análisis simple: contar tipos de preguntas
        preguntas_precio = sum(
            1 for m in self.mensajes
            if m.rol == RolMensaje.USUARIO and "precio" in m.contenido.lower()
        )
        preguntas_tecnicas = sum(
            1 for m in self.mensajes
            if m.rol == RolMensaje.USUARIO and any(
                palabra in m.contenido.lower()
                for palabra in ["especificación", "técnico", "rendimiento"]
            )
        )

        return {
            "interes_precios": preguntas_precio > 0,
            "interes_tecnico": preguntas_tecnicas > 0,
            "numero_turnos": self.contador_turnos,
            "entidades_mencionadas": len(self.seguimiento.entidades)
        }

    def limpiar_datos_sensibles(self) -> int:
        """Elimina datos sensibles (GDPR compliance)"""
        cantidad_limpiada = 0

        for mensaje in self.mensajes:
            for entidad in mensaje.entidades:
                if entidad.es_sensible():
                    mensaje.contenido = mensaje.contenido.replace(
                        entidad.valor,
                        "[REDACTADO]"
                    )
                    cantidad_limpiada += 1

        return cantidad_limpiada

    def obtener_resumen(self) -> Dict:
        """Resumen de la conversación"""
        return {
            "usuario": self.usuario_id,
            "total_mensajes": len(self.mensajes),
            "turnos": self.contador_turnos,
            "ultimos_mensajes": [
                {"rol": m.rol.value, "contenido": m.contenido[:50] + "..."}
                for m in self.mensajes[-3:]
            ],
            "entidades": self.seguimiento.obtener_resumen(),
            "personalidad": self.obtener_personalidad_usuario()
        }


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demo_memoria_conversacional():
    """Demuestra memoria en agentes conversacionales"""

    print("=" * 80)
    print("DEMOSTRACIÓN: MEMORIA EN AGENTES CONVERSACIONALES")
    print("=" * 80)

    # Crear historial
    usuario = "usuario_001"
    historial = HistorialConversacion(usuario)

    print("\n1. CONVERSACIÓN CON SEGUIMIENTO DE ENTIDADES")
    print("-" * 80)

    # Simular conversación
    turnos = [
        ("usuario", "Hola, me interesa una laptop para desarrollo con Python."),
        ("asistente", "Entendido. ¿Qué tipo de laptop buscas? ¿Gaming o productividad?"),
        ("usuario", "Productividad principalmente. Mi email es usuario@example.com"),
        ("asistente", "Perfecto. Para desarrollo recomiendo MacBook Pro o ThinkPad."),
        ("usuario", "¿Cuál es el precio del MacBook? ¿Cómo puedo comprarlo?"),
        ("asistente", "El MacBook Pro está alrededor de $3000-4000. Puedo darte info."),
    ]

    for rol_str, contenido in turnos:
        rol = RolMensaje(rol_str)
        mensaje = historial.agregar_mensaje(rol, contenido)

        print(f"\n[Turno {mensaje.turno}] {rol.value.upper()}")
        print(f"  {contenido}")

        if mensaje.entidades:
            print(f"  Entidades detectadas:")
            for entidad in mensaje.entidades:
                sensibilidad = " (SENSIBLE)" if entidad.es_sensible() else ""
                print(f"    - {entidad.valor} [{entidad.tipo.value}]{sensibilidad}")

        if mensaje.referencias_resueltas:
            print(f"  Referencias resueltas:")
            for pronombre, referente in mensaje.referencias_resueltas.items():
                print(f"    '{pronombre}' -> '{referente}'")

    # Contexto conversacional
    print("\n2. CONTEXTO CONVERSACIONAL PARA LLM")
    print("-" * 80)
    contexto = historial.obtener_contexto_conversacional(
        ultimos_n=3,
        incluir_sensibles=False
    )
    print("Contexto filtrado (sin datos sensibles):")
    print(contexto)

    # Entidades rastreadas
    print("\n3. RESUMEN DE ENTIDADES RASTREADAS")
    print("-" * 80)
    resumen_entidades = historial.seguimiento.obtener_resumen()
    for clave, valor in resumen_entidades.items():
        print(f"  {clave}: {valor}")

    # Personalización
    print("\n4. ANÁLISIS DE PERSONALIDAD DEL USUARIO")
    print("-" * 80)
    personalidad = historial.obtener_personalidad_usuario()
    for clave, valor in personalidad.items():
        print(f"  {clave}: {valor}")

    # Privacidad
    print("\n5. CUMPLIMIENTO DE PRIVACIDAD (GDPR)")
    print("-" * 80)
    print("Antes de limpiar:")
    entidades_sensibles = historial.seguimiento.obtener_resumen()
    print(f"  Entidades sensibles: {entidades_sensibles['entidades_sensibles']}")

    cantidad_limpiada = historial.limpiar_datos_sensibles()
    print(f"\nDatos sensibles eliminados: {cantidad_limpiada}")

    print("Después de limpiar (email redactado):")
    contexto_limpio = historial.obtener_contexto_conversacional(ultimos_n=2)
    print(contexto_limpio)

    # Resumen final
    print("\n6. RESUMEN DE CONVERSACIÓN")
    print("-" * 80)
    resumen_final = historial.obtener_resumen()
    for clave, valor in resumen_final.items():
        if isinstance(valor, dict):
            print(f"  {clave}:")
            for k, v in valor.items():
                print(f"    {k}: {v}")
        elif isinstance(valor, list):
            print(f"  {clave}:")
            for item in valor:
                print(f"    {item}")
        else:
            print(f"  {clave}: {valor}")

    # Información de integración
    print("\n7. INTEGRACIÓN CON OLLAMA + LANGCHAIN")
    print("-" * 80)
    print("""
Para usar en producción con Ollama:

from langchain.llms import Ollama
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain

ollama = Ollama(model="mistral")
memory = ConversationBufferWindowMemory(k=3)

chain = ConversationChain(
    llm=ollama,
    memory=memory,
    verbose=True
)

response = chain.run(input="Tu pregunta aquí")
    """)

    print("\n" + "=" * 80)
    print("Conclusión: Memoria conversacional permite:")
    print("- Mantener coherencia en diálogos largos")
    print("- Resolver referencias anafóricas")
    print("- Personalizar respuestas")
    print("- Cumplir regulaciones de privacidad")
    print("=" * 80)


if __name__ == "__main__":
    demo_memoria_conversacional()
