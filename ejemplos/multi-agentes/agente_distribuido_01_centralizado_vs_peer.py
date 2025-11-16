#!/usr/bin/env python3
"""
Ejemplo: Centralizado vs Peer-to-Peer
Demuestra diferencias arquitectónicas y sus implicaciones

Escenario: Sistema de control de semáforos en ciudad
"""

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum
import random

class EstadoSemafor(Enum):
    ROJO = "🔴"
    AMARILLO = "🟡"
    VERDE = "🟢"

@dataclass
class Interseccion:
    id: int
    x: int
    y: int
    estado_semafor: EstadoSemafor = EstadoSemafor.ROJO
    vehiculos_esperando: int = 0

# ============================================================================
# ARQUITECTURA CENTRALIZADA
# ============================================================================

class ControladorCentralizado:
    """Un servidor central controla todos los semáforos"""
    
    def __init__(self):
        self.intersecciones: Dict[int, Interseccion] = {}
        self.ciclo_actual = 0
        self.solicitudes_procesadas = 0
    
    def registrar_interseccion(self, interseccion: Interseccion):
        """Intersección se registra con servidor central"""
        self.intersecciones[interseccion.id] = interseccion
        print(f"[CENTRAL] Registrada intersección {interseccion.id}")
    
    def reportar_congestión(self, interseccion_id: int, vehiculos: int):
        """Intersección reporta congestión al central"""
        self.solicitudes_procesadas += 1
        self.intersecciones[interseccion_id].vehiculos_esperando = vehiculos
    
    def calcular_cronograma(self):
        """Central calcula cronograma óptimo global"""
        self.ciclo_actual += 1
        
        # Lógica centralizada: encontrar mejor orden
        intersecciones_ordenadas = sorted(
            self.intersecciones.values(),
            key=lambda i: i.vehiculos_esperando,
            reverse=True
        )
        
        # Asignar verde a la más congestionada
        for i, interseccion in enumerate(self.intersecciones.values()):
            if interseccion == intersecciones_ordenadas[0]:
                interseccion.estado_semafor = EstadoSemafor.VERDE
            else:
                interseccion.estado_semafor = EstadoSemafor.ROJO
    
    def obtener_estado(self, interseccion_id: int) -> EstadoSemafor:
        """Central envía estado a intersección"""
        return self.intersecciones[interseccion_id].estado_semafor

class SemaforoCentralizado:
    """Semáforo controlado por servidor central"""
    
    def __init__(self, id: int, central: ControladorCentralizado):
        self.id = id
        self.central = central
        self.vehiculos_en_cola = random.randint(0, 10)
    
    def reportar_estado(self):
        """Envía información al central (comunicación síncrona)"""
        self.central.reportar_congestión(self.id, self.vehiculos_en_cola)
    
    def recibir_orden(self) -> EstadoSemafor:
        """Recibe orden del central"""
        return self.central.obtener_estado(self.id)
    
    def simular_paso(self):
        """Simula paso de tiempo"""
        if self.recibir_orden() == EstadoSemafor.VERDE:
            # Algunos autos pasan
            autos_que_pasan = min(self.vehiculos_en_cola, 3)
            self.vehiculos_en_cola -= autos_que_pasan
        
        # Llegan nuevos autos
        self.vehiculos_en_cola += random.randint(0, 2)

# ============================================================================
# ARQUITECTURA PEER-TO-PEER (DESCENTRALIZADA)
# ============================================================================

class SemaforoDescentralizado:
    """Semáforo autónomo que comunica con vecinos directamente"""
    
    def __init__(self, id: int, x: int, y: int):
        self.id = id
        self.x = x
        self.y = y
        self.estado = EstadoSemafor.ROJO
        self.vehiculos_en_cola = random.randint(0, 10)
        self.vecinos: List['SemaforoDescentralizado'] = []
        self.estado_vecinos: Dict[int, int] = {}  # Colas conocidas de vecinos
    
    def registrar_vecino(self, vecino: 'SemaforoDescentralizado'):
        """Conecta directamente con semáforo vecino"""
        self.vecinos.append(vecino)
    
    def comunicar_con_vecinos(self):
        """Comunica directamente con vecinos (P2P)"""
        for vecino in self.vecinos:
            self.estado_vecinos[vecino.id] = vecino.vehiculos_en_cola
    
    def decidir_estado(self):
        """Decide localmente si estar en verde o rojo"""
        # Estrategia local: si tengo más autos que vecinos, me pongo verde
        autos_vecinos = sum(self.estado_vecinos.values())
        
        if self.vehiculos_en_cola > autos_vecinos:
            self.estado = EstadoSemafor.VERDE
        else:
            self.estado = EstadoSemafor.ROJO
    
    def simular_paso(self):
        """Simula paso de tiempo"""
        # Comunicar con vecinos
        self.comunicar_con_vecinos()
        
        # Tomar decisión local
        self.decidir_estado()
        
        # Simular tráfico
        if self.estado == EstadoSemafor.VERDE:
            autos_que_pasan = min(self.vehiculos_en_cola, 3)
            self.vehiculos_en_cola -= autos_que_pasan
        
        self.vehiculos_en_cola += random.randint(0, 2)

# ============================================================================
# SIMULACIÓN
# ============================================================================

def simular_centralizado(ciclos=20):
    """Simula sistema centralizado"""
    print("\n" + "="*70)
    print("SIMULACIÓN 1: ARQUITECTURA CENTRALIZADA")
    print("="*70)
    
    central = ControladorCentralizado()
    
    # Crear semáforos
    semaforos = []
    for i in range(4):
        intersec = Interseccion(id=i, x=i%2, y=i//2)
        central.registrar_interseccion(intersec)
        semaforos.append(SemaforoCentralizado(i, central))
    
    print(f"\n✓ Creados {len(semaforos)} semáforos conectados a servidor central")
    print(f"✓ Punto único de fallo: SERVIDOR CENTRAL")
    print(f"✓ Latencia de comunicación: Central es autoritario")
    
    total_espera = 0
    
    for ciclo in range(ciclos):
        # Fase 1: Reportar
        for semafo in semaforos:
            semafo.reportar_estado()
        
        # Fase 2: Central calcula
        central.calcular_cronograma()
        
        # Fase 3: Semáforos ejecutan
        for semafo in semaforos:
            semafo.simular_paso()
            total_espera += semafo.vehiculos_en_cola
        
        if ciclo % 5 == 0:
            print(f"\nCiclo {ciclo}: Solicitudes procesadas: {central.solicitudes_procesadas}")
            for i, s in enumerate(semaforos):
                print(f"  Semáforo {i}: {s.central.intersecciones[i].estado_semafor.value} "
                      f"Cola: {s.vehiculos_en_cola} autos")
    
    print(f"\n📊 RESULTADOS CENTRALIZADO:")
    print(f"   Total espera acumulada: {total_espera}")
    print(f"   Promedio por ciclo: {total_espera/ciclos:.1f}")

def simular_descentralizado(ciclos=20):
    """Simula sistema P2P descentralizado"""
    print("\n" + "="*70)
    print("SIMULACIÓN 2: ARQUITECTURA DESCENTRALIZADA (P2P)")
    print("="*70)
    
    # Crear semáforos en grid 2x2
    semaforos = [
        SemaforoDescentralizado(0, 0, 0),
        SemaforoDescentralizado(1, 1, 0),
        SemaforoDescentralizado(2, 0, 1),
        SemaforoDescentralizado(3, 1, 1),
    ]
    
    # Conectar directamente (vecinos)
    # (0,0) conecta con (1,0) y (0,1)
    semaforos[0].registrar_vecino(semaforos[1])
    semaforos[0].registrar_vecino(semaforos[2])
    # (1,0) conecta con (0,0) y (1,1)
    semaforos[1].registrar_vecino(semaforos[0])
    semaforos[1].registrar_vecino(semaforos[3])
    # etc
    semaforos[2].registrar_vecino(semaforos[0])
    semaforos[2].registrar_vecino(semaforos[3])
    semaforos[3].registrar_vecino(semaforos[1])
    semaforos[3].registrar_vecino(semaforos[2])
    
    print(f"\n✓ Creados {len(semaforos)} semáforos independientes")
    print(f"✓ NO hay punto único de fallo")
    print(f"✓ Decisiones locales autónomas")
    print(f"✓ Comunicación directa P2P entre vecinos")
    
    total_espera = 0
    
    for ciclo in range(ciclos):
        # Cada semáforo actúa autónomamente
        for semafo in semaforos:
            semafo.simular_paso()
            total_espera += semafo.vehiculos_en_cola
        
        if ciclo % 5 == 0:
            print(f"\nCiclo {ciclo}:")
            for i, s in enumerate(semaforos):
                print(f"  Semáforo {i}: {s.estado.value} "
                      f"Cola: {s.vehiculos_en_cola} autos")
    
    print(f"\n📊 RESULTADOS DESCENTRALIZADO:")
    print(f"   Total espera acumulada: {total_espera}")
    print(f"   Promedio por ciclo: {total_espera/ciclos:.1f}")

def main():
    print("\n" + "="*70)
    print("COMPARATIVA: CENTRALIZADO vs DESCENTRALIZADO")
    print("="*70)
    print("\nCaso: Sistema de control de semáforos de ciudad")
    print("\nCentralizado:")
    print("  - Un servidor central toma todas las decisiones")
    print("  - Todos los semáforos reportan y reciben órdenes")
    print("  - Decisions óptimas globales pero punto único de fallo")
    print("\nDescentralizado (P2P):")
    print("  - Cada semáforo decide autónomamente")
    print("  - Comunica directamente con vecinos cercanos")
    print("  - Más resiliente pero decisions subóptimas locales")
    
    simular_centralizado(ciclos=20)
    simular_descentralizado(ciclos=20)
    
    print("\n" + "="*70)
    print("CONCLUSIONES")
    print("="*70)
    print("""
Centralizado:
  ✓ Control global óptimo
  ✓ Fácil de coordinar
  ✗ Punto único fallo crítico
  ✗ Cuello de botella en servidor
  ✗ Escalabilidad limitada

Descentralizado (P2P):
  ✓ Altamente resiliente
  ✓ Escalable fácilmente
  ✓ Sin punto único fallo
  ✗ Control subóptimo local
  ✗ Coordinación compleja
  ✗ Potencial inconsistencia

Elección: Depende del caso de uso
    """)

if __name__ == "__main__":
    main()
