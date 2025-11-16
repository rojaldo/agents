"""
07_MEMORIA_JERARQUICA.PY
=========================

Ejemplo didáctico: Sistema de Memoria Jerárquica Avanzada

Demuestra:
- Memoria en múltiples niveles: específicos -> patrones -> abstractos
- Compresión y consolidación de información
- Interferencia y recuperación de memoria
- Olvido adaptativo basado en importancia y recency
- Arquitectura escalable para agentes complejos

REQUISITOS PREVIOS:
- pip install langchain ollama
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple
from enum import Enum
from datetime import datetime, timedelta
import time
import math


# ============================================================================
# NIVELES DE MEMORIA
# ============================================================================

class NivelMemoria(Enum):
    """Niveles jerárquicos de abstracción en memoria"""
    EPISODICO = 1  # Detalles específicos de eventos
    TACTICA = 2    # Patrones y regularidades
    ESTRATEGICO = 3  # Reglas generales abstractas


@dataclass
class RegistroEpisodico:
    """Nivel 1: Detalles específicos de un evento"""
    id: str
    descripcion: str
    timestamp: float
    detalles: Dict = field(default_factory=dict)
    entidades: Set[str] = field(default_factory=set)
    importancia: float = 0.5

    def envejecer(self, factor: float = 0.98) -> None:
        """Reduce importancia con edad (olvido natural)"""
        self.importancia = max(0.0, self.importancia * factor)

    def obtener_edad_horas(self) -> float:
        """Retorna edad en horas"""
        return (time.time() - self.timestamp) / 3600


@dataclass
class PatronTactico:
    """Nivel 2: Patrón reconocido a partir de episodios"""
    id: str
    descripcion: str
    ejemplos: List[str] = field(default_factory=list)  # IDs de episodios
    confianza: float = 0.5  # qué tan seguro es el patrón
    frecuencia: int = 0  # cuántas veces observado
    regla_generada: str = ""
    timestamp_creacion: float = field(default_factory=time.time)

    def agregar_ejemplo(self, episodio_id: str) -> None:
        """Agrega un episodio como ejemplo del patrón"""
        if episodio_id not in self.ejemplos:
            self.ejemplos.append(episodio_id)
            self.frecuencia += 1

    def aumentar_confianza(self, incremento: float = 0.1) -> None:
        """Aumenta confianza basada en más ejemplos"""
        self.confianza = min(1.0, self.confianza + incremento)


@dataclass
class ReglaBstracia:
    """Nivel 3: Regla general abstracta"""
    id: str
    regla: str  # Ej: "Si X entonces Y"
    confianza: float = 0.7
    dominios_aplicables: Set[str] = field(default_factory=set)
    patrones_subyacentes: List[str] = field(default_factory=list)
    excepciones: List[str] = field(default_factory=list)


# ============================================================================
# MEMORIA JERÁRQUICA
# ============================================================================

class MemoriaJerarquica:
    """
    Sistema de memoria en tres niveles jerárquicos.
    Información fluye de abajo (episódico) hacia arriba (abstracto).
    """

    def __init__(self):
        # Nivel 1: Episódico (detalles específicos)
        self.episodios: Dict[str, RegistroEpisodico] = {}

        # Nivel 2: Táctico (patrones)
        self.patrones: Dict[str, PatronTactico] = {}

        # Nivel 3: Estratégico (reglas)
        self.reglas: Dict[str, ReglaBstracia] = {}

        # Contador para IDs
        self.contador_episodios = 0
        self.contador_patrones = 0
        self.contador_reglas = 0

        # Historial de consolidación
        self.historial_consolidacion: List[Dict] = []

    # ========== NIVEL 1: EPISÓDICO ==========

    def registrar_episodio(
        self,
        descripcion: str,
        detalles: Dict = None,
        entidades: Set[str] = None,
        importancia: float = 0.5
    ) -> str:
        """Registra un nuevo episodio (evento específico)"""
        self.contador_episodios += 1
        episodio_id = f"ep_{self.contador_episodios}"

        episodio = RegistroEpisodico(
            id=episodio_id,
            descripcion=descripcion,
            timestamp=time.time(),
            detalles=detalles or {},
            entidades=entidades or set(),
            importancia=importancia
        )

        self.episodios[episodio_id] = episodio
        return episodio_id

    def obtener_episodios_recientes(self, horas: float = 24) -> List[RegistroEpisodico]:
        """Obtiene episodios recientes"""
        cutoff = time.time() - (horas * 3600)
        return [
            ep for ep in self.episodios.values()
            if ep.timestamp >= cutoff
        ]

    # ========== NIVEL 2: TÁCTICO ==========

    def extraer_patrones(self, min_frecuencia: int = 2) -> None:
        """
        Extrae patrones a partir de episodios.
        Consolidación: episodios específicos -> patrones tácticos
        """
        # Agrupar episodios por similitud de entidades
        grupos_entidades: Dict[frozenset, List[str]] = {}

        for ep_id, episodio in self.episodios.items():
            if episodio.entidades:
                clave = frozenset(episodio.entidades)
                if clave not in grupos_entidades:
                    grupos_entidades[clave] = []
                grupos_entidades[clave].append(ep_id)

        # Crear patrones de grupos frecuentes
        for entidades, episodio_ids in grupos_entidades.items():
            if len(episodio_ids) >= min_frecuencia:
                self.contador_patrones += 1
                patron_id = f"pat_{self.contador_patrones}"

                # Generar descripción del patrón
                entidades_str = ", ".join(sorted(entidades))
                descripcion = f"Patrón con entidades: {entidades_str}"

                patron = PatronTactico(
                    id=patron_id,
                    descripcion=descripcion,
                    confianza=min(1.0, 0.5 + (len(episodio_ids) * 0.1))
                )

                # Agregar episodios como ejemplos
                for ep_id in episodio_ids:
                    patron.agregar_ejemplo(ep_id)

                self.patrones[patron_id] = patron

        self.historial_consolidacion.append({
            "timestamp": datetime.now().isoformat(),
            "tipo": "extraccion_patrones",
            "patrones_creados": self.contador_patrones
        })

    def obtener_patrones_confiables(self, umbral_confianza: float = 0.7) -> List[PatronTactico]:
        """Obtiene patrones con suficiente confianza"""
        return [
            p for p in self.patrones.values()
            if p.confianza >= umbral_confianza
        ]

    # ========== NIVEL 3: ESTRATÉGICO ==========

    def generar_reglas(self) -> None:
        """
        Genera reglas abstractas a partir de patrones.
        Consolidación: patrones -> reglas estratégicas
        """
        for patron in self.patrones.values():
            if patron.confianza >= 0.7:
                self.contador_reglas += 1
                regla_id = f"regla_{self.contador_reglas}"

                regla = ReglaBstracia(
                    id=regla_id,
                    regla=f"Si ocurren {patron.descripcion} -> Patrón identificado",
                    confianza=patron.confianza,
                    patrones_subyacentes=[patron.id]
                )

                self.reglas[regla_id] = regla

        self.historial_consolidacion.append({
            "timestamp": datetime.now().isoformat(),
            "tipo": "generacion_reglas",
            "reglas_creadas": self.contador_reglas
        })

    def obtener_reglas_aplicables(self, dominio: str) -> List[ReglaBstracia]:
        """Obtiene reglas aplicables a un dominio"""
        return [
            r for r in self.reglas.values()
            if dominio in r.dominios_aplicables or not r.dominios_aplicables
        ]

    # ========== CONSOLIDACIÓN Y COMPRESIÓN ==========

    def consolidar_memoria(self) -> None:
        """
        Consolida memoria: mueve información de episódico a patrones/reglas.
        Similar al proceso de sueño en humanos.
        """
        # 1. Extraer patrones de episodios
        self.extraer_patrones(min_frecuencia=2)

        # 2. Generar reglas de patrones
        self.generar_reglas()

        # 3. Envejecer episodios (olvido natural)
        for episodio in self.episodios.values():
            episodio.envejecer(factor=0.95)

    def olvidar_episodios_insignificantes(self, umbral_importancia: float = 0.2) -> int:
        """
        Olvido adaptativo: elimina episodios poco importantes y antiguos.
        Privacidad: libera datos sensibles.
        """
        a_eliminar = []

        for ep_id, episodio in self.episodios.items():
            # Calcular score para olvido
            edad_dias = episodio.obtener_edad_horas() / 24
            factor_edad = math.exp(-edad_dias / 30)  # exponencial decay
            score_olvido = episodio.importancia * factor_edad

            if score_olvido < umbral_importancia:
                a_eliminar.append(ep_id)

        # Eliminar
        for ep_id in a_eliminar:
            del self.episodios[ep_id]

        return len(a_eliminar)

    def obtener_tamano_memoria(self) -> Dict[str, int]:
        """Retorna tamaño en cada nivel"""
        return {
            "episodios": len(self.episodios),
            "patrones": len(self.patrones),
            "reglas": len(self.reglas),
            "total_items": (len(self.episodios) + len(self.patrones) + len(self.reglas))
        }

    # ========== RECUPERACIÓN ==========

    def recuperar_informacion(self, query: str) -> Dict:
        """
        Recupera información relevante a través de todos los niveles.
        Empieza en nivel abstracto (reglas), desciende si necesario.
        """
        resultados = {
            "reglas_aplicables": [],
            "patrones_relevantes": [],
            "episodios_relacionados": []
        }

        palabras_query = set(query.lower().split())

        # Buscar en reglas
        for regla in self.reglas.values():
            palabras_regla = set(regla.regla.lower().split())
            if palabras_query & palabras_regla:
                resultados["reglas_aplicables"].append({
                    "regla": regla.regla,
                    "confianza": regla.confianza
                })

        # Buscar en patrones
        for patron in self.patrones.values():
            palabras_patron = set(patron.descripcion.lower().split())
            if palabras_query & palabras_patron:
                resultados["patrones_relevantes"].append({
                    "descripcion": patron.descripcion,
                    "frecuencia": patron.frecuencia,
                    "confianza": patron.confianza
                })

        # Buscar en episodios (solo si no hay resultados arriba)
        if not resultados["patrones_relevantes"]:
            for episodio in self.episodios.values():
                palabras_ep = set(episodio.descripcion.lower().split())
                if palabras_query & palabras_ep:
                    resultados["episodios_relacionados"].append({
                        "descripcion": episodio.descripcion,
                        "edad_horas": episodio.obtener_edad_horas(),
                        "importancia": episodio.importancia
                    })

        return resultados

    # ========== UTILIDADES ==========

    def obtener_resumen(self) -> Dict:
        """Resumen de toda la memoria"""
        return {
            "tamaño": self.obtener_tamano_memoria(),
            "patrones_confiables": len(self.obtener_patrones_confiables()),
            "reglas_abstractas": len(self.reglas),
            "consolidaciones_realizadas": len(self.historial_consolidacion),
            "estado": "Memoria jerárquica lista"
        }


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demo_memoria_jerarquica():
    """Demuestra sistema de memoria jerárquica"""

    print("=" * 80)
    print("DEMOSTRACIÓN: SISTEMA DE MEMORIA JERÁRQUICA")
    print("=" * 80)

    # Crear memoria jerárquica
    memoria = MemoriaJerarquica()

    # 1. REGISTRAR EPISODIOS (NIVEL 1)
    print("\n1. REGISTRO DE EPISODIOS ESPECÍFICOS (NIVEL 1)")
    print("-" * 80)

    episodios_registrados = []

    # Simular múltiples eventos similares
    eventos = [
        ("Usuario consulta precio laptop", {"producto": "laptop", "accion": "consulta"}, 0.8),
        ("Usuario pregunta especificaciones laptop", {"producto": "laptop", "accion": "especificaciones"}, 0.7),
        ("Usuario compra laptop", {"producto": "laptop", "accion": "compra"}, 0.9),
        ("Usuario devuelve laptop defectuosa", {"producto": "laptop", "accion": "devolución"}, 0.85),
        ("Usuario pregunta por tablet", {"producto": "tablet", "accion": "consulta"}, 0.6),
        ("Usuario compra tablet", {"producto": "tablet", "accion": "compra"}, 0.8),
    ]

    for descripcion, detalles, importancia in eventos:
        entidades = set(detalles.keys())
        ep_id = memoria.registrar_episodio(
            descripcion,
            detalles=detalles,
            entidades=entidades,
            importancia=importancia
        )
        episodios_registrados.append(ep_id)
        print(f"  ✓ {descripcion} (importancia: {importancia})")

    print(f"\nEpisodios registrados: {len(memoria.episodios)}")

    # 2. EXTRACCIÓN DE PATRONES (NIVEL 2)
    print("\n2. CONSOLIDACIÓN: EXTRACCIÓN DE PATRONES (NIVEL 2)")
    print("-" * 80)

    print("Identificando patrones en episodios...")
    memoria.extraer_patrones(min_frecuencia=2)

    print(f"Patrones extraídos: {len(memoria.patrones)}")
    for patron in memoria.obtener_patrones_confiables():
        print(f"  - {patron.descripcion}")
        print(f"    Confianza: {patron.confianza:.2f}, Ejemplos: {patron.frecuencia}")

    # 3. GENERACIÓN DE REGLAS (NIVEL 3)
    print("\n3. CONSOLIDACIÓN: GENERACIÓN DE REGLAS (NIVEL 3)")
    print("-" * 80)

    print("Generando reglas abstractas...")
    memoria.generar_reglas()

    print(f"Reglas generadas: {len(memoria.reglas)}")
    for regla in memoria.reglas.values():
        print(f"  - {regla.regla}")
        print(f"    Confianza: {regla.confianza:.2f}")

    # 4. TAMAÑO DE MEMORIA
    print("\n4. DISTRIBUCIÓN JERÁRQUICA EN MEMORIA")
    print("-" * 80)

    tamaño = memoria.obtener_tamano_memoria()
    print(f"Episodios (detalles específicos): {tamaño['episodios']}")
    print(f"Patrones (regularidades):        {tamaño['patrones']}")
    print(f"Reglas (abstracciones):          {tamaño['reglas']}")
    print(f"Total de items:                  {tamaño['total_items']}")

    # Visualizar compresión
    if tamaño['episodios'] > 0:
        ratio_compresion = tamaño['total_items'] / tamaño['episodios']
        print(f"\nRatio de compresión: {tamaño['episodios']} episodios -> {tamaño['total_items']} items ({ratio_compresion:.2f}x)")

    # 5. RECUPERACIÓN
    print("\n5. RECUPERACIÓN DE INFORMACIÓN")
    print("-" * 80)

    queries = [
        "laptop consulta",
        "tablet compra",
        "defectuosa",
    ]

    for query in queries:
        print(f"\nBúsqueda: '{query}'")
        resultados = memoria.recuperar_informacion(query)

        if resultados["reglas_aplicables"]:
            print(f"  Reglas aplicables:")
            for regla in resultados["reglas_aplicables"]:
                print(f"    - {regla['regla']} (confianza: {regla['confianza']:.2f})")

        if resultados["patrones_relevantes"]:
            print(f"  Patrones encontrados:")
            for patron in resultados["patrones_relevantes"][:2]:
                print(f"    - {patron['descripcion']}")

        if resultados["episodios_relacionados"]:
            print(f"  Episodios:")
            for ep in resultados["episodios_relacionados"][:2]:
                print(f"    - {ep['descripcion']}")

    # 6. OLVIDO ADAPTATIVO
    print("\n6. OLVIDO ADAPTATIVO (PRIVACIDAD)")
    print("-" * 80)

    cantidad_antes = len(memoria.episodios)
    cantidad_olvidada = memoria.olvidar_episodios_insignificantes(umbral_importancia=0.3)
    cantidad_despues = len(memoria.episodios)

    print(f"Episodios antes: {cantidad_antes}")
    print(f"Episodios olvidados: {cantidad_olvidada}")
    print(f"Episodios después: {cantidad_despues}")

    # 7. RESUMEN FINAL
    print("\n7. RESUMEN FINAL DE MEMORIA JERÁRQUICA")
    print("-" * 80)

    resumen = memoria.obtener_resumen()
    for clave, valor in resumen.items():
        if isinstance(valor, dict):
            print(f"  {clave}:")
            for k, v in valor.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {clave}: {valor}")

    print("\n" + "=" * 80)
    print("Conclusión: Memoria jerárquica permite:")
    print("- Escalabilidad: episódios -> patrones -> reglas")
    print("- Eficiencia: compresión de información")
    print("- Olvido adaptativo: privacidad y relevancia")
    print("- Recuperación en múltiples niveles de abstracción")
    print("=" * 80)


if __name__ == "__main__":
    demo_memoria_jerarquica()
