# Ejemplos de Workflows de n8n

Este directorio contiene ejemplos prácticos de workflows de n8n para el Módulo 1 del curso.

## Archivos Disponibles

### 1. docker-compose-postgres.yml
Configuración de Docker Compose para ejecutar n8n con PostgreSQL en producción.

**Uso:**
```bash
docker-compose -f docker-compose-postgres.yml up -d
```

Acceder a n8n en: http://localhost:5678
- Usuario: admin
- Contraseña: changeme123

### 2. 01-workflow-basico.json
Workflow básico que demuestra:
- Manual trigger (Start)
- HTTP Request a una API pública (JSONPlaceholder)
- Transformación de datos con el nodo Set

**Cómo importar:**
1. Abrir n8n en el navegador
2. Click en "Add workflow" → "Import from File"
3. Seleccionar `01-workflow-basico.json`
4. Click en "Execute Workflow" para probar

**Qué hace:**
- Obtiene información de un usuario desde JSONPlaceholder API
- Extrae el nombre, email y ciudad
- Presenta los datos transformados

### 3. 02-webhook-trigger.json
Workflow con Webhook que demuestra:
- Webhook trigger (recibe peticiones HTTP POST)
- Condicional IF para verificar acción
- Diferentes respuestas según la condición

**Cómo usar:**
1. Importar el workflow
2. Activar el workflow (toggle "Active" en la esquina superior)
3. Copiar la URL del webhook
4. Probar con curl:

```bash
# Caso exitoso (acción = create)
curl -X POST http://localhost:5678/webhook/mi-webhook \
  -H "Content-Type: application/json" \
  -d '{"action": "create", "name": "Nuevo Registro"}'

# Caso error (acción diferente)
curl -X POST http://localhost:5678/webhook/mi-webhook \
  -H "Content-Type: application/json" \
  -d '{"action": "delete", "name": "Registro"}'
```

### 4. 03-expresiones-ejemplo.json
Workflow avanzado que demuestra:
- Llamada HTTP a API
- Múltiples expresiones para transformar datos
- Operaciones con strings, números y booleanos
- Uso de variables del workflow
- Filtrado condicional

**Expresiones demostradas:**
- `toUpperCase()`: Convertir a mayúsculas
- `split()`: Dividir strings
- Operador ternario: `condition ? true : false`
- Concatenación de strings
- Variables: `$now`, `$workflow.name`, `$execution.id`

**Cómo probar:**
1. Importar el workflow
2. Ejecutar con "Execute Workflow"
3. Observar cómo los datos se transforman en cada nodo
4. Revisar las expresiones en el nodo "Transformar con Expresiones"

## Estructura de un Workflow JSON

Todos los workflows de n8n tienen esta estructura básica:

```json
{
  "name": "Nombre del Workflow",
  "nodes": [
    {
      "parameters": { /* configuración del nodo */ },
      "id": "uuid-unico",
      "name": "Nombre del Nodo",
      "type": "tipo-del-nodo",
      "position": [x, y]
    }
  ],
  "connections": {
    "NodoOrigen": {
      "main": [
        [{ "node": "NodoDestino", "type": "main", "index": 0 }]
      ]
    }
  },
  "active": false,
  "settings": {},
  "tags": []
}
```

## Notas Importantes

1. **IDs únicos**: Cada nodo tiene un ID único (UUID). Si copias nodos, asegúrate de cambiar los IDs.

2. **Posiciones**: Los valores `[x, y]` en `position` determinan dónde aparece el nodo en el canvas.

3. **Conexiones**: Las conexiones definen el flujo de datos entre nodos. El formato es:
   ```json
   "NodoOrigen": {
     "main": [
       [{ "node": "NodoDestino", "type": "main", "index": 0 }]
     ]
   }
   ```

4. **Webhooks**: Los workflows con webhooks deben estar **activos** para recibir peticiones HTTP.

5. **Credenciales**: Algunos nodos requieren credenciales (API keys, OAuth, etc.). Estos workflows de ejemplo usan APIs públicas sin autenticación.

## Solución de Problemas

### Error: "Workflow could not be activated"
- Verifica que n8n esté ejecutándose
- Asegúrate de que el puerto 5678 esté disponible
- Revisa los logs: `docker logs n8n`

### Error en HTTP Request
- Verifica la conectividad a Internet
- Algunas APIs pueden tener rate limiting
- Usa APIs públicas para testing: JSONPlaceholder, httpbin.org

### Webhook no responde
- Asegúrate de que el workflow esté **activo** (toggle en ON)
- Verifica la URL del webhook en el nodo
- Usa la URL completa: `http://localhost:5678/webhook/path`

## Recursos Adicionales

- Documentación oficial: https://docs.n8n.io/
- Plantillas de la comunidad: https://n8n.io/workflows/
- Foro de la comunidad: https://community.n8n.io/

## Próximos Pasos

Después de probar estos ejemplos:
1. Modifica los workflows existentes
2. Combina diferentes nodos
3. Experimenta con expresiones propias
4. Crea tus propios workflows desde cero

¡Diviértete automatizando!
