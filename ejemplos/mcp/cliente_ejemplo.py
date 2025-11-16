"""
Ejemplo 2: Cliente MCP Simple - Interactúa con un servidor

Este ejemplo muestra cómo crear un cliente MCP que:
1. Se conecta a un servidor MCP
2. Descubre recursos disponibles
3. Lee recursos
4. Ejecuta herramientas
5. Maneja errores
"""

import asyncio
import json
from typing import Any, Optional, List, Dict


class ClienteMCP:
    """Cliente para interactuar con servidores MCP"""
    
    def __init__(self, nombre: str = "cliente-mcp"):
        """
        Inicializa el cliente MCP
        
        Args:
            nombre: Nombre identificador del cliente
        """
        self.nombre = nombre
        self.id_contador = 0
        self.conectado = False
        print(f"📱 Cliente MCP '{nombre}' inicializado")
    
    def _generar_id(self) -> int:
        """Genera un ID único para cada solicitud"""
        self.id_contador += 1
        return self.id_contador
    
    def _crear_solicitud(
        self,
        metodo: str,
        parametros: Optional[Dict] = None
    ) -> Dict:
        """
        Crea una solicitud JSON-RPC 2.0
        
        Args:
            metodo: Método MCP a invocar
            parametros: Parámetros del método
        
        Returns:
            dict: Solicitud JSON-RPC 2.0
        """
        solicitud = {
            "jsonrpc": "2.0",
            "method": metodo,
            "id": self._generar_id()
        }
        
        if parametros:
            solicitud["params"] = parametros
        
        return solicitud
    
    async def conectar(self) -> bool:
        """
        Simula la conexión a un servidor MCP
        
        Returns:
            bool: True si se conectó exitosamente
        """
        try:
            print(f"\n🔌 Conectando al servidor MCP...")
            # Simulamos la conexión
            await asyncio.sleep(0.5)
            self.conectado = True
            print(f"✅ Conectado exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    async def desconectar(self) -> None:
        """Cierra la conexión con el servidor"""
        self.conectado = False
        print(f"🔌 Desconectado del servidor")
    
    async def listar_recursos(self) -> Optional[List[Dict]]:
        """
        Solicita al servidor la lista de recursos disponibles
        
        Returns:
            list: Lista de recursos o None si hay error
        """
        if not self.conectado:
            print("❌ No estás conectado. Usa conectar() primero.")
            return None
        
        try:
            solicitud = self._crear_solicitud("resources/list")
            print(f"\n📡 Enviando: {solicitud['method']}")
            
            # Simulamos el envío de la solicitud
            await asyncio.sleep(0.3)
            
            # Simulamos la respuesta del servidor
            respuesta = {
                "jsonrpc": "2.0",
                "result": {
                    "resources": [
                        {
                            "uri": "file:///datos/usuarios.json",
                            "name": "usuarios.json",
                            "description": "Base de datos de usuarios",
                            "mimeType": "application/json"
                        },
                        {
                            "uri": "file:///datos/configuracion.txt",
                            "name": "configuracion.txt",
                            "description": "Archivo de configuración",
                            "mimeType": "text/plain"
                        }
                    ]
                },
                "id": solicitud["id"]
            }
            
            print(f"📥 Respuesta recibida: {len(respuesta['result']['resources'])} recursos")
            return respuesta["result"]["resources"]
        
        except Exception as e:
            print(f"❌ Error listando recursos: {e}")
            return None
    
    async def leer_recurso(self, uri: str) -> Optional[str]:
        """
        Solicita al servidor que lea un recurso específico
        
        Args:
            uri: URI del recurso a leer
        
        Returns:
            str: Contenido del recurso o None si hay error
        """
        if not self.conectado:
            print("❌ No estás conectado. Usa conectar() primero.")
            return None
        
        try:
            solicitud = self._crear_solicitud(
                "resources/read",
                {"uri": uri}
            )
            print(f"\n📡 Enviando: {solicitud['method']} para {uri}")
            
            # Simulamos el envío de la solicitud
            await asyncio.sleep(0.3)
            
            # Simulamos la respuesta del servidor
            contenido_simulado = {
                "file:///datos/usuarios.json": '{\n  "usuarios": [\n    {"id": 1, "nombre": "Juan", "email": "juan@example.com"},\n    {"id": 2, "nombre": "María", "email": "maria@example.com"}\n  ]\n}',
                "file:///datos/configuracion.txt": "# Configuración del Sistema\nDEBUG=true\nPUERTO=8080\nHOST=localhost"
            }
            
            contenido = contenido_simulado.get(
                uri,
                "Contenido simulado del recurso"
            )
            
            print(f"📥 Contenido leído ({len(contenido)} caracteres)")
            return contenido
        
        except Exception as e:
            print(f"❌ Error leyendo recurso: {e}")
            return None
    
    async def listar_herramientas(self) -> Optional[List[Dict]]:
        """
        Solicita al servidor la lista de herramientas disponibles
        
        Returns:
            list: Lista de herramientas o None si hay error
        """
        if not self.conectado:
            print("❌ No estás conectado. Usa conectar() primero.")
            return None
        
        try:
            solicitud = self._crear_solicitud("tools/list")
            print(f"\n📡 Enviando: {solicitud['method']}")
            
            # Simulamos el envío de la solicitud
            await asyncio.sleep(0.3)
            
            # Simulamos la respuesta del servidor
            respuesta = {
                "jsonrpc": "2.0",
                "result": {
                    "tools": [
                        {
                            "name": "crear_usuario",
                            "description": "Crea un nuevo usuario en el sistema",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "nombre": {"type": "string"},
                                    "email": {"type": "string"}
                                },
                                "required": ["nombre", "email"]
                            }
                        },
                        {
                            "name": "eliminar_usuario",
                            "description": "Elimina un usuario del sistema",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"}
                                },
                                "required": ["id"]
                            }
                        },
                        {
                            "name": "enviar_email",
                            "description": "Envía un email a un usuario",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "destinatario": {"type": "string"},
                                    "asunto": {"type": "string"},
                                    "cuerpo": {"type": "string"}
                                },
                                "required": ["destinatario", "asunto", "cuerpo"]
                            }
                        }
                    ]
                },
                "id": solicitud["id"]
            }
            
            print(f"📥 Respuesta recibida: {len(respuesta['result']['tools'])} herramientas")
            return respuesta["result"]["tools"]
        
        except Exception as e:
            print(f"❌ Error listando herramientas: {e}")
            return None
    
    async def ejecutar_herramienta(
        self,
        nombre: str,
        argumentos: Dict
    ) -> Optional[Dict]:
        """
        Solicita al servidor que ejecute una herramienta
        
        Args:
            nombre: Nombre de la herramienta
            argumentos: Argumentos para la herramienta
        
        Returns:
            dict: Resultado de la ejecución o None si hay error
        """
        if not self.conectado:
            print("❌ No estás conectado. Usa conectar() primero.")
            return None
        
        try:
            solicitud = self._crear_solicitud(
                "tools/call",
                {
                    "name": nombre,
                    "arguments": argumentos
                }
            )
            print(f"\n📡 Ejecutando: {nombre}")
            print(f"   Argumentos: {json.dumps(argumentos, indent=2)}")
            
            # Simulamos el envío de la solicitud
            await asyncio.sleep(0.5)
            
            # Simulamos la respuesta del servidor
            respuestas_simuladas = {
                "crear_usuario": {
                    "success": True,
                    "message": f"✅ Usuario '{argumentos.get('nombre')}' creado exitosamente",
                    "id": 3
                },
                "eliminar_usuario": {
                    "success": True,
                    "message": f"✅ Usuario con ID {argumentos.get('id')} eliminado"
                },
                "enviar_email": {
                    "success": True,
                    "message": f"✅ Email enviado a {argumentos.get('destinatario')}",
                    "timestamp": "2024-01-15T10:30:00Z"
                }
            }
            
            resultado = respuestas_simuladas.get(
                nombre,
                {"success": True, "message": "Herramienta ejecutada"}
            )
            
            print(f"📥 Resultado: {resultado['message']}")
            return resultado
        
        except Exception as e:
            print(f"❌ Error ejecutando herramienta: {e}")
            return None
    
    async def mostrar_informacion(self) -> None:
        """Muestra información del cliente"""
        print(f"\n📊 Información del Cliente MCP:")
        print(f"   Nombre: {self.nombre}")
        print(f"   Conectado: {'✅ Sí' if self.conectado else '❌ No'}")
        print(f"   Solicitudes enviadas: {self.id_contador}")


# Ejemplo interactivo de uso
async def main():
    """Demuestra el funcionamiento del cliente MCP"""
    
    print("=" * 70)
    print("🌐 Cliente MCP - Ejemplo Interactivo")
    print("=" * 70)
    
    # Crear cliente
    cliente = ClienteMCP(nombre="mi-cliente")
    
    # 1. Conectar
    print("\n[PASO 1] Conectando al servidor...")
    if not await cliente.conectar():
        print("Abortando...")
        return
    
    # 2. Listar recursos
    print("\n[PASO 2] Descubriendo recursos disponibles...")
    recursos = await cliente.listar_recursos()
    
    if recursos:
        print("📚 Recursos disponibles:")
        for i, recurso in enumerate(recursos, 1):
            print(f"   {i}. {recurso['name']}")
            print(f"      └─ {recurso['description']}")
    
    # 3. Leer un recurso
    if recursos:
        print("\n[PASO 3] Leyendo el primer recurso...")
        contenido = await cliente.leer_recurso(recursos[0]["uri"])
        if contenido:
            print("📄 Contenido:")
            lineas = contenido.split('\n')[:5]  # Mostrar primeras 5 líneas
            for linea in lineas:
                print(f"   {linea}")
            if len(contenido.split('\n')) > 5:
                print(f"   ... ({len(contenido.split(chr(10)))} líneas en total)")
    
    # 4. Listar herramientas
    print("\n[PASO 4] Descubriendo herramientas disponibles...")
    herramientas = await cliente.listar_herramientas()
    
    if herramientas:
        print("🛠️ Herramientas disponibles:")
        for i, herramienta in enumerate(herramientas, 1):
            print(f"   {i}. {herramienta['name']}")
            print(f"      └─ {herramienta['description']}")
    
    # 5. Ejecutar herramientas
    print("\n[PASO 5] Ejecutando herramientas...")
    
    # Ejemplo 1: Crear usuario
    await cliente.ejecutar_herramienta(
        "crear_usuario",
        {
            "nombre": "Carlos García",
            "email": "carlos@example.com"
        }
    )
    
    # Ejemplo 2: Enviar email
    await cliente.ejecutar_herramienta(
        "enviar_email",
        {
            "destinatario": "carlos@example.com",
            "asunto": "Bienvenido",
            "cuerpo": "¡Hola Carlos! Bienvenido al sistema."
        }
    )
    
    # Ejemplo 3: Eliminar usuario
    await cliente.ejecutar_herramienta(
        "eliminar_usuario",
        {
            "id": 1
        }
    )
    
    # 6. Mostrar información
    await cliente.mostrar_informacion()
    
    # 7. Desconectar
    print("\n[PASO 6] Desconectando...")
    await cliente.desconectar()
    
    print("\n" + "=" * 70)
    print("✅ Ejemplo completado")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
