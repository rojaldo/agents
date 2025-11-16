#!/usr/bin/env python3
"""
Ejemplo 1: Agente Termostato Simple
Demuestra el ciclo percepto-acción básico

Concepto: Un agente que percibe temperatura y actúa controlando calefacción
"""

class Termostato:
    """Agente termostato simple que controla calefacción"""
    
    def __init__(self, temperatura_objetivo=20):
        self.temp_objetivo = temperatura_objetivo
        self.calefaccion_activa = False
        self.ciclos_ejecutados = 0
    
    def percibir(self, temperatura_actual):
        """
        FASE 1: PERCEPCIÓN
        Lee la temperatura del ambiente
        """
        return temperatura_actual
    
    def razonar(self, temperatura_sensada):
        """
        FASE 2: RAZONAMIENTO
        Decide si encender o apagar basado en temperatura objetivo
        
        Lógica racional:
        - Si temp < objetivo: necesito calor → ENCENDER
        - Si temp >= objetivo: tengo suficiente calor → APAGAR
        """
        if temperatura_sensada < self.temp_objetivo:
            return "ENCENDER"
        else:
            return "APAGAR"
    
    def actuar(self, accion):
        """
        FASE 3: ACCIÓN
        Ejecuta la decisión controlando la calefacción
        """
        if accion == "ENCENDER":
            self.calefaccion_activa = True
        else:
            self.calefaccion_activa = False
        
        return self.calefaccion_activa
    
    def ejecutar_ciclo(self, temperatura_ambiente):
        """Ejecuta un ciclo completo percepto-acción"""
        self.ciclos_ejecutados += 1
        
        print(f"\n{'='*50}")
        print(f"CICLO {self.ciclos_ejecutados}")
        print(f"{'='*50}")
        
        # 1. PERCIBIR
        print(f"[1] PERCEPCIÓN: Leyendo temperatura del ambiente...")
        temp = self.percibir(temperatura_ambiente)
        print(f"    Temperatura sensada: {temp}°C")
        
        # 2. RAZONAR
        print(f"[2] RAZONAMIENTO: Analizando temperatura...")
        print(f"    Objetivo: {self.temp_objetivo}°C")
        accion = self.razonar(temp)
        print(f"    Decisión: {accion}")
        
        # 3. ACTUAR
        print(f"[3] ACCIÓN: Ejecutando decisión...")
        estado = self.actuar(accion)
        print(f"    Calefacción: {'ENCENDIDA ✓' if estado else 'APAGADA ✗'}")
        
        return estado


# ============================================================================
# SIMULACIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*50)
    print("SIMULACIÓN: AGENTE TERMOSTATO SIMPLE")
    print("="*50)
    print("\nEste ejemplo muestra el ciclo percepto-acción básico.")
    print("El agente:\n"
          "  1. PERCIBE: Lee temperatura del ambiente\n"
          "  2. RAZONA: Compara con objetivo\n"
          "  3. ACTÚA: Enciende/apaga calefacción\n")
    
    # Crear agente con objetivo de 20°C
    termostato = Termostato(temperatura_objetivo=20)
    
    # Simular secuencia de temperaturas (simulando enfriamiento y calentamiento)
    print("\nSimulando variaciones de temperatura:\n")
    
    temperaturas = [
        15,  # Muy frío → ENCENDER
        16,  # Frío → ENCENDER
        17,  # Frío → ENCENDER
        18,  # Más caliente → ENCENDER
        19,  # Casi → ENCENDER
        20,  # Exacto → APAGAR
        21,  # Pasado → APAGAR
        22,  # Caliente → APAGAR
        21,  # Baja → APAGAR (sigue objetivo)
        19,  # Baja más → ENCENDER
        18,  # Más baja → ENCENDER
    ]
    
    for temp_ambiente in temperaturas:
        termostato.ejecutar_ciclo(temp_ambiente)
    
    print("\n" + "="*50)
    print("RESUMEN DE SIMULACIÓN")
    print("="*50)
    print(f"Total de ciclos ejecutados: {termostato.ciclos_ejecutados}")
    print(f"Objetivo de temperatura: {termostato.temp_objetivo}°C")
    print(f"\nEl agente ejecutó el ciclo percepto-acción {termostato.ciclos_ejecutados} veces")
    print("demostrando autonomía: tomó decisiones basadas en su razonamiento")
    print("y el estado del ambiente.\n")
