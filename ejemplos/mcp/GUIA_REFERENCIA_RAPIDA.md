# 📚 Guía de Referencia Rápida - MCP

## Conceptos en 2 minutos

### ¿Qué es MCP?
Un protocolo para que modelos de IA accedan a datos y ejecuten acciones de forma segura.

```
Tu Código → [MCP] → Claude
             ↕
         Recursos + Herramientas
```

---

## Componentes Esenciales

### 1. Servidor MCP
```python
from mcp.server import Server

app = Server("mi-servidor")

@app.list_resources()
async def resources():
    return [...]

@app.list_tools()
async def tools():
    return [...]

@app.call_tool()
async def call_tool(name, arguments):
    return {...}
```

### 2. Cliente MCP
```python
# Conectar
await cliente.conectar()

# Descubrir
recursos = await cliente.listar_recursos()
herramientas = await cliente.listar_herramientas()

# Usar
contenido = await cliente.leer_recurso(uri)
resultado = await cliente.ejecutar_herramienta(nombre, args)

# Desconectar
await cliente.desconectar()
```

---

## Métodos MCP Principales

| Método | Dirección | Descripción |
|--------|-----------|-------------|
| `resources/list` | → | Obtener lista de recursos |
| `resources/read` | → | Leer un recurso |
| `tools/list` | → | Obtener lista de herramientas |
| `tools/call` | → | Ejecutar una herramienta |
| `prompts/list` | → | Obtener lista de indicadores |
| `prompts/get` | → | Obtener un indicador |

---

## Estructura de Solicitud/Respuesta

### Solicitud (JSON-RPC 2.0)
```json
{
  "jsonrpc": "2.0",
  "method": "resources/list",
  "params": {},
  "id": 1
}
```

### Respuesta exitosa
```json
{
  "jsonrpc": "2.0",
  "result": {
    "resources": [...]
  },
  "id": 1
}
```

### Respuesta con error
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

---

## Tipos de Datos Clave

### Recurso
```python
{
    "uri": "file:///datos/archivo.txt",
    "name": "archivo.txt",
    "description": "Descripción",
    "mimeType": "text/plain"
}
```

### Herramienta
```python
{
    "name": "crear_archivo",
    "description": "Crea un archivo",
    "inputSchema": {
        "type": "object",
        "properties": {
            "nombre": {"type": "string"}
        },
        "required": ["nombre"]
    }
}
```

### Indicador (Prompt)
```python
{
    "name": "analizar",
    "description": "Analiza un documento",
    "arguments": [
        {
            "name": "tipo",
            "description": "Tipo de análisis"
        }
    ]
}
```

---

## Flujo Completo

```
1. INICIALIZACIÓN
   Cliente ──[initialize]──→ Servidor
           ←─[capabilities]──

2. DESCUBRIMIENTO
   Cliente ──[resources/list]──→ Servidor
           ←───[recursos]────

3. USO
   Cliente ──[tools/call]──→ Servidor
           ←──[resultado]──

4. CIERRE
   Cliente ──[shutdown]──→ Servidor
           ←─[ok]────
```

---

## Códigos de Error JSON-RPC

| Código | Significado |
|--------|------------|
| -32700 | Parse error |
| -32600 | Solicitud inválida |
| -32601 | Método no encontrado |
| -32602 | Parámetros inválidos |
| -32603 | Error interno |
| -32000 a -32099 | Errores específicos del servidor |

---

## Mejores Prácticas

### ✅ DO (Hacer)
- Validar todos los inputs
- Usar logging detallado
- Implementar timeout
- Documentar esquemas
- Manejar errores explícitamente
- Usar URIs descriptivos

### ❌ DON'T (No hacer)
- Ejecutar comandos sin validar
- Permitir path traversal
- Ignorar errores
- Usar URIs genéricos
- Exponer información sensible
- Permitir ejecución arbitraria

---

## Casos de Uso Comunes

### 1. Acceso a Base de Datos
```python
# Servidor expone tablas como recursos
# Cliente lee datos
recursos = await cliente.listar_recursos()
# "db://tabla/usuarios", "db://tabla/productos"
```

### 2. Ejecución de Scripts
```python
# Servidor ejecuta scripts mediante herramientas
resultado = await cliente.ejecutar_herramienta(
    "ejecutar_script",
    {"nombre": "backup.py"}
)
```

### 3. Integración con APIs
```python
# Servidor conecta con APIs externas
resultado = await cliente.ejecutar_herramienta(
    "obtener_clima",
    {"ciudad": "Madrid"}
)
```

### 4. Análisis de Documentos
```python
# Servidor lee archivos y recursos
contenido = await cliente.leer_recurso("file:///docs/paper.pdf")
# Cliente (Claude) analiza
```

---

## Configuración Típica

### `mcp_config.json`
```json
{
  "mcpServers": {
    "base-datos": {
      "command": "python",
      "args": ["servidor_bd.py"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    },
    "api-externa": {
      "command": "python",
      "args": ["servidor_api.py"],
      "env": {
        "API_KEY": "tu-clave"
      }
    }
  }
}
```

---

## Debugging

### Habilitar logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Solicitud: {solicitud}")
logger.info(f"Ejecutando: {nombre}")
logger.error(f"Error: {e}")
```

### Probar conexión
```bash
# Verificar que el servidor está corriendo
python servidor_mcp.py

# En otra terminal, probar cliente
python cliente_mcp.py
```

---

## Recursos Útiles

- 📖 [Docs Oficiales](https://modelcontextprotocol.io)
- 💻 [Repositorio](https://github.com/anthropics/python-sdk)
- 🎓 [Ejemplos](https://github.com/anthropics/mcp-examples)
- 🤝 [Comunidad](https://discord.gg/anthropic)

---

## Cheat Sheet Terminal

```bash
# Instalar MCP
pip install mcp

# Ejecutar servidor
python servidor_mcp.py

# Ejecutar cliente
python cliente_mcp.py

# Verificar logs
tail -f server.log

# Limpiar data
rm -rf mcp_data/*

# Probar conexión JSON-RPC
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"resources/list","id":1}'
```

---

**🎯 Recuerda: MCP = Seguridad + Estandarización + Integración**
