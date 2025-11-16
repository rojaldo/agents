# Curso Completo de MCP (Model Context Protocol)

## 📚 Temario General

1. **Introducción a MCP**
2. **Conceptos Fundamentales**
3. **Arquitectura: Cliente y Servidor MCP**
4. **Instalación y Configuración**
5. **Ejemplos Prácticos Básicos**
6. **Recursos y Herramientas**
7. **Casos de Uso Avanzados**
8. **Mejores Prácticas**

---

## 1️⃣ Introducción a MCP

### ¿Qué es MCP?

El **Model Context Protocol (MCP)** es un protocolo abierto que permite a los modelos de IA (como Claude) acceder a recursos externos de forma estandarizada y segura.

### Analogía para entender MCP

Imagina que tienes un **asistente inteligente (el modelo de IA)** que sabe mucho, pero necesita acceso a recursos específicos:

- 📁 **Archivos en tu computadora**
- 🗄️ **Bases de datos**
- 🌐 **APIs externas**
- 📊 **Datos en tiempo real**

MCP es como proporcionar al asistente un **uniforme especial** que le permite:
1. **Conectarse** a estos recursos
2. **Solicitar información** de forma segura
3. **Ejecutar acciones** limitadas
4. **Recibir respuestas** estructuradas

### Objetivos principales de MCP

```
┌─────────────────────────────────────────┐
│      Model Context Protocol (MCP)       │
├─────────────────────────────────────────┤
│  ✅ Estandarización                     │
│  ✅ Seguridad                           │
│  ✅ Facilidad de integración            │
│  ✅ Interoperabilidad                   │
└─────────────────────────────────────────┘
```

---

## 2️⃣ Conceptos Fundamentales

### 2.1 ¿Por qué necesitamos MCP?

**Antes de MCP:**
```
┌──────────┐
│   IA     │  ❌ No tiene acceso a datos externos
│ (Claude) │  ❌ No puede ejecutar acciones
│          │  ❌ Cada integración es diferente
└──────────┘
```

**Con MCP:**
```
┌──────────┐
│   IA     │  ✅ Acceso estandarizado a recursos
│ (Claude) │  ✅ Ejecuta acciones de forma segura
│          │  ✅ Mismo protocolo para todo
└──────────┘
     ↓
  (MCP Protocol)
     ↓
┌──────────┬──────────┬──────────┐
│ Archivos │ BD       │ APIs     │
└──────────┴──────────┴──────────┘
```

### 2.2 Conceptos clave

#### **Recursos (Resources)**
Son los datos que el servidor MCP pone a disposición del cliente.

**Ejemplo:**
```json
{
  "type": "resource",
  "uri": "file:///documents/proyectos.txt",
  "name": "Lista de Proyectos",
  "description": "Proyectos activos de la empresa"
}
```

#### **Herramientas (Tools)**
Son funciones que el servidor MCP ofrece para que el cliente las ejecute.

**Ejemplo:**
```json
{
  "type": "tool",
  "name": "crear_archivo",
  "description": "Crea un nuevo archivo",
  "inputSchema": {
    "nombre": "string",
    "contenido": "string"
  }
}
```

#### **Indicadores (Prompts)**
Son plantillas predefinidas que el servidor proporciona para casos de uso específicos.

**Ejemplo:**
```json
{
  "name": "analizar_documento",
  "description": "Plantilla para analizar documentos",
  "arguments": [
    {
      "name": "tipo_analisis",
      "description": "Tipo de análisis a realizar"
    }
  ]
}
```

---

## 3️⃣ Arquitectura: Cliente y Servidor MCP

### 3.1 Modelo Cliente-Servidor

```
┌────────────────────────────────────────────────────────────┐
│                    CLIENTE MCP                             │
│                  (Ej: Claude)                              │
│                                                            │
│  - Solicita recursos                                      │
│  - Ejecuta herramientas                                   │
│  - Recibe respuestas                                      │
└─────────────────────┬──────────────────────────────────────┘
                      │
                      │ (JSON-RPC 2.0)
                      │ (Estándar HTTP o stdio)
                      │
┌─────────────────────▼──────────────────────────────────────┐
│                   SERVIDOR MCP                             │
│              (Tu aplicación)                               │
│                                                            │
│  - Publica recursos                                       │
│  - Implementa herramientas                                │
│  - Maneja solicitudes                                     │
└────────────────────────────────────────────────────────────┘
```

### 3.2 Flujo de comunicación

```
1. INICIALIZACIÓN
   Cliente ──➜ "Hola, quiero conectarme"
   Servidor ◀─ "Listo, así es lo que ofrezco"

2. DESCUBRIMIENTO
   Cliente ──➜ "¿Qué recursos tienes?"
   Servidor ◀─ "Tengo archivos, BD, APIs..."

3. EJECUCIÓN
   Cliente ──➜ "Quiero usar esta herramienta"
   Servidor ◀─ "Hecho, aquí está el resultado"

4. CIERRE
   Cliente ──➜ "Adiós"
   Servidor ◀─ "Hasta luego"
```

### 3.3 Componentes principales

#### **Cliente MCP**
- **¿Quién?** Claude (o cualquier LLM)
- **¿Qué hace?**
  - Descubre qué ofrece el servidor
  - Solicita recursos
  - Ejecuta herramientas
  - Interpreta resultados
- **¿Cuándo?** Cuando necesita datos o ejecutar acciones

#### **Servidor MCP**
- **¿Quién?** Tu aplicación/servicio
- **¿Qué hace?**
  - Expone recursos disponibles
  - Implementa herramientas
  - Procesa solicitudes del cliente
  - Devuelve resultados
- **¿Cuándo?** Siempre disponible para servir

### 3.4 Ejemplo visual de una interacción

```
┌─────────────────┐                    ┌──────────────────┐
│  CLIENTE (IA)   │                    │ SERVIDOR (Tu App)│
│                 │                    │                  │
│ "Dame archivos" │───────Request────➜│                  │
│                 │                    │ 📂 Busca archivos│
│                 │                    │                  │
│                 │◀───Response────────│ [archivo1, ...]  │
│ Recibe lista    │                    │                  │
│                 │                    │                  │
│"Ejecuta crear"  │───────Request────➜│                  │
│                 │                    │ ✅ Crea archivo │
│                 │                    │                  │
│                 │◀───Response────────│ {exitoso: true}  │
│ Procesa         │                    │                  │
└─────────────────┘                    └──────────────────┘
```

---

## 4️⃣ Instalación y Configuración

### 4.1 Requisitos previos

```bash
# Python 3.9+
python --version

# pip actualizado
pip install --upgrade pip

# Git (para clonar repositorios)
git --version
```

### 4.2 Instalación de MCP

#### **Opción 1: Desde PyPI (Recomendado)**

```bash
# Instalar la librería MCP
pip install mcp

# Verificar instalación
python -c "import mcp; print(mcp.__version__)"
```

#### **Opción 2: Desde el repositorio**

```bash
# Clonar el repositorio
git clone https://github.com/anthropics/python-sdk.git

# Instalar en modo desarrollo
cd python-sdk
pip install -e ".[mcp]"
```

### 4.3 Configuración básica

**Crear archivo `mcp_config.json`:**

```json
{
  "mcpServers": {
    "mi_servidor": {
      "command": "python",
      "args": ["servidor_mcp.py"],
      "env": {
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

---

## 5️⃣ Ejemplos Prácticos Básicos

### 5.1 Servidor MCP Simple (Gestor de Archivos)

**Archivo: `servidor_simple.py`**

```python
import json
import os
from mcp.server import Server
from mcp.types import Resource, Tool

# Crear servidor
app = Server("gestor-archivos")

# 1. EXPONER UN RECURSO
@app.list_resources()
async def list_resources():
    """Lista todos los archivos en la carpeta actual"""
    recursos = []
    for archivo in os.listdir("."):
        if os.path.isfile(archivo):
            recursos.append(
                Resource(
                    uri=f"file://{os.path.abspath(archivo)}",
                    name=archivo,
                    description=f"Archivo: {archivo}",
                    mimeType="text/plain"
                )
            )
    return recursos

# 2. LEER UN RECURSO
@app.read_resource()
async def read_resource(uri: str):
    """Lee el contenido de un archivo"""
    ruta = uri.replace("file://", "")
    with open(ruta, 'r', encoding='utf-8') as f:
        contenido = f.read()
    return contenido

# 3. EXPONER UNA HERRAMIENTA
@app.list_tools()
async def list_tools():
    """Lista las herramientas disponibles"""
    return [
        Tool(
            name="crear_archivo",
            description="Crea un nuevo archivo",
            inputSchema={
                "type": "object",
                "properties": {
                    "nombre": {
                        "type": "string",
                        "description": "Nombre del archivo"
                    },
                    "contenido": {
                        "type": "string",
                        "description": "Contenido del archivo"
                    }
                },
                "required": ["nombre", "contenido"]
            }
        ),
        Tool(
            name="eliminar_archivo",
            description="Elimina un archivo",
            inputSchema={
                "type": "object",
                "properties": {
                    "nombre": {
                        "type": "string",
                        "description": "Nombre del archivo a eliminar"
                    }
                },
                "required": ["nombre"]
            }
        )
    ]

# 4. IMPLEMENTAR UNA HERRAMIENTA
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Ejecuta una herramienta"""
    if name == "crear_archivo":
        with open(arguments["nombre"], "w", encoding='utf-8') as f:
            f.write(arguments["contenido"])
        return f"✅ Archivo '{arguments['nombre']}' creado"
    
    elif name == "eliminar_archivo":
        os.remove(arguments["nombre"])
        return f"✅ Archivo '{arguments['nombre']}' eliminado"
    
    return "❌ Herramienta no reconocida"

# Ejecutar servidor
if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run())
```

### 5.2 Cliente MCP Simple

**Archivo: `cliente_simple.py`**

```python
import json
import httpx
import asyncio
from typing import Any

class ClienteMCP:
    def __init__(self, url: str = "http://localhost:8000"):
        self.url = url
        self.client = httpx.AsyncClient()
        self.id_contador = 0
    
    def _generar_id(self) -> int:
        """Genera un ID único para cada request"""
        self.id_contador += 1
        return self.id_contador
    
    async def descubrir_recursos(self) -> list:
        """Descubre los recursos disponibles en el servidor"""
        request = {
            "jsonrpc": "2.0",
            "method": "resources/list",
            "id": self._generar_id()
        }
        
        response = await self.client.post(
            f"{self.url}/rpc",
            json=request
        )
        
        resultado = response.json()
        return resultado.get("result", {}).get("resources", [])
    
    async def leer_recurso(self, uri: str) -> str:
        """Lee un recurso específico"""
        request = {
            "jsonrpc": "2.0",
            "method": "resources/read",
            "params": {"uri": uri},
            "id": self._generar_id()
        }
        
        response = await self.client.post(
            f"{self.url}/rpc",
            json=request
        )
        
        resultado = response.json()
        return resultado.get("result", {}).get("contents", "")
    
    async def listar_herramientas(self) -> list:
        """Lista las herramientas disponibles"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": self._generar_id()
        }
        
        response = await self.client.post(
            f"{self.url}/rpc",
            json=request
        )
        
        resultado = response.json()
        return resultado.get("result", {}).get("tools", [])
    
    async def ejecutar_herramienta(
        self,
        nombre: str,
        argumentos: dict
    ) -> Any:
        """Ejecuta una herramienta"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": nombre,
                "arguments": argumentos
            },
            "id": self._generar_id()
        }
        
        response = await self.client.post(
            f"{self.url}/rpc",
            json=request
        )
        
        resultado = response.json()
        return resultado.get("result", {})

# Ejemplo de uso
async def main():
    cliente = ClienteMCP()
    
    # 1. Descubrir recursos
    print("📂 Descubriendo recursos...")
    recursos = await cliente.descubrir_recursos()
    for recurso in recursos:
        print(f"  - {recurso['name']}")
    
    # 2. Listar herramientas
    print("\n🛠️ Herramientas disponibles:")
    herramientas = await cliente.listar_herramientas()
    for herramienta in herramientas:
        print(f"  - {herramienta['name']}: {herramienta['description']}")
    
    # 3. Ejecutar una herramienta
    print("\n✏️ Creando un archivo...")
    resultado = await cliente.ejecutar_herramienta(
        "crear_archivo",
        {
            "nombre": "ejemplo.txt",
            "contenido": "Hola MCP"
        }
    )
    print(f"  {resultado}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 5.3 Ejecutar servidor y cliente

```bash
# Terminal 1: Iniciar servidor
python servidor_simple.py

# Terminal 2: Ejecutar cliente
python cliente_simple.py
```

---

## 6️⃣ Recursos y Herramientas

### 6.1 Esquema JSON-RPC 2.0

MCP usa JSON-RPC 2.0 como protocolo de comunicación.

#### **Estructura de una solicitud**

```json
{
  "jsonrpc": "2.0",
  "method": "nombre_del_metodo",
  "params": {
    "param1": "valor1",
    "param2": "valor2"
  },
  "id": 1
}
```

#### **Estructura de una respuesta**

```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": "resultado"
  },
  "id": 1
}
```

#### **En caso de error**

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32600,
    "message": "Solicitud inválida"
  },
  "id": 1
}
```

### 6.2 Métodos principales

| Método | Descripción | Cliente/Servidor |
|--------|-------------|-----------------|
| `initialize` | Establece la conexión | Cliente → Servidor |
| `resources/list` | Lista recursos disponibles | Cliente → Servidor |
| `resources/read` | Lee un recurso | Cliente → Servidor |
| `tools/list` | Lista herramientas | Cliente → Servidor |
| `tools/call` | Ejecuta una herramienta | Cliente → Servidor |
| `prompts/list` | Lista indicadores | Cliente → Servidor |
| `prompts/get` | Obtiene un indicador | Cliente → Servidor |

---

## 7️⃣ Casos de Uso Avanzados

### 7.1 Servidor con acceso a Base de Datos

```python
import sqlite3
from mcp.server import Server
from mcp.types import Resource, Tool

app = Server("gestor-bd")

# Conexión a BD
conexion = sqlite3.connect("datos.db")

@app.list_resources()
async def list_resources():
    """Expone tablas como recursos"""
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    tablas = cursor.fetchall()
    
    recursos = [
        Resource(
            uri=f"db://tabla/{tabla[0]}",
            name=f"Tabla: {tabla[0]}",
            description=f"Datos de {tabla[0]}"
        )
        for tabla in tablas
    ]
    return recursos

@app.read_resource()
async def read_resource(uri: str):
    """Lee datos de una tabla"""
    tabla = uri.split("/")[-1]
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM {tabla}")
    datos = cursor.fetchall()
    return json.dumps(datos, default=str)

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="ejecutar_query",
            description="Ejecuta una consulta SQL",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Consulta SQL a ejecutar"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "ejecutar_query":
        cursor = conexion.cursor()
        try:
            cursor.execute(arguments["query"])
            conexion.commit()
            return "✅ Query ejecutado"
        except Exception as e:
            return f"❌ Error: {str(e)}"
```

### 7.2 Servidor con integración a API externa

```python
import httpx
from mcp.server import Server
from mcp.types import Tool

app = Server("integrador-api")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="obtener_clima",
            description="Obtiene el clima de una ciudad",
            inputSchema={
                "type": "object",
                "properties": {
                    "ciudad": {
                        "type": "string",
                        "description": "Ciudad"
                    }
                },
                "required": ["ciudad"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "obtener_clima":
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": arguments["ciudad"],
                    "appid": "TU_API_KEY"
                }
            )
            datos = response.json()
            return json.dumps(datos)
```

### 7.3 Servidor con múltiples recursos

```python
from mcp.server import Server
from mcp.types import Resource

app = Server("gestor-multiples")

# Simulamos diferentes fuentes de datos
datos = {
    "usuarios": [
        {"id": 1, "nombre": "Juan"},
        {"id": 2, "nombre": "María"}
    ],
    "productos": [
        {"id": 1, "nombre": "Laptop"},
        {"id": 2, "nombre": "Mouse"}
    ],
    "ordenes": [
        {"id": 1, "usuario_id": 1, "producto_id": 1}
    ]
}

@app.list_resources()
async def list_resources():
    recursos = [
        Resource(
            uri=f"data://usuarios",
            name="Usuarios",
            description="Lista de usuarios"
        ),
        Resource(
            uri=f"data://productos",
            name="Productos",
            description="Catálogo de productos"
        ),
        Resource(
            uri=f"data://ordenes",
            name="Órdenes",
            description="Órdenes de compra"
        )
    ]
    return recursos

@app.read_resource()
async def read_resource(uri: str):
    tipo = uri.split("://")[-1]
    if tipo in datos:
        return json.dumps(datos[tipo], indent=2)
    return "❌ Recurso no encontrado"
```

---

## 8️⃣ Mejores Prácticas

### 8.1 Seguridad

```python
# ❌ MAL: Sin validación
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    os.system(arguments["comando"])  # ¡Peligroso!

# ✅ BIEN: Con validación
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    comandos_permitidos = ["ls", "pwd", "echo"]
    if name in comandos_permitidos:
        # Usar subprocess en lugar de os.system
        resultado = subprocess.run(
            [name, arguments["param"]],
            capture_output=True,
            text=True
        )
        return resultado.stdout
```

### 8.2 Manejo de errores

```python
# ✅ BIEN: Manejo robusto de errores
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "crear_archivo":
            ruta = arguments.get("ruta")
            if not ruta:
                raise ValueError("Ruta requerida")
            
            # Validar ruta
            if ".." in ruta:  # Prevenir path traversal
                raise ValueError("Ruta no permitida")
            
            with open(ruta, "w") as f:
                f.write(arguments["contenido"])
            
            return {"success": True, "message": "Archivo creado"}
    
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {str(e)}"}
```

### 8.3 Logging y debugging

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    logger.debug(f"Herramienta solicitada: {name}")
    logger.debug(f"Argumentos: {arguments}")
    
    try:
        resultado = ejecutar_herramienta(name, arguments)
        logger.info(f"Herramienta {name} ejecutada exitosamente")
        return resultado
    except Exception as e:
        logger.error(f"Error ejecutando {name}: {str(e)}")
        raise
```

### 8.4 Documentación clara

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """
    Ejecuta herramientas disponibles en el servidor.
    
    Args:
        name (str): Nombre de la herramienta.
                   Opciones: crear_archivo, eliminar_archivo
        
        arguments (dict): Argumentos específicos de la herramienta.
                         Ejemplo:
                         {
                            "nombre": "archivo.txt",
                            "contenido": "Contenido del archivo"
                         }
    
    Returns:
        dict: Resultado de la ejecución con keys:
              - success (bool): Indicador de éxito
              - message (str): Descripción del resultado
              - data (any): Datos adicionales
    
    Raises:
        ValueError: Si los argumentos son inválidos
        FileNotFoundError: Si el archivo no existe
    
    Examples:
        >>> await call_tool("crear_archivo", {
        ...     "nombre": "test.txt",
        ...     "contenido": "Hola"
        ... })
        {'success': True, 'message': 'Archivo creado'}
    """
    pass
```

---

## 📊 Diagrama completo de la arquitectura MCP

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│        APLICACIÓN DEL USUARIO (Claude, etc)           │
│                                                        │
│     ┌──────────────────────────────────────┐           │
│     │  Pregunta: "¿Cuáles son los datos?" │           │
│     └──────────────┬───────────────────────┘           │
│                    │                                    │
└────────────────────┼────────────────────────────────────┘
                     │
                     │ JSON-RPC 2.0
                     │
┌────────────────────▼────────────────────────────────────┐
│                                                        │
│           CLIENTE MCP (SDK Python)                    │
│                                                        │
│     ┌──────────────────────────────────────┐           │
│     │ Decodifica mensajes                  │           │
│     │ Maneja conexión                      │           │
│     │ Enruta solicitudes                   │           │
│     └──────────────────────────────────────┘           │
│                                                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP / WebSocket / stdio
                     │
┌────────────────────▼────────────────────────────────────┐
│                                                        │
│           SERVIDOR MCP (Tu código)                    │
│                                                        │
│     ┌──────────────────────────────────────┐           │
│     │ Descubre recursos                   │           │
│     │ Implementa herramientas              │           │
│     │ Gestiona permisos                    │           │
│     │ Retorna resultados                   │           │
│     └──────────────────────────────────────┘           │
│                                                        │
│     ┌─────────────┬─────────────┬─────────────┐        │
│     │  Recursos   │ Herramientas │ Indicadores │        │
│     │  - Archivos │ - Crear     │ - Analizar  │        │
│     │  - Datos    │ - Leer      │ - Resumen   │        │
│     │  - APIs     │ - Ejecutar  │ - Plantilla │        │
│     └─────────────┴─────────────┴─────────────┘        │
│                                                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
        ┌──────────────────────────────┐
        │  Servicios Externos          │
        ├──────────────────────────────┤
        │ 📁 Archivos del Sistema      │
        │ 🗄️  Bases de Datos          │
        │ 🌐 APIs Externas            │
        │ 📊 Datos en Tiempo Real      │
        └──────────────────────────────┘
```

---

## 🎯 Resumen de aprendizaje

### ¿Qué aprendiste?

1. ✅ **MCP es un protocolo** para conectar LLMs con recursos externos
2. ✅ **Cliente-Servidor**: Los clientes piden, los servidores responden
3. ✅ **Tres pilares**: Recursos, Herramientas e Indicadores
4. ✅ **JSON-RPC 2.0** es el formato de comunicación
5. ✅ **Seguridad first**: Siempre validar y hacer logging
6. ✅ **Escalable**: Puedes conectar múltiples fuentes de datos

### ¿Qué puedes hacer ahora?

- 🚀 Crear servidores MCP propios
- 🔌 Conectar Claude a tus datos
- 🛠️ Construir herramientas personalizadas
- 📊 Automatizar procesos
- 🔐 Hacerlo de forma segura

---

## 📚 Recursos adicionales

- [Documentación oficial MCP](https://modelcontextprotocol.io)
- [SDK Python](https://github.com/anthropics/python-sdk)
- [Ejemplos de referencia](https://github.com/anthropics/mcp-examples)
- [Comunidad Discord](https://discord.gg/anthropic)

---

## 🔗 Próximos pasos

1. **Experimenta** con los ejemplos básicos
2. **Crea** tu primer servidor
3. **Integra** datos reales
4. **Optimiza** para producción
5. **Comparte** tu servidor con la comunidad

---

**¡Felicidades! Ya entiendes MCP. Ahora es momento de crear algo increíble 🚀**
