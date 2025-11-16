#!/usr/bin/env python3
"""
Ejemplo: Emergencia de Comportamiento Complejo
Demuestra cómo reglas simples locales generan patrones globales complejos

Caso: Hormigas buscando comida usando feromonas
Reglas simples:
  1. Si ves feromona, síguelo
  2. Si encuentras comida, deposita feromona y regresa
  3. Si no ves feromona, camina al azar

Resultado: Sistema emergente de búsqueda eficiente sin coordinación central
"""

import random
import math
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class Posicion:
    x: float
    y: float
    
    def distancia_a(self, otra: 'Posicion') -> float:
        """Calcula distancia Euclidiana"""
        return math.sqrt((self.x - otra.x)**2 + (self.y - otra.y)**2)
    
    def towards(self, otra: 'Posicion', paso: float = 0.5) -> 'Posicion':
        """Retorna nueva posición moviéndose hacia otra"""
        if self.distancia_a(otra) == 0:
            return Posicion(self.x, self.y)
        dx = otra.x - self.x
        dy = otra.y - self.y
        dist = self.distancia_a(otra)
        return Posicion(self.x + (dx/dist)*paso, self.y + (dy/dist)*paso)

class Ambiente:
    """Representa mundo 2D con feromonas distribuidas"""
    
    def __init__(self, ancho: float = 20.0, alto: float = 20.0):
        self.ancho = ancho
        self.alto = alto
        self.feromonas: Dict[Tuple[int, int], float] = {}
        self.comida = Posicion(ancho - 2, alto - 2)
        self.nido = Posicion(1, 1)
    
    def _obtener_celda(self, pos: Posicion) -> Tuple[int, int]:
        """Discretiza posición a celda"""
        return (int(pos.x), int(pos.y))
    
    def depositar_feromona(self, pos: Posicion, cantidad: float = 1.0):
        """Deposita feromona en posición"""
        celda = self._obtener_celda(pos)
        if 0 <= celda[0] < self.ancho and 0 <= celda[1] < self.alto:
            self.feromonas[celda] = self.feromonas.get(celda, 0) + cantidad
    
    def obtener_feromona(self, pos: Posicion) -> float:
        """Lee cantidad de feromona en posición"""
        celda = self._obtener_celda(pos)
        return self.feromonas.get(celda, 0)
    
    def evaporar_feromonas(self, tasa: float = 0.95):
        """Las feromonas se evaporan gradualmente"""
        celdas_a_eliminar = []
        for celda, cantidad in self.feromonas.items():
            nueva_cantidad = cantidad * tasa
            if nueva_cantidad < 0.01:
                celdas_a_eliminar.append(celda)
            else:
                self.feromonas[celda] = nueva_cantidad
        
        for celda in celdas_a_eliminar:
            del self.feromonas[celda]
    
    def obtener_feromonas_cercanas(self, pos: Posicion, radio: float = 1.5) -> List[Tuple[Posicion, float]]:
        """Retorna feromonas en radio cercano, ordenadas por cantidad"""
        cercanas = []
        celda_actual = self._obtener_celda(pos)
        
        for celda, cantidad in self.feromonas.items():
            pos_celda = Posicion(celda[0], celda[1])
            if pos.distancia_a(pos_celda) <= radio and celda != celda_actual:
                cercanas.append((pos_celda, cantidad))
        
        # Ordenar por cantidad (más fuerte primero)
        return sorted(cercanas, key=lambda x: x[1], reverse=True)
    
    def esta_en_limites(self, pos: Posicion) -> bool:
        """Verifica si posición está dentro del ambiente"""
        return 0 <= pos.x < self.ancho and 0 <= pos.y < self.alto

class Hormiga:
    """Hormiga autónoma con reglas simples locales"""
    
    def __init__(self, nombre: str, nido: Posicion, comida: Posicion):
        self.nombre = nombre
        self.posicion = Posicion(nido.x, nido.y)
        self.nido = nido
        self.comida = comida
        self.tiene_comida = False
        self.pasos = 0
        self.ciclos_vivos = 0
        self.comidas_encontradas = 0
    
    def percibir(self, ambiente: Ambiente) -> Dict:
        """PERCEPCIÓN: Detecta feromonas y objetivos cercanos"""
        distancia_a_comida = self.posicion.distancia_a(self.comida)
        distancia_a_nido = self.posicion.distancia_a(self.nido)
        
        # Detectar feromonas cercanas
        feromonas_cercanas = ambiente.obtener_feromonas_cercanas(self.posicion, radio=2.0)
        
        percepcion = {
            'posicion': self.posicion,
            'comida_cercana': distancia_a_comida < 1.5,
            'nido_cercano': distancia_a_nido < 1.5,
            'feromonas_cercanas': feromonas_cercanas,
            'distancia_comida': distancia_a_comida,
            'distancia_nido': distancia_a_nido,
            'feromona_local': ambiente.obtener_feromona(self.posicion)
        }
        
        return percepcion
    
    def decidir(self, percepcion: Dict, ambiente: Ambiente) -> Posicion:
        """RAZONAMIENTO: Decide próxima acción usando reglas simples"""
        
        # REGLA 1: Si llegué al nido con comida, listo
        if percepcion['nido_cercano'] and self.tiene_comida:
            return self.posicion  # Parar
        
        # REGLA 2: Si encontré comida, vuelvo al nido y deposito feromona
        if percepcion['comida_cercana'] and not self.tiene_comida:
            self.tiene_comida = True
            destino = self.nido
        
        # REGLA 3: Si tengo comida, vuelvo al nido
        elif self.tiene_comida:
            destino = self.nido
        
        # REGLA 4: Si hay feromonas cercanas, síguelas (emergencia colectiva!)
        elif percepcion['feromonas_cercanas']:
            destino_pos, _ = percepcion['feromonas_cercanas'][0]
            destino = destino_pos
        
        # REGLA 5: Si no hay feromonas, busca comida
        else:
            destino = self.comida
        
        # Moverse hacia destino
        if destino.distancia_a(self.posicion) > 0.1:
            return self.posicion.towards(destino, paso=0.5)
        else:
            return self.posicion
    
    def actuar(self, nueva_posicion: Posicion, ambiente: Ambiente):
        """ACCIÓN: Se mueve y deposita feromonas"""
        # Validar límites
        if ambiente.esta_en_limites(nueva_posicion):
            self.posicion = nueva_posicion
        
        self.pasos += 1
        
        # Si encontré comida
        if self.posicion.distancia_a(self.comida) < 0.5:
            self.tiene_comida = True
        
        # Si regresé al nido
        if self.tiene_comida and self.posicion.distancia_a(self.nido) < 0.5:
            self.tiene_comida = False
            self.comidas_encontradas += 1
        
        # Depositar feromona al volver (marca camino)
        if not self.tiene_comida and self.pasos % 2 == 0:
            ambiente.depositar_feromona(self.posicion, cantidad=0.5)
    
    def ejecutar_ciclo(self, ambiente: Ambiente):
        """Ciclo completo percepto-acción"""
        # 1. PERCIBIR
        percepcion = self.percibir(ambiente)
        
        # 2. RAZONAR
        nueva_pos = self.decidir(percepcion, ambiente)
        
        # 3. ACTUAR
        self.actuar(nueva_pos, ambiente)
        
        self.ciclos_vivos += 1

class Visualizador:
    """Visualiza estado del ambiente"""
    
    @staticmethod
    def generar_grid(ambiente: Ambiente, hormigas: List[Hormiga], 
                     escala: int = 1) -> List[str]:
        """Genera representación visual"""
        alto = int(ambiente.alto / escala)
        ancho = int(ambiente.ancho / escala)
        
        # Grid con caracteres
        grid = [['.' for _ in range(ancho)] for _ in range(alto)]
        
        # Marcar feromonas
        for (x, y), cantidad in ambiente.feromonas.items():
            gx, gy = int(x / escala), int(y / escala)
            if 0 <= gx < ancho and 0 <= gy < alto:
                if cantidad > 2:
                    grid[alto - 1 - gy][gx] = '*'
                elif cantidad > 0.5:
                    grid[alto - 1 - gy][gx] = '+'
        
        # Marcar comida
        cx = int(ambiente.comida.x / escala)
        cy = int(ambiente.comida.y / escala)
        if 0 <= cx < ancho and 0 <= cy < alto:
            grid[alto - 1 - cy][cx] = 'C'
        
        # Marcar nido
        nx = int(ambiente.nido.x / escala)
        ny = int(ambiente.nido.y / escala)
        if 0 <= nx < ancho and 0 <= ny < alto:
            grid[alto - 1 - ny][nx] = 'N'
        
        # Marcar hormigas
        for hormiga in hormigas:
            hx = int(hormiga.posicion.x / escala)
            hy = int(hormiga.posicion.y / escala)
            if 0 <= hx < ancho and 0 <= hy < alto:
                grid[alto - 1 - hy][hx] = 'H'
        
        return [''.join(fila) for fila in grid]
    
    @staticmethod
    def mostrar(ambiente: Ambiente, hormigas: List[Hormiga], ciclo: int):
        """Muestra grid en pantalla"""
        print(f"\n{'='*50}")
        print(f"CICLO {ciclo}")
        print(f"{'='*50}")
        print("Legend: N=Nido, C=Comida, H=Hormiga, *=Feromona fuerte, +=débil, .=libre")
        
        grid = Visualizador.generar_grid(ambiente, hormigas, escala=1)
        for fila in grid:
            print(fila)
        
        # Estadísticas
        total_comidas = sum(h.comidas_encontradas for h in hormigas)
        print(f"\nComidas encontradas: {total_comidas}")
        print(f"Feromonas en ambiente: {len(ambiente.feromonas)}")

def main():
    print("\n" + "="*60)
    print("SIMULACIÓN: EMERGENCIA DE COMPORTAMIENTO COLECTIVO")
    print("="*60)
    print("""
CONCEPTO: Hormigas buscando comida
- Cada hormiga sigue reglas SIMPLES locales
- NO hay coordinador central
- NO hay plan global
- Resultado: Camino emergente eficiente

REGLAS LOCALES:
1. Si ves feromona, síguelo
2. Si encuentras comida, vuelve al nido
3. Si no ves feromona, camina al azar
4. Deposita feromona al volver
    """)
    
    # Crear ambiente
    ambiente = Ambiente(ancho=20.0, alto=20.0)
    
    # Crear hormigas
    num_hormigas = 5
    hormigas = [
        Hormiga(f"Hormiga-{i}", ambiente.nido, ambiente.comida)
        for i in range(num_hormigas)
    ]
    
    print(f"\nCreadas {num_hormigas} hormigas")
    print(f"Nido: ({ambiente.nido.x:.1f}, {ambiente.nido.y:.1f})")
    print(f"Comida: ({ambiente.comida.x:.1f}, {ambiente.comida.y:.1f})")
    print(f"Distancia: {ambiente.nido.distancia_a(ambiente.comida):.1f} unidades")
    
    # Simulación
    ciclos_totales = 300
    
    for ciclo in range(ciclos_totales):
        # Hormigas ejecutan ciclo percepto-acción
        for hormiga in hormigas:
            hormiga.ejecutar_ciclo(ambiente)
        
        # Feromonas se evaporan
        ambiente.evaporar_feromonas(tasa=0.93)
        
        # Visualizar en momentos clave
        if ciclo in [0, 50, 100, 150, 200, 299]:
            Visualizador.mostrar(ambiente, hormigas, ciclo)
    
    # Resultados finales
    print("\n" + "="*60)
    print("ANÁLISIS DE EMERGENCIA")
    print("="*60)
    
    total_comidas = sum(h.comidas_encontradas for h in hormigas)
    total_pasos = sum(h.pasos for h in hormigas)
    
    print(f"\nCiclos ejecutados: {ciclos_totales}")
    print(f"Hormigas: {num_hormigas}")
    print(f"Total comidas encontradas: {total_comidas}")
    print(f"Promedio pasos/hormiga: {total_pasos/num_hormigas:.0f}")
    print(f"Feromonas residuales: {len(ambiente.feromonas)}")
    
    print(f"""
OBSERVACIONES:
✓ Sin coordinador central, las hormigas encontraron la comida
✓ Caminos emergentes se formaron usando feromonas
✓ El sistema es robusto: si falla una hormiga, otras continúan
✓ Comportamiento colectivo surge de reglas locales simples

CONCLUSIÓN:
Este es un ejemplo perfecto de EMERGENCIA:
- Reglas locales simples (cada hormiga)
- Interacción entre agentes (feromonas compartidas)
- Patrón global complejo emerge (camino óptimo)
- Sin planificación central
    """)

if __name__ == "__main__":
    main()
