"""
03_BUFFER_CONTEXTO.PY
=====================

Ejemplo didáctico: Buffer de Contexto y Límites de Contexto en LLMs

Demuestra:
- Implementación de buffer de contexto con ventana móvil
- Manejo de límites de tokens en LLMs
- Estrategias de compresión y selección de información relevante
- FIFO, LRU, y selección por relevancia

REQUISITOS PREVIOS:
- pip install langchain ollama tiktoken
"""

from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import time
from datetime import datetime


# ============================================================================
# TIPOS Y ENUMS
# ============================================================================

class EstrategiaEliminacion(Enum):
    """Estrategias para eliminar contenido cuando buffer está lleno"""
    FIFO = "fifo"  # First In First Out
    LRU = "lru"    # Least Recently Used
    RELEVANCIA = "relevancia"  # Basada en relevancia
    IMPORTANCIA = "importancia"  # Por importancia


@dataclass
class ItemContexto:
    """Representa un item en el buffer de contexto"""
    contenido: str
    tipo: str  # "sistema", "usuario", "asistente", "evento"
    tokens: int = 0
    timestamp: float = field(default_factory=time.time)
    accesos: int = 0
    importancia: float = 0.5  # 0.0 a 1.0
    id: str = ""

    def actualizar_acceso(self) -> None:
        """Registra acceso para LRU"""
        self.accesos += 1
        self.timestamp = time.time()

    def envejecer(self, factor: float = 0.95) -> None:
        """Reduce importancia con edad"""
        self.importancia *= factor

    def estimar_relevancia(self, query: str) -> float:
        """Estima relevancia respecto a una query (0.0 a 1.0)"""
        # Búsqueda simple de palabras clave
        palabras_query = query.lower().split()
        palabras_contenido = self.contenido.lower().split()

        coincidencias = sum(1 for p in palabras_query if p in palabras_contenido)
        relevancia = coincidencias / max(len(palabras_query), 1)

        return min(1.0, relevancia + self.importancia * 0.1)


# ============================================================================
# BUFFER DE CONTEXTO
# ============================================================================

class BufferContexto:
    """
    Buffer de contexto con ventana móvil (sliding window).
    Mantiene información reciente directamente accesible,
    elimina información antigua cuando se alcanza el límite.
    """

    def __init__(
        self,
        max_tokens: int = 2048,
        estrategia: EstrategiaEliminacion = EstrategiaEliminacion.RELEVANCIA,
        margen_seguridad: float = 0.9  # usar 90% del máximo
    ):
        self.max_tokens = max_tokens
        self.estrategia = estrategia
        self.margen_seguridad = margen_seguridad
        self.buffer: deque = deque()
        self.contador_items = 0

    @property
    def tokens_disponibles(self) -> int:
        """Tokens disponibles para nuevo contenido"""
        return int(self.max_tokens * self.margen_seguridad) - self.tokens_usados

    @property
    def tokens_usados(self) -> int:
        """Total de tokens actualmente en buffer"""
        return sum(item.tokens for item in self.buffer)

    @property
    def porcentaje_uso(self) -> float:
        """Porcentaje de utilización del buffer"""
        return (self.tokens_usados / self.max_tokens) * 100

    def agregar(
        self,
        contenido: str,
        tipo: str = "usuario",
        importancia: float = 0.5,
        tokens: Optional[int] = None
    ) -> bool:
        """
        Agrega item al buffer.
        Retorna True si se agregó, False si no había espacio.
        """
        # Estimar tokens si no se proporciona
        if tokens is None:
            # Aproximación simple: ~0.25 tokens por palabra
            tokens = max(10, len(contenido.split()) // 4)

        self.contador_items += 1
        item = ItemContexto(
            contenido=contenido,
            tipo=tipo,
            tokens=tokens,
            importancia=importancia,
            id=f"item_{self.contador_items}"
        )

        # Si hay espacio, simplemente agregar
        if self.tokens_usados + tokens <= int(self.max_tokens * self.margen_seguridad):
            self.buffer.append(item)
            return True

        # Sino, eliminar items según estrategia hasta hacer espacio
        return self._agregar_con_eliminacion(item)

    def _agregar_con_eliminacion(self, nuevo_item: ItemContexto) -> bool:
        """Agrega item eliminando items menos importantes"""
        mientras_hay_espacio = False

        while self.tokens_usados + nuevo_item.tokens > int(self.max_tokens * self.margen_seguridad):
            if not self.buffer:
                break

            # Seleccionar item a eliminar según estrategia
            idx_eliminar = self._seleccionar_para_eliminar()
            if idx_eliminar is not None:
                self.buffer.pop(idx_eliminar)
            else:
                return False

        self.buffer.append(nuevo_item)
        return True

    def _seleccionar_para_eliminar(self) -> Optional[int]:
        """Selecciona índice del item a eliminar según estrategia"""
        if not self.buffer:
            return None

        items_list = list(self.buffer)

        if self.estrategia == EstrategiaEliminacion.FIFO:
            return 0  # Eliminar el primero

        elif self.estrategia == EstrategiaEliminacion.LRU:
            # Eliminar el menos recientemente usado
            idx = min(range(len(items_list)),
                     key=lambda i: (items_list[i].accesos, items_list[i].timestamp))
            return idx

        elif self.estrategia == EstrategiaEliminacion.IMPORTANCIA:
            # Eliminar el menos importante
            idx = min(range(len(items_list)),
                     key=lambda i: items_list[i].importancia)
            return idx

        elif self.estrategia == EstrategiaEliminacion.RELEVANCIA:
            # Eliminar el menos importante considerando antigüedad
            def score(i):
                edad_s = time.time() - items_list[i].timestamp
                edad_factor = 1.0 + (edad_s / 3600)  # más viejo = más fácil de eliminar
                return items_list[i].importancia / edad_factor

            idx = min(range(len(items_list)), key=score)
            return idx

        return 0

    def recuperar(self, query: str) -> List[Dict]:
        """Recupera items relevantes a la query"""
        items_con_relevancia = []

        for item in self.buffer:
            item.actualizar_acceso()
            relevancia = item.estimar_relevancia(query)
            items_con_relevancia.append((item, relevancia))

        # Ordenar por relevancia descendente
        items_con_relevancia.sort(key=lambda x: x[1], reverse=True)

        return [
            {
                "id": item.id,
                "contenido": item.contenido,
                "tipo": item.tipo,
                "relevancia": round(relevancia, 2),
                "tokens": item.tokens
            }
            for item, relevancia in items_con_relevancia
        ]

    def limpiar_expirados(self, edad_maxima_s: float = 3600) -> int:
        """Limpia items que superan edad máxima, retorna cantidad limpiada"""
        ahora = time.time()
        cantidad_inicial = len(self.buffer)

        nuevos_items = deque()
        for item in self.buffer:
            edad = ahora - item.timestamp
            if edad < edad_maxima_s:
                nuevos_items.append(item)

        self.buffer = nuevos_items
        return cantidad_inicial - len(self.buffer)

    def obtener_contexto_para_llm(self) -> str:
        """Obtiene el contexto formateado para pasar al LLM"""
        lineas = []
        for item in self.buffer:
            lineas.append(f"[{item.tipo.upper()}] {item.contenido}")
        return "\n".join(lineas)

    def obtener_resumen(self) -> Dict:
        """Resumen del estado del buffer"""
        return {
            "items_totales": len(self.buffer),
            "tokens_usados": self.tokens_usados,
            "tokens_disponibles": self.tokens_disponibles,
            "porcentaje_uso": round(self.porcentaje_uso, 1),
            "estrategia": self.estrategia.value,
            "items_por_tipo": self._contar_por_tipo()
        }

    def _contar_por_tipo(self) -> Dict[str, int]:
        """Cuenta items por tipo"""
        conteo = {}
        for item in self.buffer:
            conteo[item.tipo] = conteo.get(item.tipo, 0) + 1
        return conteo


# ============================================================================
# COMPRESIÓN DE CONTEXTO
# ============================================================================

class CompresorContexto:
    """
    Comprime el buffer de contexto cuando está muy lleno,
    manteniendo información importante.
    """

    @staticmethod
    def resumir_item(item: ItemContexto) -> str:
        """Resume un item a su esencia"""
        palabras = item.contenido.split()
        # Simplemente tomar primeras palabras si es muy largo
        if len(palabras) > 20:
            return " ".join(palabras[:10]) + "..."
        return item.contenido

    @staticmethod
    def comprimir_buffer(buffer: BufferContexto, ratio: float = 0.7) -> int:
        """
        Comprime buffer a un ratio del tamaño actual.
        Retorna tokens eliminados.
        """
        tokens_objetivo = int(buffer.tokens_usados * ratio)
        tokens_eliminados = 0

        items_ordenados = sorted(
            buffer.buffer,
            key=lambda x: x.importancia
        )

        for item in items_ordenados:
            if buffer.tokens_usados <= tokens_objetivo:
                break

            tokens_eliminados += item.tokens
            buffer.buffer.remove(item)

        return tokens_eliminados

    @staticmethod
    def extraer_resumen_ejecutivo(buffer: BufferContexto) -> str:
        """Extrae los puntos principales del contexto"""
        items_importantes = sorted(
            buffer.buffer,
            key=lambda x: x.importancia,
            reverse=True
        )[:5]

        resumen = "Puntos clave:\n"
        for item in items_importantes:
            resumen += f"- {CompresorContexto.resumir_item(item)}\n"

        return resumen


# ============================================================================
# DEMOSTRACIÓN
# ============================================================================

def demo_buffer_contexto():
    """Demuestra gestión de buffer de contexto"""

    print("=" * 80)
    print("DEMOSTRACIÓN: BUFFER DE CONTEXTO Y LÍMITES EN LLMS")
    print("=" * 80)

    # Crear buffer
    buffer = BufferContexto(
        max_tokens=200,
        estrategia=EstrategiaEliminacion.RELEVANCIA
    )

    print("\n1. AGREGACIÓN DE CONTENIDO AL BUFFER")
    print("-" * 80)

    items_agregar = [
        ("El usuario preguntó sobre precios de laptops", "usuario", 0.9),
        ("Sistema: conectado a base de datos de productos", "sistema", 0.7),
        ("Laptop XPS cuesta $1500 USD", "asistente", 0.85),
        ("Usuario interesado en garantía de 3 años", "usuario", 0.8),
        ("Memoria insuficiente: modelo antiguo descontinuado", "evento", 0.5),
    ]

    for contenido, tipo, importancia in items_agregar:
        exito = buffer.agregar(contenido, tipo=tipo, importancia=importancia)
        print(f"  {'✓' if exito else '✗'} [{tipo}] {contenido[:50]}...")
        print(f"     Uso: {buffer.porcentaje_uso:.1f}% ({buffer.tokens_usados}/{buffer.max_tokens})")

    # Estado actual
    print("\n2. ESTADO ACTUAL DEL BUFFER")
    print("-" * 80)
    resumen = buffer.obtener_resumen()
    for clave, valor in resumen.items():
        print(f"  {clave}: {valor}")

    # Recuperación por relevancia
    print("\n3. RECUPERACIÓN POR RELEVANCIA (QUERY: 'laptop precio')")
    print("-" * 80)
    items_recuperados = buffer.recuperar("laptop precio")
    for item in items_recuperados[:5]:
        print(f"  [relevancia={item['relevancia']}] {item['contenido'][:60]}...")

    # Agregar más contenido hasta llenar el buffer
    print("\n4. PRESIÓN EN BUFFER - AGREGANDO MÁS CONTENIDO")
    print("-" * 80)
    for i in range(5):
        contenido = f"Información adicional del usuario #{i}"
        exito = buffer.agregar(contenido, tipo="usuario", importancia=0.3 + i*0.1)
        print(f"  Item {i+1}: {'agregado' if exito else 'NO agregado'} - "
              f"Uso: {buffer.porcentaje_uso:.1f}%")

    print("\n  Items en buffer después de presión:")
    for item in buffer.buffer:
        print(f"    - {item.contenido[:50]}... (importancia: {item.importancia})")

    # Compresión
    print("\n5. COMPRESIÓN DE CONTEXTO")
    print("-" * 80)
    print(f"  Tokens antes: {buffer.tokens_usados}")
    tokens_liberados = CompresorContexto.comprimir_buffer(buffer, ratio=0.6)
    print(f"  Tokens liberados: {tokens_liberados}")
    print(f"  Tokens después: {buffer.tokens_usados}")
    print(f"  Espacio disponible: {buffer.tokens_disponibles}")

    # Contexto para LLM
    print("\n6. CONTEXTO FORMATEADO PARA LLM")
    print("-" * 80)
    contexto_llm = buffer.obtener_contexto_para_llm()
    print(f"  (Primeros 500 caracteres)")
    print(f"  {contexto_llm[:500]}...")

    # Diferentes estrategias
    print("\n7. COMPARACIÓN DE ESTRATEGIAS")
    print("-" * 80)

    estrategias = [
        EstrategiaEliminacion.FIFO,
        EstrategiaEliminacion.LRU,
        EstrategiaEliminacion.IMPORTANCIA,
        EstrategiaEliminacion.RELEVANCIA
    ]

    for estrategia in estrategias:
        buf = BufferContexto(max_tokens=200, estrategia=estrategia)

        # Agregar items variados
        for j, (contenido, tipo, importancia) in enumerate(items_agregar):
            buf.agregar(contenido, tipo=tipo, importancia=importancia)

        # Agregar mucho hasta forzar eliminación
        for i in range(10):
            buf.agregar(f"Item adicional {i}", importancia=0.2)

        print(f"  {estrategia.value:12} - Items finales: {len(buf.buffer):2}, "
              f"Tokens: {buf.tokens_usados:3}, Uso: {buf.porcentaje_uso:5.1f}%")

    # Resumen ejecutivo
    print("\n8. RESUMEN EJECUTIVO (COMPRESIÓN ABSTRACTIVA)")
    print("-" * 80)
    print(CompresorContexto.extraer_resumen_ejecutivo(buffer))

    print("=" * 80)
    print("Conclusión: El buffer de contexto es crucial para manejar")
    print("límites de tokens en LLMs manteniendo info relevante reciente")
    print("=" * 80)


if __name__ == "__main__":
    demo_buffer_contexto()
