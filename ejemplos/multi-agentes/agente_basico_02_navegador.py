#!/usr/bin/env python3
"""
Ejemplo 2: Agente Navegador en Cuadrícula
Demuestra autonomía, razonamiento y percepción parcial del ambiente

Concepto: Un agente autónomo navega en una cuadrícula 5x5 hacia un objetivo,
evitando obstáculos usando solo información local.
"""

import random
from enum import Enum
from typing import Tuple, Dict

class Direccion(Enum):
    """Direcciones posibles de movimiento"""
    NORTE = (0, 1)
    SUR = (0, -1)
    ESTE = (1, 0)
    OESTE = (-1, 0)

class Ambiente:
    """Representa el ambiente: cuadrícula con objetivo y obstáculos"""
    
    def __init__(self, tamaño=5):
        self.tamaño = tamaño
        self.objetivo = (tamaño - 1, tamaño - 1)
        # Obstáculos fijos en el ambiente
        self.obstaculos = {(2, 2), (2, 3), (3, 2)}
    
    def es_valido(self, posicion: Tuple[int, int]) -> bool:
        """Verifica si una posición es válida (dentro de límites y sin obstáculos)"""
        x, y = posicion
        return (0 <= x < self.tamaño and 
                0 <= y < self.tamaño and 
                posicion not in self.obstaculos)
    
    def distancia_manhattan(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calcula distancia Manhattan entre dos posiciones"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def obtener_vecinos_validos(self, posicion: Tuple[int, int]) -> list:
        """Retorna posiciones válidas adyacentes (para búsqueda local)"""
        vecinos = []
        for direccion in Direccion:
            dx, dy = direccion.value
            nueva_pos = (posicion[0] + dx, posicion[1] + dy)
            if self.es_valido(nueva_pos):
                vecinos.append(nueva_pos)
        return vecinos
    
    def visualizar(self, pos_agente: Tuple[int, int]) -> str:
        """Genera una representación visual del ambiente"""
        grid = []
        for y in range(self.tamaño - 1, -1, -1):  # De arriba a abajo
            fila = []
            for x in range(self.tamaño):
                pos = (x, y)
                if pos == pos_agente:
                    fila.append("A")  # Agente
                elif pos == self.objetivo:
                    fila.append("O")  # Objetivo
                elif pos in self.obstaculos:
                    fila.append("X")  # Obstáculo
                else:
                    fila.append("·")  # Espacio libre
            grid.append(" ".join(fila))
        return "\n".join(grid)


class AgenteNavigador:
    """Agente autónomo que navega hacia objetivo"""
    
    def __init__(self, nombre: str, posicion_inicial: Tuple[int, int]):
        self.nombre = nombre
        self.posicion = posicion_inicial
        self.objetivo_alcanzado = False
        self.pasos_ejecutados = 0
        self.historial_movimientos = [posicion_inicial]
        self.decisiones_tomadas = []
    
    def percibir(self, ambiente: Ambiente) -> Dict:
        """
        FASE 1: PERCEPCIÓN
        El agente percibe su estado actual y distancia al objetivo.
        (Percepción parcial: solo conoce su posición y meta)
        """
        distancia = ambiente.distancia_manhattan(
            self.posicion, 
            ambiente.objetivo
        )
        
        percepcion = {
            'posicion_actual': self.posicion,
            'objetivo': ambiente.objetivo,
            'distancia_a_objetivo': distancia,
            'en_objetivo': self.posicion == ambiente.objetivo,
            'vecinos_validos': ambiente.obtener_vecinos_validos(self.posicion)
        }
        
        return percepcion
    
    def razonar(self, percepcion: Dict, ambiente: Ambiente) -> Tuple[int, int]:
        """
        FASE 2: RAZONAMIENTO
        El agente decide hacia dónde moverse usando una estrategia racional:
        Mover-se hacia el objetivo tomando el camino más directo (greedy approach).
        """
        if percepcion['en_objetivo']:
            return None  # Ya estoy en el objetivo
        
        vecinos = percepcion['vecinos_validos']
        objetivo = percepcion['objetivo']
        
        if not vecinos:
            return None  # No hay movimientos posibles (atrapado)
        
        # Estrategia racional greedy: elegir vecino más cercano al objetivo
        mejor_vecino = min(
            vecinos,
            key=lambda v: ambiente.distancia_manhattan(v, objetivo)
        )
        
        razon = {
            'estrategia': 'Greedy (minimizar distancia)',
            'objetivo': objetivo,
            'opciones': vecinos,
            'elegido': mejor_vecino,
            'distancia_nueva': ambiente.distancia_manhattan(mejor_vecino, objetivo)
        }
        
        return mejor_vecino, razon
    
    def actuar(self, accion, ambiente: Ambiente) -> bool:
        """
        FASE 3: ACCIÓN
        El agente se mueve a la nueva posición
        """
        if accion is None:
            return False  # No hay acción válida
        
        nueva_pos = accion
        
        # Verificar validez (debería ser válida si viene de razonar)
        if ambiente.es_valido(nueva_pos):
            self.posicion = nueva_pos
            self.pasos_ejecutados += 1
            self.historial_movimientos.append(nueva_pos)
            return True
        
        return False
    
    def ejecutar_ciclo(self, ambiente: Ambiente) -> bool:
        """
        Ejecuta un ciclo completo: percibir → razonar → actuar
        Retorna False si no hay más movimientos posibles
        """
        # 1. PERCIBIR
        percepcion = self.percibir(ambiente)
        
        # 2. RAZONAR
        resultado = self.razonar(percepcion, ambiente)
        
        if resultado is None:
            self.objetivo_alcanzado = True
            return False
        
        accion, razon = resultado
        self.decisiones_tomadas.append(razon)
        
        # 3. ACTUAR
        exito = self.actuar(accion, ambiente)
        
        return exito and not self.objetivo_alcanzado
    
    def obtener_resumen(self) -> str:
        """Retorna resumen de la navegación"""
        resumen = f"\n{'='*60}\n"
        resumen += f"RESUMEN - Agente: {self.nombre}\n"
        resumen += f"{'='*60}\n"
        resumen += f"Posición inicial: {self.historial_movimientos[0]}\n"
        resumen += f"Posición final: {self.posicion}\n"
        resumen += f"Pasos ejecutados: {self.pasos_ejecutados}\n"
        resumen += f"Objetivo alcanzado: {'SÍ ✓' if self.objetivo_alcanzado else 'NO ✗'}\n"
        resumen += f"Camino recorrido: {' → '.join(str(p) for p in self.historial_movimientos)}\n"
        return resumen


# ============================================================================
# SIMULACIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("SIMULACIÓN: AGENTE NAVEGADOR AUTÓNOMO")
    print("="*60)
    
    print("\nCaracterísticas del agente:")
    print("  ✓ Autónomo: Toma decisiones sin supervisión")
    print("  ✓ Racional: Usa estrategia greedy (minimiza distancia)")
    print("  ✓ Perceptivo: Conoce su posición y objetivo")
    print("  ✓ Reactivo: Ciclo percepto-acción continuo")
    
    # Crear ambiente
    ambiente = Ambiente(tamaño=5)
    
    print("\n" + "-"*60)
    print("AMBIENTE INICIAL:")
    print("-"*60)
    print("(A=Agente, O=Objetivo, X=Obstáculo, ·=Libre)")
    
    # Mostrar estado inicial (antes de empezar)
    pos_inicial = (0, 0)
    print(f"\nPosición inicial agente: {pos_inicial}")
    print(f"Objetivo: {ambiente.objetivo}")
    print(f"Obstáculos: {ambiente.obstaculos}\n")
    print(ambiente.visualizar(pos_inicial))
    
    # Crear agente
    agente = AgenteNavigador("Bot-Alpha", pos_inicial)
    
    # Ejecutar ciclos
    print("\n" + "-"*60)
    print("EJECUCIÓN DE CICLOS PERCEPTO-ACCIÓN:")
    print("-"*60)
    
    ciclo_num = 0
    max_ciclos = 20
    
    while ciclo_num < max_ciclos:
        ciclo_num += 1
        
        print(f"\n[CICLO {ciclo_num}]")
        print(f"  Posición: {agente.posicion}")
        
        # Ejecutar ciclo
        continuar = agente.ejecutar_ciclo(ambiente)
        
        if not continuar:
            if agente.objetivo_alcanzado:
                print(f"  ✓ OBJETIVO ALCANZADO")
            else:
                print(f"  ✗ Sin movimientos posibles")
            break
    
    # Mostrar estado final
    print("\n" + "-"*60)
    print("AMBIENTE FINAL:")
    print("-"*60)
    print(ambiente.visualizar(agente.posicion))
    
    # Mostrar resumen
    print(agente.obtener_resumen())
    
    # Explicación
    print("\nINTERPRETACIÓN:")
    print("  • El agente ejecutó ciclos percepto-acción autónomamente")
    print("  • Cada ciclo: percibió posición → razonó estrategia → actuó")
    print("  • Sin intervención externa, solo con su lógica racional")
    print("  • Llegó al objetivo evitando obstáculos automáticamente\n")
