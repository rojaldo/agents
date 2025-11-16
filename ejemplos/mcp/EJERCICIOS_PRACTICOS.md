# 🏋️ Ejercicios Prácticos de MCP

## Ejercicio 1: Servidor de Notas (Básico)

### Objetivo
Crear un servidor MCP que:
- Expone notas como recursos
- Permite crear, leer y eliminar notas
- Valida todas las operaciones

### Esqueleto
```python
class ServidorNotas:
    def __init__(self):
        self.notas = {}  # {id: {"titulo": ..., "contenido": ...}}
    
    async def listar_recursos(self):
        # TODO: Retornar notas como recursos
        pass
    
    async def leer_recurso(self, uri):
        # TODO: Leer una nota específica
        pass
    
    async def listar_herramientas(self):
        # TODO: Retornar herramientas disponibles
        pass
    
    async def ejecutar_herramienta(self, nombre, argumentos):
        # TODO: Implementar crear_nota, eliminar_nota
        pass
```

### Pasos
1. Implementar almacenamiento de notas
2. Crear resources/list que devuelva notas
3. Crear resources/read que lea una nota
4. Crear herramienta para crear notas
5. Crear herramienta para eliminar notas
6. Probar con cliente

### Pistas
- Usar UUID para IDs de notas
- Validar que el contenido no esté vacío
- Prevenir eliminación de notas inexistentes

---

## Ejercicio 2: Gestor de Tareas (Intermedio)

### Objetivo
Crear un servidor MCP para gestionar tareas con:
- Estados: PENDIENTE, EN_PROGRESO, COMPLETADA
- Prioridades: BAJA, MEDIA, ALTA
- Fechas de vencimiento

### Modelos de datos
```python
@dataclass
class Tarea:
    id: str
    titulo: str
    descripcion: str
    estado: str  # PENDIENTE | EN_PROGRESO | COMPLETADA
    prioridad: str  # BAJA | MEDIA | ALTA
    vencimiento: datetime
```

### Herramientas requeridas
- `crear_tarea`: Crea una nueva tarea
- `actualizar_tarea`: Modifica estado o prioridad
- `completar_tarea`: Marca como completada
- `listar_por_estado`: Retorna tareas por estado
- `listar_vencidas`: Retorna tareas vencidas

### Desafíos
1. Implementar validación de estados
2. Agregar notificaciones de tareas próximas a vencer
3. Persistencia en JSON
4. Ordenar resultados por prioridad

---

## Ejercicio 3: Cliente Inteligente (Avanzado)

### Objetivo
Crear un cliente que:
- Maneja reconexión automática
- Cachea recursos
- Reintentos con backoff exponencial
- Logging detallado

### Características avanzadas
```python
class ClienteMCPAvanzado:
    def __init__(self):
        self.cache = {}
        self.reintentos = 3
        self.timeout = 30
    
    async def conectar_con_reintentos(self):
        # TODO: Conectar con reintentos
        pass
    
    async def listar_recursos_cacheado(self):
        # TODO: Usar cache si está disponible
        pass
    
    async def ejecutar_con_timeout(self, herramienta, args):
        # TODO: Ejecutar con timeout
        pass
```

### Requisitos
- [ ] Reconexión automática
- [ ] Caché con TTL
- [ ] Reintentos con backoff
- [ ] Logging estructurado
- [ ] Métricas de rendimiento

---

## Ejercicio 4: Integración con BD (Avanzado)

### Objetivo
Crear servidor MCP que expone base de datos SQLite

### Estructura
```python
class ServidorBD:
    def __init__(self, db_path: str):
        self.conexion = sqlite3.connect(db_path)
    
    async def listar_recursos(self):
        # TODO: Retornar tablas como recursos
        pass
    
    async def leer_recurso(self, uri):
        # TODO: Ejecutar SELECT y retornar datos
        pass
    
    async def ejecutar_herramienta(self, nombre, argumentos):
        # TODO: Ejecutar INSERT, UPDATE, DELETE
        pass
```

### Herramientas
- `ejecutar_query`: Ejecuta consulta SELECT
- `insertar_registro`: Inserta un registro
- `actualizar_registro`: Actualiza un registro
- `eliminar_registro`: Elimina un registro

### Consideraciones de seguridad
- [ ] Prevenir SQL injection
- [ ] Validar permisos
- [ ] Limitar cantidad de resultados
- [ ] Logging de operaciones

---

## Ejercicio 5: Proyecto Integrador (Capstone)

### Objetivo
Crear sistema completo de gestión de proyecto

### Componentes
1. **Servidor Principal**
   - Gestiona proyectos, tareas, usuarios
   - Expone datos como recursos
   - Ejecuta operaciones

2. **Servidor Secundario**
   - Integración con APIs externas
   - Notificaciones
   - Reportes

3. **Cliente**
   - Descubre servidores
   - Coordina operaciones
   - Maneja errores

### Requisitos
- [ ] 3+ recursos diferentes
- [ ] 5+ herramientas
- [ ] Validación completa
- [ ] Manejo de errores
- [ ] Documentación
- [ ] Pruebas unitarias

### Puntos bonus
- Persistencia en BD
- Autenticación
- Rate limiting
- Caché distribuido
- Métricas

---

## Soluciones de Referencia

### Ejercicio 1: Solución básica

```python
async def listar_recursos(self):
    recursos = []
    for id, nota in self.notas.items():
        recursos.append(
            RecursoMCP(
                uri=f"note://{id}",
                nombre=nota["titulo"],
                descripcion=nota["contenido"][:50],
                tipo_mime="text/plain"
            )
        )
    return recursos

async def ejecutar_herramienta(self, nombre, argumentos):
    if nombre == "crear_nota":
        id = str(uuid.uuid4())
        self.notas[id] = {
            "titulo": argumentos["titulo"],
            "contenido": argumentos["contenido"]
        }
        return {"success": True, "id": id}
```

### Ejercicio 2: Estructura de tarea

```python
async def actualizar_tarea(self, argumentos):
    id = argumentos["id"]
    if id not in self.tareas:
        return {"success": False, "error": "Tarea no encontrada"}
    
    # Validar nuevo estado
    nuevo_estado = argumentos.get("estado")
    if nuevo_estado not in ["PENDIENTE", "EN_PROGRESO", "COMPLETADA"]:
        return {"success": False, "error": "Estado inválido"}
    
    self.tareas[id]["estado"] = nuevo_estado
    return {"success": True, "tarea": self.tareas[id]}
```

---

## Desafíos Opcionales

### 1. Servidor Multi-tenant
```python
# Cada usuario accede a sus propios datos
class ServidorMultiTenant:
    def __init__(self):
        self.datos_usuarios = {}
    
    async def listar_recursos(self, usuario_id):
        # Retornar solo recursos del usuario
        return self.datos_usuarios.get(usuario_id, {})
```

### 2. Servidor con WebSocket
```python
# Comunicación en tiempo real
@app.websocket_route("/mcp")
async def websocket_endpoint(websocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        # Procesar solicitud MCP
        respuesta = await procesar(data)
        await websocket.send_json(respuesta)
```

### 3. Servidor con Autenticación
```python
# Validar tokens en cada solicitud
def validar_token(token):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return payload["user_id"]
    except:
        return None
```

---

## Evaluación

### Criterios
| Criterio | Puntos |
|----------|--------|
| Funcionalidad | 40% |
| Seguridad | 20% |
| Documentación | 15% |
| Pruebas | 15% |
| Presentación | 10% |

### Rúbrica
- ⭐⭐⭐⭐⭐ Excelente: Todos los requisitos + extras
- ⭐⭐⭐⭐ Bueno: Todos los requisitos
- ⭐⭐⭐ Satisfactorio: 80% de requisitos
- ⭐⭐ Necesita mejora: 60% de requisitos
- ⭐ Insuficiente: Menos del 60%

---

## Recursos para Resolver Ejercicios

### Documentación
- [JSON Schema](https://json-schema.org/)
- [UUID Python](https://docs.python.org/3/library/uuid.html)
- [SQLite3](https://docs.python.org/3/library/sqlite3.html)
- [AsyncIO](https://docs.python.org/3/library/asyncio.html)

### Herramientas de Testing
```bash
# Verificar sintaxis
python -m py_compile servidor.py

# Ejecutar tests
python -m pytest tests/

# Lint
python -m pylint servidor.py

# Profiling
python -m cProfile -s cumtime servidor.py
```

---

**¡Buena suerte! Recuerda que los mejores aprendizajes vienen de los errores 🚀**
