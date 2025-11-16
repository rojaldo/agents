"""
Ejemplo 1: Servidor MCP Simple - Gestor de Archivos

Este es el ejemplo más básico de un servidor MCP que:
1. Expone archivos locales como recursos
2. Permite leer archivos
3. Ofrece herramientas para crear y eliminar archivos
"""

import json
import os
import asyncio
from typing import Any
from dataclasses import dataclass
from enum import Enum


# Simulación básica del servidor MCP
class TipoMensaje(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"


@dataclass
class RecursoMCP:
    """Representa un recurso en MCP"""
    uri: str
    nombre: str
    descripcion: str
    tipo_mime: str = "text/plain"


@dataclass
class HerramientaMCP:
    """Representa una herramienta en MCP"""
    nombre: str
    descripcion: str
    esquema_entrada: dict


class ServidorGestorArchivos:
    """Servidor MCP para gestionar archivos"""
    
    def __init__(self, carpeta_base: str = "."):
        """
        Inicializa el servidor
        
        Args:
            carpeta_base: Carpeta donde se almacenarán los archivos
        """
        self.carpeta_base = carpeta_base
        self.id_contador = 0
        self.herramientas = self._definir_herramientas()
        
        # Crear carpeta si no existe
        os.makedirs(carpeta_base, exist_ok=True)
    
    def _definir_herramientas(self) -> list:
        """Define las herramientas disponibles"""
        return [
            HerramientaMCP(
                nombre="crear_archivo",
                descripcion="Crea un nuevo archivo con contenido",
                esquema_entrada={
                    "type": "object",
                    "properties": {
                        "nombre": {
                            "type": "string",
                            "description": "Nombre del archivo (ej: documento.txt)"
                        },
                        "contenido": {
                            "type": "string",
                            "description": "Contenido del archivo"
                        }
                    },
                    "required": ["nombre", "contenido"]
                }
            ),
            HerramientaMCP(
                nombre="eliminar_archivo",
                descripcion="Elimina un archivo existente",
                esquema_entrada={
                    "type": "object",
                    "properties": {
                        "nombre": {
                            "type": "string",
                            "description": "Nombre del archivo a eliminar"
                        }
                    },
                    "required": ["nombre"]
                }
            ),
            HerramientaMCP(
                nombre="renombrar_archivo",
                descripcion="Renombra un archivo existente",
                esquema_entrada={
                    "type": "object",
                    "properties": {
                        "nombre_actual": {
                            "type": "string",
                            "description": "Nombre actual del archivo"
                        },
                        "nombre_nuevo": {
                            "type": "string",
                            "description": "Nuevo nombre del archivo"
                        }
                    },
                    "required": ["nombre_actual", "nombre_nuevo"]
                }
            )
        ]
    
    async def listar_recursos(self) -> list:
        """
        Método MCP: Retorna lista de recursos disponibles
        
        Returns:
            list: Lista de recursos (archivos en la carpeta)
        """
        print("📂 Listando recursos...")
        recursos = []
        
        try:
            for archivo in os.listdir(self.carpeta_base):
                ruta_completa = os.path.join(self.carpeta_base, archivo)
                if os.path.isfile(ruta_completa):
                    tamano = os.path.getsize(ruta_completa)
                    recurso = RecursoMCP(
                        uri=f"file://{ruta_completa}",
                        nombre=archivo,
                        descripcion=f"Archivo: {archivo} ({tamano} bytes)",
                        tipo_mime="text/plain"
                    )
                    recursos.append(recurso)
        except Exception as e:
            print(f"❌ Error listando recursos: {e}")
        
        return recursos
    
    async def leer_recurso(self, uri: str) -> str:
        """
        Método MCP: Lee un recurso específico
        
        Args:
            uri: URI del recurso (ej: file:///ruta/al/archivo)
        
        Returns:
            str: Contenido del archivo
        """
        print(f"📖 Leyendo recurso: {uri}")
        
        try:
            # Extraer ruta del URI
            ruta = uri.replace("file://", "")
            
            # Validar que el archivo está dentro de carpeta_base
            ruta_abs = os.path.abspath(ruta)
            base_abs = os.path.abspath(self.carpeta_base)
            
            if not ruta_abs.startswith(base_abs):
                return "❌ Error: Acceso denegado (archivo fuera de carpeta permitida)"
            
            if not os.path.exists(ruta_abs):
                return f"❌ Error: Archivo no encontrado: {ruta_abs}"
            
            with open(ruta_abs, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            return contenido
        
        except Exception as e:
            return f"❌ Error leyendo archivo: {e}"
    
    async def listar_herramientas(self) -> list:
        """
        Método MCP: Retorna lista de herramientas disponibles
        
        Returns:
            list: Lista de herramientas
        """
        print("🛠️ Listando herramientas...")
        return self.herramientas
    
    async def ejecutar_herramienta(
        self,
        nombre: str,
        argumentos: dict
    ) -> dict:
        """
        Método MCP: Ejecuta una herramienta
        
        Args:
            nombre: Nombre de la herramienta
            argumentos: Argumentos para la herramienta
        
        Returns:
            dict: Resultado de la ejecución
        """
        print(f"🚀 Ejecutando herramienta: {nombre}")
        
        try:
            if nombre == "crear_archivo":
                return await self._crear_archivo(argumentos)
            
            elif nombre == "eliminar_archivo":
                return await self._eliminar_archivo(argumentos)
            
            elif nombre == "renombrar_archivo":
                return await self._renombrar_archivo(argumentos)
            
            else:
                return {
                    "success": False,
                    "error": f"Herramienta desconocida: {nombre}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error inesperado: {str(e)}"
            }
    
    async def _crear_archivo(self, argumentos: dict) -> dict:
        """Implementación: Crear archivo"""
        try:
            # Validar argumentos
            if "nombre" not in argumentos or "contenido" not in argumentos:
                return {
                    "success": False,
                    "error": "Faltan argumentos: nombre y contenido"
                }
            
            nombre = argumentos["nombre"]
            contenido = argumentos["contenido"]
            
            # Validar nombre (prevenir path traversal)
            if ".." in nombre or "/" in nombre or "\\" in nombre:
                return {
                    "success": False,
                    "error": "Nombre de archivo no válido"
                }
            
            ruta = os.path.join(self.carpeta_base, nombre)
            
            # Crear archivo
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            return {
                "success": True,
                "message": f"✅ Archivo '{nombre}' creado exitosamente",
                "ruta": ruta,
                "tamano": len(contenido)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error creando archivo: {str(e)}"
            }
    
    async def _eliminar_archivo(self, argumentos: dict) -> dict:
        """Implementación: Eliminar archivo"""
        try:
            if "nombre" not in argumentos:
                return {
                    "success": False,
                    "error": "Falta argumento: nombre"
                }
            
            nombre = argumentos["nombre"]
            
            # Validar nombre
            if ".." in nombre or "/" in nombre or "\\" in nombre:
                return {
                    "success": False,
                    "error": "Nombre de archivo no válido"
                }
            
            ruta = os.path.join(self.carpeta_base, nombre)
            
            if not os.path.exists(ruta):
                return {
                    "success": False,
                    "error": f"Archivo no encontrado: {nombre}"
                }
            
            os.remove(ruta)
            
            return {
                "success": True,
                "message": f"✅ Archivo '{nombre}' eliminado exitosamente"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error eliminando archivo: {str(e)}"
            }
    
    async def _renombrar_archivo(self, argumentos: dict) -> dict:
        """Implementación: Renombrar archivo"""
        try:
            if "nombre_actual" not in argumentos or "nombre_nuevo" not in argumentos:
                return {
                    "success": False,
                    "error": "Faltan argumentos: nombre_actual y nombre_nuevo"
                }
            
            nombre_actual = argumentos["nombre_actual"]
            nombre_nuevo = argumentos["nombre_nuevo"]
            
            # Validar nombres
            for nombre in [nombre_actual, nombre_nuevo]:
                if ".." in nombre or "/" in nombre or "\\" in nombre:
                    return {
                        "success": False,
                        "error": "Nombre de archivo no válido"
                    }
            
            ruta_actual = os.path.join(self.carpeta_base, nombre_actual)
            ruta_nueva = os.path.join(self.carpeta_base, nombre_nuevo)
            
            if not os.path.exists(ruta_actual):
                return {
                    "success": False,
                    "error": f"Archivo no encontrado: {nombre_actual}"
                }
            
            if os.path.exists(ruta_nueva):
                return {
                    "success": False,
                    "error": f"Ya existe un archivo con ese nombre: {nombre_nuevo}"
                }
            
            os.rename(ruta_actual, ruta_nueva)
            
            return {
                "success": True,
                "message": f"✅ Archivo renombrado: {nombre_actual} → {nombre_nuevo}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Error renombrando archivo: {str(e)}"
            }
    
    async def procesar_solicitud(
        self,
        metodo: str,
        parametros: dict = None
    ) -> dict:
        """
        Procesa una solicitud MCP
        
        Args:
            metodo: Método MCP a ejecutar
            parametros: Parámetros del método
        
        Returns:
            dict: Respuesta MCP
        """
        parametros = parametros or {}
        
        try:
            if metodo == "resources/list":
                recursos = await self.listar_recursos()
                return {
                    "result": {
                        "resources": [
                            {
                                "uri": r.uri,
                                "name": r.nombre,
                                "description": r.descripcion,
                                "mimeType": r.tipo_mime
                            }
                            for r in recursos
                        ]
                    }
                }
            
            elif metodo == "resources/read":
                uri = parametros.get("uri", "")
                contenido = await self.leer_recurso(uri)
                return {
                    "result": {
                        "contents": contenido
                    }
                }
            
            elif metodo == "tools/list":
                herramientas = await self.listar_herramientas()
                return {
                    "result": {
                        "tools": [
                            {
                                "name": h.nombre,
                                "description": h.descripcion,
                                "inputSchema": h.esquema_entrada
                            }
                            for h in herramientas
                        ]
                    }
                }
            
            elif metodo == "tools/call":
                nombre = parametros.get("name", "")
                argumentos = parametros.get("arguments", {})
                resultado = await self.ejecutar_herramienta(nombre, argumentos)
                return {
                    "result": resultado
                }
            
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Método no encontrado: {metodo}"
                    }
                }
        
        except Exception as e:
            return {
                "error": {
                    "code": -32603,
                    "message": f"Error interno: {str(e)}"
                }
            }


# Ejemplo de uso
async def main():
    """Demuestra el funcionamiento del servidor"""
    
    # Crear servidor
    servidor = ServidorGestorArchivos(carpeta_base="./mcp_data")
    
    print("=" * 60)
    print("🚀 Servidor MCP - Gestor de Archivos")
    print("=" * 60)
    
    # 1. Crear archivos de prueba
    print("\n1️⃣ CREANDO ARCHIVOS...")
    print("-" * 60)
    
    respuesta = await servidor.procesar_solicitud(
        "tools/call",
        {
            "name": "crear_archivo",
            "arguments": {
                "nombre": "introduccion.txt",
                "contenido": "Bienvenido a MCP\n\nEste es un ejemplo simple de servidor MCP"
            }
        }
    )
    print(f"Resultado: {respuesta['result']['message']}")
    
    respuesta = await servidor.procesar_solicitud(
        "tools/call",
        {
            "name": "crear_archivo",
            "arguments": {
                "nombre": "datos.json",
                "contenido": '{"usuarios": [{"id": 1, "nombre": "Juan"}]}'
            }
        }
    )
    print(f"Resultado: {respuesta['result']['message']}")
    
    # 2. Listar recursos
    print("\n2️⃣ LISTANDO RECURSOS...")
    print("-" * 60)
    
    respuesta = await servidor.procesar_solicitud("resources/list")
    for recurso in respuesta["result"]["resources"]:
        print(f"📄 {recurso['name']}: {recurso['description']}")
    
    # 3. Leer un recurso
    print("\n3️⃣ LEYENDO UN RECURSO...")
    print("-" * 60)
    
    if respuesta["result"]["resources"]:
        uri = respuesta["result"]["resources"][0]["uri"]
        respuesta = await servidor.procesar_solicitud(
            "resources/read",
            {"uri": uri}
        )
        print(f"Contenido de {uri}:")
        print(respuesta["result"]["contents"][:100] + "...")
    
    # 4. Listar herramientas
    print("\n4️⃣ HERRAMIENTAS DISPONIBLES...")
    print("-" * 60)
    
    respuesta = await servidor.procesar_solicitud("tools/list")
    for herramienta in respuesta["result"]["tools"]:
        print(f"🛠️ {herramienta['name']}: {herramienta['description']}")
    
    # 5. Renombrar archivo
    print("\n5️⃣ RENOMBRANDO ARCHIVO...")
    print("-" * 60)
    
    respuesta = await servidor.procesar_solicitud(
        "tools/call",
        {
            "name": "renombrar_archivo",
            "arguments": {
                "nombre_actual": "introduccion.txt",
                "nombre_nuevo": "bienvenida.txt"
            }
        }
    )
    print(f"Resultado: {respuesta['result']['message']}")
    
    # 6. Verificar cambios
    print("\n6️⃣ VERIFICANDO CAMBIOS...")
    print("-" * 60)
    
    respuesta = await servidor.procesar_solicitud("resources/list")
    print("Archivos finales:")
    for recurso in respuesta["result"]["resources"]:
        print(f"  • {recurso['name']}")
    
    print("\n" + "=" * 60)
    print("✅ Demostración completada")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
