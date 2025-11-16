#!/usr/bin/env python3
"""
EJEMPLO: Teoría de Juegos y Dilema del Prisionero
====================================================

Demuestra conceptos clave de teoría de juegos:
- Equilibrio de Nash
- Estrategia Dominante
- Dilema del Prisionero (Competencia vs Cooperación)
- Batalla de los Sexos (Conflicto de Intereses)

Caso de uso: Negociación entre agentes empresariales
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple, List


# ============================================================================
# DEFINICIONES
# ============================================================================

class Estrategia(Enum):
    """Estrategias disponibles para los agentes"""
    COOPERAR = "cooperar"
    TRAICIONAR = "traicionar"
    ESCALADA = "escalada"
    APACIGUAR = "apaciguar"


@dataclass
class Payoff:
    """Resultado de una interacción"""
    agente_A: int
    agente_B: int
    
    def es_pareto_optimo(self) -> bool:
        """No se puede mejorar a uno sin empeorar al otro"""
        return True  # Simplificación


@dataclass
class Juego:
    """Juego de dos jugadores con payoffs definidos"""
    nombre: str
    matriz: Dict[Tuple[Estrategia, Estrategia], Tuple[int, int]]
    
    def obtener_payoff(self, est_a: Estrategia, est_b: Estrategia) -> Tuple[int, int]:
        """Obtiene payoff para combinación de estrategias"""
        return self.matriz.get((est_a, est_b), (0, 0))


# ============================================================================
# JUEGOS CLÁSICOS
# ============================================================================

def crear_dilema_prisionero() -> Juego:
    """
    El Dilema del Prisionero
    
    Dos prisioneros arrestados sin poder comunicarse.
    Cada uno puede confesar o permanecer callado.
    
    Matriz de Payoffs (años de prisión, negativo = malo):
    
                     Prisionero B
                  Callado | Confesar
    Prisionero A:
    Callado        -1, -1 | -10, 0
    Confesar        0, -10| -5, -5
    
    Equilibrio de Nash: (Confesar, Confesar) = (-5, -5)
    Óptimo de Pareto: (Callado, Callado) = (-1, -1)
    Dilema: Incentivos individuales llevan a peor resultado conjunto
    """
    return Juego(
        nombre="Dilema del Prisionero",
        matriz={
            (Estrategia.COOPERAR, Estrategia.COOPERAR): (-1, -1),      # Ambos callados
            (Estrategia.COOPERAR, Estrategia.TRAICIONAR): (-10, 0),    # B confiesa, A se sacrifica
            (Estrategia.TRAICIONAR, Estrategia.COOPERAR): (0, -10),    # A confiesa, B se sacrifica
            (Estrategia.TRAICIONAR, Estrategia.TRAICIONAR): (-5, -5),  # Ambos confiesan
        }
    )


def crear_batalla_sexos() -> Juego:
    """
    Batalla de los Sexos
    
    Pareja quiere pasar la noche juntos pero con actividades diferentes.
    Ella prefiere ópera, Él prefiere fútbol.
    
    Matriz de Payoffs:
    
              Ella
         Ópera | Fútbol
    Él:
    Ópera    2, 1 | 0, 0
    Fútbol   0, 0 | 1, 2
    
    Dos Equilibrios de Nash: (Ópera, Ópera) y (Fútbol, Fútbol)
    Problema: ¿Cuál elegir? Hay conflicto de coordinación
    """
    return Juego(
        nombre="Batalla de los Sexos",
        matriz={
            (Estrategia.ESCALADA, Estrategia.ESCALADA): (2, 1),    # Él ópera, Ella ópera
            (Estrategia.ESCALADA, Estrategia.APACIGUAR): (0, 0),   # Él ópera, Ella fútbol
            (Estrategia.APACIGUAR, Estrategia.ESCALADA): (0, 0),   # Él fútbol, Ella ópera
            (Estrategia.APACIGUAR, Estrategia.APACIGUAR): (1, 2),  # Él fútbol, Ella fútbol
        }
    )


def crear_halcon_paloma() -> Juego:
    """
    Halcón-Paloma
    
    Juego evolutivo. Dos agentes compiten por recurso.
    Halcón: Agresivo, obtiene recurso si otro no se retira
    Paloma: Pacífico, se retira ante agresión
    
    Matriz de Payoffs:
    
            Otro Agente
         Halcón | Paloma
    Yo:
    Halcón  0, 0 | 3, 1
    Paloma  1, 3 | 2, 2
    
    Este juego tiende a equilibrio mixto (probabilístico)
    """
    return Juego(
        nombre="Halcón-Paloma",
        matriz={
            (Estrategia.ESCALADA, Estrategia.ESCALADA): (0, 0),    # Ambos pelean, todos pierden
            (Estrategia.ESCALADA, Estrategia.APACIGUAR): (3, 1),   # Agresivo gana más
            (Estrategia.APACIGUAR, Estrategia.ESCALADA): (1, 3),   # Pacífico pierde
            (Estrategia.APACIGUAR, Estrategia.APACIGUAR): (2, 2),  # Ambos pacíficos, bueno
        }
    )


def crear_coordinacion() -> Juego:
    """
    Juego de Coordinación
    
    Dos agentes quieren coordinar pero sin comunicación.
    Si eligen lo mismo, ambos ganan; si divergen, pierden.
    
    Matriz de Payoffs:
    
            Agente B
         Opción A | Opción B
    A:
    Opción A   10, 10 | 0, 0
    Opción B    0, 0  | 10, 10
    
    Dos Equilibrios de Nash
    Problema: ¿Cómo coordinar sin comunicación?
    """
    return Juego(
        nombre="Juego de Coordinación",
        matriz={
            (Estrategia.COOPERAR, Estrategia.COOPERAR): (10, 10),
            (Estrategia.COOPERAR, Estrategia.TRAICIONAR): (0, 0),
            (Estrategia.TRAICIONAR, Estrategia.COOPERAR): (0, 0),
            (Estrategia.TRAICIONAR, Estrategia.TRAICIONAR): (10, 10),
        }
    )


# ============================================================================
# ANÁLISIS DE JUEGOS
# ============================================================================

class AnalizadorJuego:
    """Analiza juegos para encontrar equilibrios y estrategias"""
    
    @staticmethod
    def encontrar_estrategia_dominante(juego: Juego, es_primera_fila: bool = True) -> Estrategia:
        """
        Encuentra estrategia dominante si existe.
        Una estrategia es dominante si es mejor sin importar qué haga el otro.
        """
        estrategias = [Estrategia.COOPERAR, Estrategia.TRAICIONAR]
        
        for est1 in estrategias:
            es_dominante = True
            for est2 in estrategias:
                if est1 == est2:
                    continue
                
                # Comparar payoffs
                payoff_est1_vs_est2 = juego.obtener_payoff(est1, est2)
                payoff_otra_vs_est2 = juego.obtener_payoff(
                    Estrategia.TRAICIONAR if est1 == Estrategia.COOPERAR else Estrategia.COOPERAR,
                    est2
                )
                
                # Para primer jugador
                if es_primera_fila:
                    if payoff_est1_vs_est2[0] <= payoff_otra_vs_est2[0]:
                        es_dominante = False
                        break
                else:
                    if payoff_est1_vs_est2[1] <= payoff_otra_vs_est2[1]:
                        es_dominante = False
                        break
            
            if es_dominante:
                return est1
        
        return None
    
    @staticmethod
    def encontrar_equilibrios_nash(juego: Juego) -> List[Tuple[Estrategia, Estrategia]]:
        """
        Equilibrio de Nash: Combinación de estrategias donde ninguno quiere cambiar.
        Ambos están minimizando riesgo o maximizando ganancia dado lo que hace el otro.
        """
        estrategias = [Estrategia.COOPERAR, Estrategia.TRAICIONAR, 
                      Estrategia.ESCALADA, Estrategia.APACIGUAR]
        equilibrios = []
        
        for est_a in estrategias:
            for est_b in estrategias:
                payoff_a, payoff_b = juego.obtener_payoff(est_a, est_b)
                
                # Verificar si es equilibrio de Nash
                es_equilibrio = True
                
                # Verificar si A quiere cambiar
                for alt_a in estrategias:
                    if alt_a != est_a:
                        alt_payoff_a, _ = juego.obtener_payoff(alt_a, est_b)
                        if alt_payoff_a > payoff_a:
                            es_equilibrio = False
                            break
                
                # Verificar si B quiere cambiar
                if es_equilibrio:
                    for alt_b in estrategias:
                        if alt_b != est_b:
                            _, alt_payoff_b = juego.obtener_payoff(est_a, alt_b)
                            if alt_payoff_b > payoff_b:
                                es_equilibrio = False
                                break
                
                if es_equilibrio:
                    equilibrios.append((est_a, est_b))
        
        return equilibrios
    
    @staticmethod
    def encontrar_optimos_pareto(juego: Juego) -> List[Tuple[Estrategia, Estrategia]]:
        """
        Óptimo de Pareto: No se puede mejorar a uno sin empeorar al otro.
        """
        estrategias = [Estrategia.COOPERAR, Estrategia.TRAICIONAR,
                      Estrategia.ESCALADA, Estrategia.APACIGUAR]
        optimos = []
        
        for est_a in estrategias:
            for est_b in estrategias:
                payoff_a, payoff_b = juego.obtener_payoff(est_a, est_b)
                es_optimo = True
                
                # Verificar si existe mejor combinación
                for alt_a in estrategias:
                    for alt_b in estrategias:
                        alt_payoff_a, alt_payoff_b = juego.obtener_payoff(alt_a, alt_b)
                        # Si ambos mejoran, no es Pareto óptimo
                        if alt_payoff_a > payoff_a and alt_payoff_b > payoff_b:
                            es_optimo = False
                            break
                    if not es_optimo:
                        break
                
                if es_optimo:
                    optimos.append((est_a, est_b))
        
        return optimos
    
    @staticmethod
    def imprimir_matriz(juego: Juego):
        """Imprime matriz de payoffs de forma visual"""
        estrategias = [Estrategia.COOPERAR, Estrategia.TRAICIONAR,
                      Estrategia.ESCALADA, Estrategia.APACIGUAR]
        
        print(f"\nMatriz de {juego.nombre}:")
        print("-" * 60)
        
        # Encabezado
        print(f"{'Yo \\ Otro':<15}", end="")
        for est in estrategias:
            print(f"{est.value:<15}", end="")
        print()
        print("-" * 60)
        
        # Filas
        for est_a in estrategias:
            print(f"{est_a.value:<15}", end="")
            for est_b in estrategias:
                payoff_a, payoff_b = juego.obtener_payoff(est_a, est_b)
                print(f"({payoff_a:+2},{payoff_b:+2})      ", end="")
            print()


# ============================================================================
# SIMULACIÓN ITERADA
# ============================================================================

class AgenteJugador:
    """Agente que juega un juego"""
    
    def __init__(self, id: str, estrategia: Estrategia):
        self.id = id
        self.estrategia = estrategia
        self.payoff_acumulado = 0
        self.historial_estrategias = []
    
    def jugar(self) -> Estrategia:
        """Retorna su estrategia actual"""
        self.historial_estrategias.append(self.estrategia)
        return self.estrategia
    
    def cambiar_estrategia(self, nueva: Estrategia):
        """Cambia a nueva estrategia"""
        self.estrategia = nueva
    
    def agregar_payoff(self, payoff: int):
        """Suma payoff al acumulado"""
        self.payoff_acumulado += payoff
    
    def __str__(self):
        return f"{self.id}({self.estrategia.value}):${self.payoff_acumulado}"


class SimuladorIterado:
    """Simula juego iterado entre dos agentes"""
    
    def __init__(self, juego: Juego):
        self.juego = juego
    
    def simular(self, agente_a: AgenteJugador, agente_b: AgenteJugador, 
                rondas: int = 50, permitir_cambio: bool = False) -> Dict:
        """Ejecuta juego iterado"""
        
        resultados = {
            "juego": self.juego.nombre,
            "rondas": rondas,
            "agente_a_payoff": 0,
            "agente_b_payoff": 0,
            "cambios_estrategia": 0,
            "historial": []
        }
        
        for ronda in range(rondas):
            # Ambos juegan
            est_a = agente_a.jugar()
            est_b = agente_b.jugar()
            
            # Obtener payoffs
            payoff_a, payoff_b = self.juego.obtener_payoff(est_a, est_b)
            agente_a.agregar_payoff(payoff_a)
            agente_b.agregar_payoff(payoff_b)
            
            resultados["historial"].append({
                "ronda": ronda,
                "est_a": est_a.value,
                "est_b": est_b.value,
                "payoff_a": payoff_a,
                "payoff_b": payoff_b,
            })
            
            # Posible cambio de estrategia
            if permitir_cambio and ronda % 5 == 0:
                # Cambiar a estrategia del otro si fue mejor
                if payoff_b > payoff_a:
                    agente_a.cambiar_estrategia(est_b)
                    resultados["cambios_estrategia"] += 1
                
                if payoff_a > payoff_b:
                    agente_b.cambiar_estrategia(est_a)
                    resultados["cambios_estrategia"] += 1
        
        resultados["agente_a_payoff"] = agente_a.payoff_acumulado
        resultados["agente_b_payoff"] = agente_b.payoff_acumulado
        
        return resultados


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║  TEORÍA DE JUEGOS: Equilibrios de Nash y Estrategias Dominantes          ║
║                                                                           ║
║  Explorando cómo agentes racionales interactúan en conflictos            ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    analizador = AnalizadorJuego()
    
    # Crear y analizar cada juego
    juegos = [
        crear_dilema_prisionero(),
        crear_batalla_sexos(),
        crear_halcon_paloma(),
        crear_coordinacion(),
    ]
    
    for juego in juegos:
        print(f"\n{'='*70}")
        print(f"JUEGO: {juego.nombre}")
        print(f"{'='*70}")
        
        # Mostrar matriz
        analizador.imprimir_matriz(juego)
        
        # Análisis
        print("\n▶ EQUILIBRIOS DE NASH:")
        equilibrios = analizador.encontrar_equilibrios_nash(juego)
        if equilibrios:
            for est_a, est_b in equilibrios:
                payoff_a, payoff_b = juego.obtener_payoff(est_a, est_b)
                print(f"   • ({est_a.value}, {est_b.value}) → payoffs: {payoff_a}, {payoff_b}")
        else:
            print("   (No hay equilibrios puros)")
        
        print("\n▶ ÓPTIMOS DE PARETO:")
        optimos = analizador.encontrar_optimos_pareto(juego)
        for est_a, est_b in optimos:
            payoff_a, payoff_b = juego.obtener_payoff(est_a, est_b)
            print(f"   • ({est_a.value}, {est_b.value}) → payoffs: {payoff_a}, {payoff_b}")
    
    # Simulación iterada del Dilema del Prisionero
    print(f"\n{'='*70}")
    print("SIMULACIÓN ITERADA: Dilema del Prisionero")
    print(f"{'='*70}")
    
    juego_dp = crear_dilema_prisionero()
    simulador = SimuladorIterado(juego_dp)
    
    # Escenario 1: Ambos cooperan al inicio
    print("\n▶ Escenario 1: Ambos Cooperan al inicio")
    agente_a = AgenteJugador("AgentA", Estrategia.COOPERAR)
    agente_b = AgenteJugador("AgentB", Estrategia.COOPERAR)
    simulador.simular(agente_a, agente_b, rondas=50)
    print(f"   Resultados: {agente_a} | {agente_b}")
    
    # Escenario 2: A coopera, B traiciona
    print("\n▶ Escenario 2: A Coopera, B Traiciona")
    agente_a = AgenteJugador("AgentA", Estrategia.COOPERAR)
    agente_b = AgenteJugador("AgentB", Estrategia.TRAICIONAR)
    simulador.simular(agente_a, agente_b, rondas=50)
    print(f"   Resultados: {agente_a} | {agente_b}")
    
    # Escenario 3: Ambos traicionan (Equilibrio de Nash)
    print("\n▶ Escenario 3: Ambos Traicionan (Equilibrio de Nash)")
    agente_a = AgenteJugador("AgentA", Estrategia.TRAICIONAR)
    agente_b = AgenteJugador("AgentB", Estrategia.TRAICIONAR)
    simulador.simular(agente_a, agente_b, rondas=50)
    print(f"   Resultados: {agente_a} | {agente_b}")
    
    # Conclusión
    print(f"\n{'='*70}")
    print("CONCLUSIÓN")
    print(f"{'='*70}")
    print("""
El DILEMA DEL PRISIONERO muestra por qué la cooperación es difícil:

  • Óptimo conjunto: Ambos cooperan (-1, -1) → Total: -2
  • Equilibrio Nash: Ambos traicionan (-5, -5) → Total: -10
  
  El problema: Si el otro coopera, TRAICIONAR es mejor para mí (-10 vs -1)
  Pero si ambos pensamos así, ¡ambos empeoramos!

IMPLICACIONES PARA AGENTES:
  ✓ Reputación importa (juego iterado favorece cooperación)
  ✓ Comunicación reduce incertidumbre
  ✓ Instituciones pueden forzar cooperación (castigos)
  ✓ Confianza es recurso valioso
    """)


if __name__ == "__main__":
    main()
