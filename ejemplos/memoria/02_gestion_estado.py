"""
02_GESTION_ESTADO.PY
====================

Ejemplo didáctico: Gestión de Estado en Agentes

Demuestra cómo un agente mantiene, persiste y recupera su estado:

- Representación de estado (identidad, posición, recursos, objetivos, creencias)
- Estado local vs compartido
- Persistencia y recuperación
- Serialización y versionado
- Historial con Event Sourcing

REQUISITOS PREVIOS:
- pip install langchain ollama pydantic pydantic-settings
"""

import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
import hashlib


# ============================================================================
# ENUMS Y TIPOS
# ============================================================================

class EstadoAgente(Enum):
    """Estados posibles del agente"""
    OCIOSO = "ocioso"
    PROCESANDO = "procesando"
    EJECUTANDO_TAREA = "ejecutando_tarea"
    EN_ERROR = "en_error"


class TipoEvento(Enum):
    """Tipos de eventos para event sourcing"""
    AGENTE_CREADO = "agente_creado"
    ESTADO_CAMBIADO = "estado_cambiado"
    TAREA_ASIGNADA = "tarea_asignada"
    TAREA_COMPLETADA = "tarea_completada"
    RECURSO_AGREGADO = "recurso_agregado"
    CREENCIA_ACTUALIZADA = "creencia_actualizada"
    RELACION_ESTABLECIDA = "relacion_establecida"


# ============================================================================
# ESTRUCTURAS DE ESTADO
# ============================================================================

@dataclass
class Identidad:
    """Identidad del agente"""
    id: str
    nombre: str
    tipo: str  # "supervisor", "trabajador", "coordinador", etc.
    version: str = "1.0"
    creado_en: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Posicion:
    """Ubicación del agente en el ambiente"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    zona: str = "zona_inicial"

    def distancia_a(self, otra: "Posicion") -> float:
        """Calcula distancia euclidiana"""
        return ((self.x - otra.x)**2 + (self.y - otra.y)**2 + (self.z - otra.z)**2) ** 0.5


@dataclass
class Recurso:
    """Representa un recurso que posee el agente"""
    nombre: str
    cantidad: float = 1.0
    unidad: str = "unidades"
    criticidad: float = 0.5  # 0.0 a 1.0


@dataclass
class Objetivo:
    """Objetivo del agente"""
    id: str
    descripcion: str
    prioridad: float = 0.5  # 0.0 a 1.0
    completado: bool = False
    progreso: float = 0.0  # 0.0 a 1.0


@dataclass
class Creencia:
    """Creencia del agente sobre el mundo"""
    contenido: str
    confianza: float = 0.5  # 0.0 a 1.0
    fuente: str = "inferencia"  # "sensor", "otro_agente", "inferencia", "aprendizaje"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Relacion:
    """Relación con otro agente"""
    agente_id: str
    tipo: str  # "aliado", "rival", "neutral", "supervisor", "subordinado"
    confianza: float = 0.5
    interacciones: int = 0


# ============================================================================
# EVENTO PARA EVENT SOURCING
# ============================================================================

@dataclass
class Evento:
    """Representa un evento en la historia del agente"""
    id: str
    tipo: TipoEvento
    timestamp: str
    datos: Dict[str, Any]
    secuencia: int = 0  # número secuencial

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "tipo": self.tipo.value,
            "timestamp": self.timestamp,
            "datos": self.datos,
            "secuencia": self.secuencia
        }


# ============================================================================
# ESTADO DEL AGENTE
# ============================================================================

class EstadoAgenteLLM:
    """
    Mantiene el estado completo de un agente que interactúa con LLM.
    Incluye identidad, posición, recursos, objetivos, creencias y relaciones.
    """

    def __init__(self, identidad: Identidad):
        self.identidad = identidad
        self.estado_actual = EstadoAgente.OCIOSO
        self.posicion = Posicion()
        self.recursos: Dict[str, Recurso] = {}
        self.objetivos: Dict[str, Objetivo] = {}
        self.creencias: List[Creencia] = []
        self.relaciones: Dict[str, Relacion] = {}

        # Event sourcing
        self.eventos: List[Evento] = []
        self.secuencia_evento = 0

        # Historial
        self.historial_cambios: List[Dict] = []

        # Timestamp de creación
        self.timestamp_creacion = datetime.now()
        self.timestamp_ultimo_cambio = datetime.now()

        # Registrar creación
        self._registrar_evento(
            TipoEvento.AGENTE_CREADO,
            {"identidad": asdict(identidad)}
        )

    def cambiar_estado(self, nuevo_estado: EstadoAgente) -> None:
        """Cambia el estado del agente"""
        estado_anterior = self.estado_actual
        self.estado_actual = nuevo_estado
        self._registrar_evento(
            TipoEvento.ESTADO_CAMBIADO,
            {
                "anterior": estado_anterior.value,
                "nuevo": nuevo_estado.value
            }
        )

    def agregar_recurso(self, recurso: Recurso) -> None:
        """Agrega un recurso al agente"""
        self.recursos[recurso.nombre] = recurso
        self._registrar_evento(
            TipoEvento.RECURSO_AGREGADO,
            {"recurso": asdict(recurso)}
        )

    def consumir_recurso(self, nombre: str, cantidad: float) -> bool:
        """Consume una cantidad de recurso, retorna éxito"""
        if nombre not in self.recursos:
            return False

        recurso = self.recursos[nombre]
        if recurso.cantidad >= cantidad:
            recurso.cantidad -= cantidad
            self._registrar_evento(
                TipoEvento.RECURSO_AGREGADO,
                {"recurso": nombre, "cantidad_consumida": cantidad}
            )
            return True
        return False

    def asignar_objetivo(self, objetivo: Objetivo) -> None:
        """Asigna un objetivo al agente"""
        self.objetivos[objetivo.id] = objetivo
        self._registrar_evento(
            TipoEvento.TAREA_ASIGNADA,
            {"objetivo": asdict(objetivo)}
        )

    def actualizar_objetivo(self, objetivo_id: str, progreso: float) -> None:
        """Actualiza el progreso de un objetivo"""
        if objetivo_id in self.objetivos:
            self.objetivos[objetivo_id].progreso = min(1.0, progreso)
            if progreso >= 1.0:
                self.objetivos[objetivo_id].completado = True
                self._registrar_evento(
                    TipoEvento.TAREA_COMPLETADA,
                    {"objetivo_id": objetivo_id, "progreso": progreso}
                )

    def agregar_creencia(self, creencia: Creencia) -> None:
        """Agrega una creencia"""
        self.creencias.append(creencia)
        self._registrar_evento(
            TipoEvento.CREENCIA_ACTUALIZADA,
            {
                "contenido": creencia.contenido,
                "confianza": creencia.confianza,
                "fuente": creencia.fuente
            }
        )

    def establecer_relacion(self, relacion: Relacion) -> None:
        """Establece relación con otro agente"""
        self.relaciones[relacion.agente_id] = relacion
        self._registrar_evento(
            TipoEvento.RELACION_ESTABLECIDA,
            {"agente_id": relacion.agente_id, "tipo": relacion.tipo}
        )

    def mover_a(self, x: float, y: float, z: float, zona: str) -> None:
        """Mueve el agente a nueva posición"""
        self.posicion = Posicion(x=x, y=y, z=z, zona=zona)

    def _registrar_evento(self, tipo: TipoEvento, datos: Dict[str, Any]) -> None:
        """Registra un evento en el historial"""
        self.secuencia_evento += 1
        evento = Evento(
            id=f"evt_{self.identidad.id}_{self.secuencia_evento}",
            tipo=tipo,
            timestamp=datetime.now().isoformat(),
            datos=datos,
            secuencia=self.secuencia_evento
        )
        self.eventos.append(evento)
        self.timestamp_ultimo_cambio = datetime.now()
        self.historial_cambios.append({
            "timestamp": evento.timestamp,
            "tipo": tipo.value,
            "datos": datos
        })

    def obtener_snapshot(self) -> Dict:
        """Retorna snapshot actual del estado"""
        return {
            "identidad": asdict(self.identidad),
            "estado": self.estado_actual.value,
            "posicion": asdict(self.posicion),
            "recursos": {k: asdict(v) for k, v in self.recursos.items()},
            "objetivos": {k: asdict(v) for k, v in self.objetivos.items()},
            "creencias": [asdict(c) for c in self.creencias],
            "relaciones": {k: asdict(v) for k, v in self.relaciones.items()},
            "timestamp": datetime.now().isoformat()
        }

    def obtener_resumen(self) -> Dict:
        """Resumen legible del estado actual"""
        return {
            "agente": self.identidad.nombre,
            "tipo": self.identidad.tipo,
            "estado": self.estado_actual.value,
            "posicion": f"({self.posicion.x}, {self.posicion.y}, {self.posicion.z}) en {self.posicion.zona}",
            "recursos": {k: f"{v.cantidad} {v.unidad}" for k, v in self.recursos.items()},
            "objetivos_activos": len([o for o in self.objetivos.values() if not o.completado]),
            "creencias": len(self.creencias),
            "relaciones": len(self.relaciones),
            "eventos_registrados": len(self.eventos),
            "ultimo_cambio": self.timestamp_ultimo_cambio.isoformat()
        }


# ============================================================================
# PERSISTENCIA
# ============================================================================

class PersistenciaEstado:
    """Maneja persistencia y recuperación de estado"""

    def __init__(self, directorio: str = "./agent_states"):
        self.directorio = Path(directorio)
        self.directorio.mkdir(exist_ok=True)

    def guardar_estado(self, estado: EstadoAgenteLLM) -> str:
        """Guarda estado a archivo, retorna path"""
        snapshot = estado.obtener_snapshot()
        archivo = self.directorio / f"{estado.identidad.id}_snapshot.json"

        with open(archivo, "w") as f:
            json.dump(snapshot, f, indent=2)

        return str(archivo)

    def guardar_eventos(self, estado: EstadoAgenteLLM) -> str:
        """Guarda todos los eventos (event log)"""
        eventos = [e.to_dict() for e in estado.eventos]
        archivo = self.directorio / f"{estado.identidad.id}_events.json"

        with open(archivo, "w") as f:
            json.dump(eventos, f, indent=2)

        return str(archivo)

    def cargar_estado(self, agente_id: str) -> Optional[Dict]:
        """Carga snapshot de estado"""
        archivo = self.directorio / f"{agente_id}_snapshot.json"
        if not archivo.exists():
            return None

        with open(archivo, "r") as f:
            return json.load(f)

    def cargar_eventos(self, agente_id: str) -> List[Dict]:
        """Carga historial de eventos"""
        archivo = self.directorio / f"{agente_id}_events.json"
        if not archivo.exists():
            return []

        with open(archivo, "r") as f:
            return json.load(f)

    def listar_agentes(self) -> List[str]:
        """Lista todos los agentes guardados"""
        archivos = list(self.directorio.glob("*_snapshot.json"))
        return [f.stem.replace("_snapshot", "") for f in archivos]


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demo_gestion_estado():
    """Demuestra gestión de estado en agentes"""

    print("=" * 80)
    print("DEMOSTRACIÓN: GESTIÓN DE ESTADO EN AGENTES")
    print("=" * 80)

    # Crear agente
    print("\n1. CREACIÓN DE AGENTE")
    print("-" * 80)
    identidad = Identidad(
        id="ag001",
        nombre="Alice",
        tipo="supervisora"
    )
    agente = EstadoAgenteLLM(identidad)
    print(f"Agente creado: {agente.identidad.nombre} (tipo: {agente.identidad.tipo})")

    # Agregar recursos
    print("\n2. AGREGACIÓN DE RECURSOS")
    print("-" * 80)
    agente.agregar_recurso(Recurso("CPU", cantidad=100.0, unidad="GHz"))
    agente.agregar_recurso(Recurso("Memoria", cantidad=16.0, unidad="GB"))
    agente.agregar_recurso(Recurso("Energía", cantidad=1000.0, unidad="Joules"))
    print("Recursos agregados:")
    for nombre, recurso in agente.recursos.items():
        print(f"  - {nombre}: {recurso.cantidad} {recurso.unidad}")

    # Cambiar estado
    print("\n3. CAMBIO DE ESTADO")
    print("-" * 80)
    print(f"Estado anterior: {agente.estado_actual.value}")
    agente.cambiar_estado(EstadoAgente.PROCESANDO)
    print(f"Estado actual: {agente.estado_actual.value}")

    # Agregar objetivos
    print("\n4. ASIGNACIÓN DE OBJETIVOS")
    print("-" * 80)
    obj1 = Objetivo(
        id="obj001",
        descripcion="Procesar datos de entrada",
        prioridad=0.9
    )
    obj2 = Objetivo(
        id="obj002",
        descripcion="Enviar reporte",
        prioridad=0.7
    )
    agente.asignar_objetivo(obj1)
    agente.asignar_objetivo(obj2)
    print("Objetivos asignados:")
    for objetivo in agente.objetivos.values():
        print(f"  - {objetivo.descripcion} (prioridad: {objetivo.prioridad})")

    # Actualizar objetivos
    print("\n5. PROGRESO DE OBJETIVOS")
    print("-" * 80)
    agente.actualizar_objetivo("obj001", 0.5)
    print(f"Objetivo obj001 - Progreso: {agente.objetivos['obj001'].progreso}")
    agente.actualizar_objetivo("obj001", 1.0)
    print(f"Objetivo obj001 - Completado: {agente.objetivos['obj001'].completado}")

    # Agregar creencias
    print("\n6. AGREGACIÓN DE CREENCIAS")
    print("-" * 80)
    agente.agregar_creencia(Creencia(
        contenido="El sistema está en buenas condiciones",
        confianza=0.95,
        fuente="sensor"
    ))
    agente.agregar_creencia(Creencia(
        contenido="Los usuarios están satisfechos",
        confianza=0.7,
        fuente="otro_agente"
    ))
    print(f"Creencias almacenadas: {len(agente.creencias)}")

    # Establecer relaciones
    print("\n7. RELACIONES CON OTROS AGENTES")
    print("-" * 80)
    agente.establecer_relacion(Relacion(
        agente_id="ag002",
        tipo="aliado",
        confianza=0.8
    ))
    agente.establecer_relacion(Relacion(
        agente_id="ag003",
        tipo="supervisor",
        confianza=0.95
    ))
    print(f"Relaciones establecidas: {len(agente.relaciones)}")
    for otro_id, relacion in agente.relaciones.items():
        print(f"  - Con {otro_id}: {relacion.tipo} (confianza: {relacion.confianza})")

    # Snapshot del estado
    print("\n8. SNAPSHOT DEL ESTADO")
    print("-" * 80)
    resumen = agente.obtener_resumen()
    for clave, valor in resumen.items():
        print(f"  {clave}: {valor}")

    # Event Sourcing
    print("\n9. EVENT SOURCING - HISTORIAL DE EVENTOS")
    print("-" * 80)
    print(f"Total de eventos registrados: {len(agente.eventos)}")
    print("\nÚltimos 5 eventos:")
    for evento in agente.eventos[-5:]:
        print(f"  [{evento.timestamp}] {evento.tipo.value}: {evento.datos}")

    # Persistencia
    print("\n10. PERSISTENCIA DE ESTADO")
    print("-" * 80)
    persistencia = PersistenciaEstado()
    archivo_snapshot = persistencia.guardar_estado(agente)
    archivo_eventos = persistencia.guardar_eventos(agente)
    print(f"Estado guardado en: {archivo_snapshot}")
    print(f"Eventos guardados en: {archivo_eventos}")

    # Recuperación
    print("\n11. RECUPERACIÓN DE ESTADO")
    print("-" * 80)
    estado_recuperado = persistencia.cargar_estado("ag001")
    if estado_recuperado:
        print("Estado recuperado exitosamente:")
        print(f"  Agente: {estado_recuperado['identidad']['nombre']}")
        print(f"  Estado: {estado_recuperado['estado']}")
        print(f"  Recursos: {len(estado_recuperado['recursos'])}")
        print(f"  Objetivos: {len(estado_recuperado['objetivos'])}")

    eventos_recuperados = persistencia.cargar_eventos("ag001")
    print(f"\nEventos recuperados: {len(eventos_recuperados)}")

    print("\n" + "=" * 80)
    print("Conclusión: El estado del agente se mantiene persistentemente")
    print("y puede recuperarse completamente usando snapshots y event sourcing")
    print("=" * 80)


if __name__ == "__main__":
    demo_gestion_estado()
