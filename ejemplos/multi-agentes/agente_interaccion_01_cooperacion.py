#!/usr/bin/env python3
"""
EJEMPLO: Cooperación vs Colaboración vs Competencia
=========================================================

Demuestra las tres formas de interacción entre agentes:
1. Cooperación: Agentes sin comunicación explícita
2. Colaboración: Agentes coordinados con comunicación
3. Competencia: Agentes con objetivos contradictorios

Caso de uso: Equipo de robots recogiendo objetos en una fábrica
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict
from random import randint, choice

# ============================================================================
# MODELOS DE DATOS
# ============================================================================

class TipoInteraccion(Enum):
    """Tipos de interacción entre agentes"""
    COOPERACION = "cooperacion"
    COLABORACION = "colaboracion"
    COMPETENCIA = "competencia"


@dataclass
class Objeto:
    """Objeto a recoger en la fábrica"""
    id: int
    peso: int  # 1-10
    valor: int  # 1-100
    recolector: str = None  # ID del agente que lo recogió
    
    def __str__(self):
        return f"Obj{self.id}(p={self.peso},v={self.valor})"


@dataclass
class Robot:
    """Robot trabajando en la fábrica"""
    id: str
    capacidad: int = 50  # Peso máximo que puede llevar
    carga_actual: int = field(default=0)
    objetos: List[Objeto] = field(default_factory=list)
    valor_total: int = 0
    es_activo: bool = True
    
    def puede_cargar(self, objeto: Objeto) -> bool:
        """Verifica si el robot puede cargar el objeto"""
        return self.carga_actual + objeto.peso <= self.capacidad
    
    def cargar_objeto(self, objeto: Objeto) -> bool:
        """Carga un objeto si es posible"""
        if self.puede_cargar(objeto):
            objeto.recolector = self.id
            self.objetos.append(objeto)
            self.carga_actual += objeto.peso
            self.valor_total += objeto.valor
            return True
        return False
    
    def descargar_todos(self):
        """Descarga todos los objetos en almacén"""
        self.carga_actual = 0
        self.objetos.clear()
    
    def __str__(self):
        return f"Robot{self.id}(cap={self.capacidad},actual={self.carga_actual},val={self.valor_total})"


@dataclass
class Ambiente:
    """Ambiente de la fábrica con objetos distribuidos"""
    objetos: List[Objeto] = field(default_factory=list)
    robots: Dict[str, Robot] = field(default_factory=dict)
    ciclo: int = 0
    modo_interaccion: TipoInteraccion = TipoInteraccion.COOPERACION
    
    def agregar_objeto(self, peso: int, valor: int) -> Objeto:
        """Agrega un nuevo objeto al ambiente"""
        obj = Objeto(id=len(self.objetos), peso=peso, valor=valor)
        self.objetos.append(obj)
        return obj
    
    def agregar_robot(self, robot: Robot):
        """Agrega un robot al ambiente"""
        self.robots[robot.id] = robot
    
    def objetos_sin_recoger(self) -> List[Objeto]:
        """Retorna objetos que no han sido recogidos"""
        return [obj for obj in self.objetos if obj.recolector is None]


# ============================================================================
# ESTRATEGIAS DE INTERACCIÓN
# ============================================================================

class EstrategiaCooperacion:
    """
    COOPERACIÓN: Sin comunicación explícita
    Cada robot recoge cualquier objeto que vea, asumiendo que otros hacen lo mismo
    Resultado: Distribución equitativa sin coordinación
    """
    
    @staticmethod
    def ejecutar_ciclo(ambiente: Ambiente):
        """Un ciclo de cooperación"""
        objetos_disponibles = ambiente.objetos_sin_recoger()
        
        if not objetos_disponibles:
            return
        
        # Cada robot intenta recoger el objeto más cercano (aleatorio)
        for robot in ambiente.robots.values():
            if not robot.es_activo:
                continue
            
            # Busca objeto aleatorio que pueda cargar
            objetos_posibles = [obj for obj in objetos_disponibles 
                              if robot.puede_cargar(obj)]
            
            if objetos_posibles:
                # Sin comunicación: cada uno toma el primero que encuentra
                objeto = choice(objetos_posibles)
                if robot.cargar_objeto(objeto):
                    objetos_disponibles.remove(objeto)
        
        # Robots llenos descargan
        for robot in ambiente.robots.values():
            if robot.carga_actual >= robot.capacidad * 0.8:
                robot.descargar_todos()


class EstrategiaColaboracion:
    """
    COLABORACIÓN: Con comunicación y coordinación explícita
    Robots se comunican para asignar tareas evitando duplicación
    Resultado: Eficiencia mejorada, menos conflictos
    """
    
    @staticmethod
    def ejecutar_ciclo(ambiente: Ambiente):
        """Un ciclo de colaboración con asignación coordinada"""
        objetos_disponibles = ambiente.objetos_sin_recoger()
        
        if not objetos_disponibles:
            return
        
        # Fase 1: Negociación
        asignaciones = {}  # objeto_id -> robot_id
        
        for robot in ambiente.robots.values():
            if not robot.es_activo:
                continue
            
            # Robot declara su capacidad disponible
            espacio_disponible = robot.capacidad - robot.carga_actual
            
            # Encuentra objetos que caben
            objetos_candidatos = [obj for obj in objetos_disponibles
                                if obj.peso <= espacio_disponible 
                                and obj.id not in asignaciones]
            
            # Elige mejores objetos (valor/peso)
            if objetos_candidatos:
                objetos_candidatos.sort(key=lambda x: x.valor / x.peso, reverse=True)
                mejor_objeto = objetos_candidatos[0]
                asignaciones[mejor_objeto.id] = robot.id
        
        # Fase 2: Ejecución
        for objeto_id, robot_id in asignaciones.items():
            objeto = ambiente.objetos[objeto_id]
            robot = ambiente.robots[robot_id]
            robot.cargar_objeto(objeto)
            objetos_disponibles.remove(objeto)
        
        # Fase 3: Descarga coordinada
        for robot in ambiente.robots.values():
            if robot.carga_actual >= robot.capacidad * 0.9:
                robot.descargar_todos()


class EstrategiaCompetencia:
    """
    COMPETENCIA: Objetivos contradictorios
    Robots compiten por objetos de alto valor
    Resultado: Ineficiencia pero mayor "motivación" individual
    """
    
    @staticmethod
    def ejecutar_ciclo(ambiente: Ambiente):
        """Un ciclo de competencia por objetos valiosos"""
        objetos_disponibles = ambiente.objetos_sin_recoger()
        
        if not objetos_disponibles:
            return
        
        # Todos quieren los objetos más valiosos
        objetos_disponibles.sort(key=lambda x: x.valor, reverse=True)
        
        for robot in ambiente.robots.values():
            if not robot.es_activo:
                continue
            
            # Cada robot intenta tomar el mejor objeto disponible
            for objeto in objetos_disponibles:
                if robot.puede_cargar(objeto):
                    robot.cargar_objeto(objeto)
                    objetos_disponibles.remove(objeto)
                    break  # Este robot consigue su presa
        
        # Robots llenos descargan, pero quedan con el valor
        for robot in ambiente.robots.values():
            if robot.carga_actual >= robot.capacidad * 0.7:
                robot.descargar_todos()


# ============================================================================
# SIMULACIÓN
# ============================================================================

class Simulador:
    """Ejecuta simulación de diferentes estrategias"""
    
    def __init__(self):
        self.resultados = {}
    
    def crear_ambiente(self, num_robots: int, num_objetos: int) -> Ambiente:
        """Crea un ambiente con robots y objetos"""
        ambiente = Ambiente()
        
        # Agregar robots
        for i in range(num_robots):
            robot = Robot(id=f"R{i+1}", capacidad=50)
            ambiente.agregar_robot(robot)
        
        # Agregar objetos
        for i in range(num_objetos):
            peso = randint(5, 15)
            valor = randint(10, 100)
            ambiente.agregar_objeto(peso, valor)
        
        return ambiente
    
    def simular(self, tipo_interaccion: TipoInteraccion, 
                ambiente: Ambiente, ciclos: int = 100) -> Dict:
        """Ejecuta simulación con una estrategia"""
        
        ambiente.modo_interaccion = tipo_interaccion
        
        # Seleccionar estrategia
        if tipo_interaccion == TipoInteraccion.COOPERACION:
            estrategia = EstrategiaCooperacion()
        elif tipo_interaccion == TipoInteraccion.COLABORACION:
            estrategia = EstrategiaColaboracion()
        else:  # COMPETENCIA
            estrategia = EstrategiaCompetencia()
        
        # Ejecutar ciclos
        for ciclo in range(ciclos):
            ambiente.ciclo = ciclo
            estrategia.ejecutar_ciclo(ambiente)
        
        # Calcular estadísticas
        total_objetos_recogidos = sum(len(r.objetos) for r in ambiente.robots.values())
        valor_total = sum(r.valor_total for r in ambiente.robots.values())
        valor_promedio_robot = valor_total / len(ambiente.robots) if ambiente.robots else 0
        varianza_valor = self._calcular_varianza(
            [r.valor_total for r in ambiente.robots.values()]
        )
        
        return {
            "tipo": tipo_interaccion.value,
            "ciclos": ciclos,
            "objetos_recogidos": total_objetos_recogidos,
            "valor_total": valor_total,
            "valor_promedio_robot": valor_promedio_robot,
            "varianza_valor": varianza_valor,
            "equidad": self._calcular_equidad(ambiente),
            "robots": {
                r.id: {
                    "valor": r.valor_total,
                    "objetos": len(r.objetos),
                    "carga": r.carga_actual
                }
                for r in ambiente.robots.values()
            }
        }
    
    @staticmethod
    def _calcular_varianza(valores: List[int]) -> float:
        """Calcula varianza de valores"""
        if not valores:
            return 0
        media = sum(valores) / len(valores)
        return sum((v - media) ** 2 for v in valores) / len(valores)
    
    @staticmethod
    def _calcular_equidad(ambiente: Ambiente) -> float:
        """Coeficiente de Gini simplificado (mide desigualdad)"""
        valores = sorted([r.valor_total for r in ambiente.robots.values()])
        if not valores or sum(valores) == 0:
            return 0
        n = len(valores)
        return (2 * sum(i * v for i, v in enumerate(valores, 1))) / (n * sum(valores)) - (n + 1) / n


def visualizar_resultados(resultados: Dict):
    """Visualiza resultados de la simulación"""
    print("\n" + "="*80)
    print(f"ESTRATEGIA: {resultados['tipo'].upper()}")
    print("="*80)
    print(f"Ciclos: {resultados['ciclos']}")
    print(f"Objetos recogidos: {resultados['objetos_recogidos']}")
    print(f"Valor total: {resultados['valor_total']}")
    print(f"Valor promedio por robot: {resultados['valor_promedio_robot']:.2f}")
    print(f"Varianza (dispersión): {resultados['varianza_valor']:.2f}")
    print(f"Índice de Equidad (Gini): {resultados['equidad']:.3f} (0=perfecta, 1=perfecta desigualdad)")
    
    print("\nDetalle por Robot:")
    for robot_id, datos in resultados['robots'].items():
        barra = "█" * (datos['valor'] // 10)
        print(f"  {robot_id}: {barra} Valor={datos['valor']:3d} Objetos={datos['objetos']:2d}")


def main():
    """Función principal"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║  EJEMPLO: Cooperación, Colaboración y Competencia en Agentes             ║
║                                                                           ║
║  Caso: 5 Robots recogiendo 30 objetos en una fábrica                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    simulador = Simulador()
    
    # Crear ambientes para cada estrategia (con mismos objetos)
    env_base = simulador.crear_ambiente(num_robots=5, num_objetos=30)
    
    # Copiar objetos para mantener consistencia
    objetos_originales = [
        (obj.peso, obj.valor) for obj in env_base.objetos
    ]
    
    resultados_todos = []
    
    for tipo in [TipoInteraccion.COOPERACION, 
                 TipoInteraccion.COLABORACION, 
                 TipoInteraccion.COMPETENCIA]:
        
        # Crear ambiente limpio con mismos objetos
        env = Ambiente()
        for i in range(5):
            robot = Robot(id=f"R{i+1}", capacidad=50)
            env.agregar_robot(robot)
        
        for peso, valor in objetos_originales:
            env.agregar_objeto(peso, valor)
        
        # Simular
        resultado = simulador.simular(tipo, env, ciclos=100)
        resultados_todos.append(resultado)
        visualizar_resultados(resultado)
    
    # Comparación final
    print("\n" + "="*80)
    print("COMPARACIÓN DE ESTRATEGIAS")
    print("="*80)
    
    print(f"\n{'Métrica':<25} {'Cooperación':<20} {'Colaboración':<20} {'Competencia':<20}")
    print("-"*85)
    
    for metrica in ['valor_total', 'valor_promedio_robot', 'varianza_valor', 'equidad']:
        print(f"{metrica:<25}", end="")
        for r in resultados_todos:
            valor = r[metrica]
            if isinstance(valor, float):
                print(f"{valor:<20.2f}", end="")
            else:
                print(f"{valor:<20}", end="")
        print()
    
    # Análisis
    print("\n" + "="*80)
    print("ANÁLISIS")
    print("="*80)
    
    val_coop = resultados_todos[0]['valor_total']
    val_colab = resultados_todos[1]['valor_total']
    val_comp = resultados_todos[2]['valor_total']
    
    print(f"""
EFICIENCIA GLOBAL:
  • Cooperación obtiene {val_coop} de valor
  • Colaboración obtiene {val_colab} de valor (mejora: {(val_colab-val_coop):+d})
  • Competencia obtiene {val_comp} de valor (cambio: {(val_comp-val_coop):+d})

EQUIDAD (Índice de Gini):
  • Cooperación: {resultados_todos[0]['equidad']:.3f} (más equitativo)
  • Colaboración: {resultados_todos[1]['equidad']:.3f}
  • Competencia: {resultados_todos[2]['equidad']:.3f} (más desigual)

CONCLUSIONES:
  ✓ COLABORACIÓN: Máxima eficiencia global (mejor coordinación)
  ✓ COOPERACIÓN: Equidad, escalabilidad, emergencia
  ✓ COMPETENCIA: Motivación individual pero ineficiencia global
    """)


if __name__ == "__main__":
    main()
