"""
01_TIPOS_MEMORIA.PY
==================

Ejemplo didáctico: Tipos de Memoria en Agentes

Este módulo demuestra la implementación de diferentes tipos de memoria
basada en el modelo neurobiológico humano:

- Memoria Sensorial: muy breve, gran capacidad
- Memoria de Trabajo: limitada (4-7 items), consciente
- Memoria Episódica: eventos específicos con contexto temporal
- Memoria Semántica: conocimiento abstracto y hechos
- Memoria Procedural: habilidades y cómo hacer cosas

Sistema: LangChain + Ollama (ejecutable localmente)

REQUISITOS PREVIOS:
- Ollama instalado y ejecutándose: ollama serve
- En otra terminal: ollama pull mistral (o tu modelo preferido)
- pip install langchain ollama python-dotenv
"""

from collections import deque
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import json
import time

# ============================================================================
# MEMORIA SENSORIAL
# ============================================================================

@dataclass
class MemoriaSensorial:
    """
    Simula la memoria sensorial: muy breve duración (milisegundos),
    gran capacidad, sensaciones brutas sin procesar.
    """
    capacidad: int = 100  # items máximos en buffer
    tiempo_duracion_ms: float = 100  # duracion en milisegundos
    buffer: deque = field(default_factory=deque)

    def registrar(self, estimulo: str, timestamp: Optional[float] = None) -> None:
        """Registra un estímulo sensorial con timestamp"""
        if len(self.buffer) >= self.capacidad:
            self.buffer.popleft()

        ts = timestamp or time.time()
        self.buffer.append({
            "estimulo": estimulo,
            "timestamp": ts,
            "edad_ms": 0
        })

    def obtener_activos(self) -> List[Dict]:
        """Retorna estímulos que aún no han expirado"""
        ahora = time.time()
        activos = []

        for item in self.buffer:
            edad_ms = (ahora - item["timestamp"]) * 1000
            if edad_ms < self.tiempo_duracion_ms:
                item["edad_ms"] = edad_ms
                activos.append(item)

        return activos

    def limpiar_expirados(self) -> int:
        """Limpia estímulos expirados, retorna cantidad limpiada"""
        activos = self.obtener_activos()
        cantidad_limpiada = len(self.buffer) - len(activos)
        self.buffer = deque(activos)
        return cantidad_limpiada


# ============================================================================
# MEMORIA DE TRABAJO (WORKING MEMORY)
# ============================================================================

@dataclass
class MemoriaTrabajoItem:
    """Representa un item en memoria de trabajo"""
    contenido: str
    importancia: float = 0.5  # 0.0 a 1.0
    timestamp: float = field(default_factory=time.time)
    accesos: int = 0  # cuántas veces se accedió

    def envejecer(self, factor: float = 0.95) -> None:
        """Reduce importancia con el tiempo"""
        self.importancia *= factor


class MemoriaTrabajoLimitada:
    """
    Simula memoria de trabajo: limitada (típicamente 4-7 items),
    consciente, accesible directamente, información actual en procesamiento.
    """
    def __init__(self, capacidad: int = 7):
        self.capacidad = capacidad
        self.items: List[MemoriaTrabajoItem] = []

    def agregar(self, contenido: str, importancia: float = 0.5) -> bool:
        """Agrega item a memoria de trabajo. Si llena, elimina menos importante"""
        if len(self.items) < self.capacidad:
            self.items.append(MemoriaTrabajoItem(contenido, importancia))
            return True

        # Memoria llena: eliminar item menos importante
        if self.items:
            idx_min = min(range(len(self.items)),
                         key=lambda i: self.items[i].importancia)
            self.items.pop(idx_min)
            self.items.append(MemoriaTrabajoItem(contenido, importancia))
            return True

        return False

    def obtener(self, indice: int) -> Optional[MemoriaTrabajoItem]:
        """Accede a item por índice, incrementa contador de accesos"""
        if 0 <= indice < len(self.items):
            self.items[indice].accesos += 1
            return self.items[indice]
        return None

    def envejecer_todos(self) -> None:
        """Envejece todos los items (reduce importancia)"""
        for item in self.items:
            item.envejecer()

    def listar(self) -> List[Dict]:
        """Retorna representación de items actuales"""
        return [
            {
                "contenido": item.contenido,
                "importancia": round(item.importancia, 2),
                "accesos": item.accesos,
                "edad_s": round(time.time() - item.timestamp, 2)
            }
            for item in self.items
        ]


# ============================================================================
# MEMORIA EPISÓDICA
# ============================================================================

@dataclass
class Episodio:
    """Representa un episodio: evento específico con contexto temporal"""
    descripcion: str
    timestamp: float = field(default_factory=time.time)
    contexto: Dict[str, Any] = field(default_factory=dict)
    entidades_involucradas: List[str] = field(default_factory=list)
    emociones: Dict[str, float] = field(default_factory=dict)  # importancia emocional

    def get_timestamp_legible(self) -> str:
        return datetime.fromtimestamp(self.timestamp).isoformat()


class MemoriaEpisodica:
    """
    Registra eventos específicos ordenados cronológicamente.
    Facilita aprendizaje de situaciones y recuperación de experiencias.
    """
    def __init__(self, max_episodios: int = 1000):
        self.max_episodios = max_episodios
        self.episodios: List[Episodio] = []

    def registrar_evento(
        self,
        descripcion: str,
        contexto: Dict[str, Any] = None,
        entidades: List[str] = None,
        emociones: Dict[str, float] = None
    ) -> None:
        """Registra un nuevo episodio"""
        episodio = Episodio(
            descripcion=descripcion,
            contexto=contexto or {},
            entidades_involucradas=entidades or [],
            emociones=emociones or {}
        )
        self.episodios.append(episodio)

        # Limitar tamaño
        if len(self.episodios) > self.max_episodios:
            self.episodios.pop(0)

    def recuperar_por_rango_temporal(
        self,
        hace_segundos: float
    ) -> List[Episodio]:
        """Recupera episodios de los últimos N segundos"""
        ahora = time.time()
        cutoff = ahora - hace_segundos
        return [ep for ep in self.episodios if ep.timestamp >= cutoff]

    def recuperar_por_entidad(self, entidad: str) -> List[Episodio]:
        """Recupera episodios que involucran una entidad específica"""
        return [
            ep for ep in self.episodios
            if entidad in ep.entidades_involucradas
        ]

    def obtener_timeline(self) -> List[Dict]:
        """Retorna timeline de episodios"""
        return [
            {
                "timestamp": ep.get_timestamp_legible(),
                "descripcion": ep.descripcion,
                "entidades": ep.entidades_involucradas,
                "contexto": ep.contexto
            }
            for ep in self.episodios[-10:]  # últimos 10
        ]


# ============================================================================
# MEMORIA SEMÁNTICA
# ============================================================================

class MemoriaSemantica:
    """
    Almacena conocimiento abstracto: hechos, conceptos, relaciones.
    Descontextualizado e intemporal, compartible entre agentes.
    """
    def __init__(self):
        self.hechos: Dict[str, Any] = {}  # clave: valor
        self.conceptos: Dict[str, Dict[str, Any]] = {}  # conceptos con propiedades
        self.relaciones: List[Dict[str, str]] = []  # sujeto-predicado-objeto

    def agregar_hecho(self, clave: str, valor: Any) -> None:
        """Agrega un hecho simple"""
        self.hechos[clave] = valor

    def agregar_concepto(
        self,
        nombre: str,
        propiedades: Dict[str, Any]
    ) -> None:
        """Agrega un concepto con propiedades"""
        self.conceptos[nombre] = propiedades

    def agregar_relacion(
        self,
        sujeto: str,
        predicado: str,
        objeto: str
    ) -> None:
        """Agrega una relación triple (sujeto-predicado-objeto)"""
        self.relaciones.append({
            "sujeto": sujeto,
            "predicado": predicado,
            "objeto": objeto
        })

    def consultar_hecho(self, clave: str) -> Optional[Any]:
        """Consulta un hecho por clave"""
        return self.hechos.get(clave)

    def obtener_concepto(self, nombre: str) -> Optional[Dict]:
        """Obtiene propiedades de un concepto"""
        return self.conceptos.get(nombre)

    def buscar_relaciones(
        self,
        sujeto: Optional[str] = None,
        predicado: Optional[str] = None
    ) -> List[Dict]:
        """Busca relaciones por criterios"""
        resultados = []
        for rel in self.relaciones:
            if sujeto and rel["sujeto"] != sujeto:
                continue
            if predicado and rel["predicado"] != predicado:
                continue
            resultados.append(rel)
        return resultados

    def exportar_conocimiento(self) -> Dict:
        """Exporta toda la memoria semántica"""
        return {
            "hechos": self.hechos,
            "conceptos": self.conceptos,
            "relaciones": self.relaciones
        }


# ============================================================================
# MEMORIA PROCEDURAL (HABILIDADES Y SKILLS)
# ============================================================================

class MemoriaProceduralItem:
    """Representa una habilidad o procedimiento"""
    def __init__(
        self,
        nombre: str,
        descripcion: str,
        pasos: List[str],
        precondiciones: List[str] = None,
        postcondiciones: List[str] = None
    ):
        self.nombre = nombre
        self.descripcion = descripcion
        self.pasos = pasos
        self.precondiciones = precondiciones or []
        self.postcondiciones = postcondiciones or []
        self.veces_ejecutada = 0
        self.tasa_exito = 1.0  # 0.0 a 1.0


class MemoriaProcedural:
    """
    Almacena habilidades, scripts y procedimientos.
    Mejora con práctica, se ejecuta automáticamente.
    """
    def __init__(self):
        self.habilidades: Dict[str, MemoriaProceduralItem] = {}

    def agregar_habilidad(self, habilidad: MemoriaProceduralItem) -> None:
        """Agrega una habilidad"""
        self.habilidades[habilidad.nombre] = habilidad

    def ejecutar_habilidad(self, nombre: str) -> Optional[Dict]:
        """Ejecuta una habilidad, registra intento"""
        if nombre not in self.habilidades:
            return None

        skill = self.habilidades[nombre]

        # Verificar precondiciones
        resultado = {
            "nombre": nombre,
            "pasos_ejecutados": skill.pasos,
            "precondiciones_ok": len(skill.precondiciones) == 0,
            "postcondiciones_ok": len(skill.postcondiciones) == 0,
            "exito": True
        }

        # Registrar ejecución (mejorar con práctica)
        skill.veces_ejecutada += 1
        skill.tasa_exito = min(1.0, skill.tasa_exito + 0.01)  # mejora gradualmente

        return resultado

    def listar_habilidades(self) -> List[Dict]:
        """Lista todas las habilidades aprendidas"""
        return [
            {
                "nombre": skill.nombre,
                "descripcion": skill.descripcion,
                "veces_ejecutada": skill.veces_ejecutada,
                "tasa_exito": round(skill.tasa_exito, 2),
                "pasos": len(skill.pasos)
            }
            for skill in self.habilidades.values()
        ]


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demo_tipos_memoria():
    """Demuestra todos los tipos de memoria"""

    print("=" * 80)
    print("DEMOSTRACIÓN: TIPOS DE MEMORIA EN AGENTES")
    print("=" * 80)

    # --- MEMORIA SENSORIAL ---
    print("\n1. MEMORIA SENSORIAL (muy breve, gran capacidad)")
    print("-" * 80)
    mem_sensorial = MemoriaSensorial(capacidad=10, tiempo_duracion_ms=3000)

    # Simular estímulos
    for i in range(5):
        mem_sensorial.registrar(f"Estímulo visual {i}")

    print(f"Estímulos activos: {len(mem_sensorial.obtener_activos())}")
    print(f"Buffer total: {len(mem_sensorial.buffer)}")

    # Simular paso de tiempo
    time.sleep(3.5)
    mem_sensorial.limpiar_expirados()
    print(f"Después de 3.5s: estímulos activos = {len(mem_sensorial.obtener_activos())}")

    # --- MEMORIA DE TRABAJO ---
    print("\n2. MEMORIA DE TRABAJO (limitada a 7 items, consciente)")
    print("-" * 80)
    mem_trabajo = MemoriaTrabajoLimitada(capacidad=4)

    mem_trabajo.agregar("Tarea urgente A", importancia=0.9)
    mem_trabajo.agregar("Nota B", importancia=0.5)
    mem_trabajo.agregar("Contexto C", importancia=0.7)
    mem_trabajo.agregar("Información D", importancia=0.3)

    print(f"Items en memoria de trabajo:")
    for item in mem_trabajo.listar():
        print(f"  - {item['contenido']}: importancia={item['importancia']}")

    # Intentar agregar cuando está llena
    print(f"\nIntentando agregar item cuando memoria está llena...")
    mem_trabajo.agregar("Item nuevo E", importancia=0.8)
    print(f"Items después de agregar (nota: se elimina el menos importante):")
    for item in mem_trabajo.listar():
        print(f"  - {item['contenido']}: importancia={item['importancia']}")

    # --- MEMORIA EPISÓDICA ---
    print("\n3. MEMORIA EPISÓDICA (eventos con contexto temporal)")
    print("-" * 80)
    mem_episodica = MemoriaEpisodica()

    # Registrar eventos
    mem_episodica.registrar_evento(
        "Usuario preguntó sobre precios",
        contexto={"producto": "laptop", "cantidad": 2},
        entidades=["usuario", "producto"],
        emociones={"confianza": 0.8}
    )

    mem_episodica.registrar_evento(
        "Completada transacción de venta",
        contexto={"monto": 2000, "moneda": "USD"},
        entidades=["usuario", "sistema_pago"],
        emociones={"satisfacción": 0.9}
    )

    print("Timeline de episodios:")
    for ep in mem_episodica.obtener_timeline():
        print(f"  [{ep['timestamp']}] {ep['descripcion']}")

    # --- MEMORIA SEMÁNTICA ---
    print("\n4. MEMORIA SEMÁNTICA (conocimiento abstracto)")
    print("-" * 80)
    mem_semantica = MemoriaSemantica()

    # Hechos
    mem_semantica.agregar_hecho("capital_españa", "Madrid")
    mem_semantica.agregar_hecho("idioma_oficial_españa", "Español")

    # Conceptos
    mem_semantica.agregar_concepto("Laptop", {
        "tipo": "dispositivo",
        "categoria": "electrónica",
        "precio_promedio": 1000
    })

    # Relaciones
    mem_semantica.agregar_relacion("Laptop", "es_tipo_de", "Computadora")
    mem_semantica.agregar_relacion("Español", "idioma_oficial", "España")

    print("Hechos registrados:")
    for clave, valor in mem_semantica.hechos.items():
        print(f"  {clave}: {valor}")

    print("\nRelaciones:")
    for rel in mem_semantica.relaciones:
        print(f"  {rel['sujeto']} {rel['predicado']} {rel['objeto']}")

    # --- MEMORIA PROCEDURAL ---
    print("\n5. MEMORIA PROCEDURAL (habilidades y procedimientos)")
    print("-" * 80)
    mem_procedural = MemoriaProcedural()

    # Agregar habilidades
    skill_venta = MemoriaProceduralItem(
        nombre="realizar_venta",
        descripcion="Proceso completo de venta",
        pasos=[
            "Identificar necesidades cliente",
            "Presentar opciones",
            "Negociar precio",
            "Procesar pago",
            "Enviar confirmación"
        ]
    )
    mem_procedural.agregar_habilidad(skill_venta)

    skill_soporte = MemoriaProceduralItem(
        nombre="resolver_ticket_soporte",
        descripcion="Resolver ticket de soporte técnico",
        pasos=[
            "Leer ticket",
            "Diagnosticar problema",
            "Aplicar solución",
            "Verificar resolución",
            "Cerrar ticket"
        ]
    )
    mem_procedural.agregar_habilidad(skill_soporte)

    # Ejecutar habilidades varias veces
    print("Ejecutando habilidades...")
    for _ in range(3):
        mem_procedural.ejecutar_habilidad("realizar_venta")

    for _ in range(5):
        mem_procedural.ejecutar_habilidad("resolver_ticket_soporte")

    print("\nHabilidades aprendidas:")
    for skill in mem_procedural.listar_habilidades():
        print(f"  {skill['nombre']}: ejecutada {skill['veces_ejecutada']} veces, "
              f"tasa éxito={skill['tasa_exito']}")

    print("\n" + "=" * 80)
    print("Conclusión: Los 5 tipos de memoria modelan cómo los agentes")
    print("procesan información en diferentes escalas temporales y contextos.")
    print("=" * 80)


if __name__ == "__main__":
    demo_tipos_memoria()
