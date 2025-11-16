# MÓDULO 7: Webhooks y APIs - Ejemplos Funcionales

Este módulo cubre la creación de webhooks en n8n y consumo de APIs externas.

## Ejemplos

### 01-webhook-basico.json
- **Concepto**: Crear un webhook que reciba datos HTTP
- **Nodos**: Webhook trigger → Process → HTTP Response
- **Uso**: Exponer un endpoint n8n para recibir datos

### 02-webhook-slack-notification.json
- **Concepto**: Webhook que envía notificaciones a Slack
- **Nodos**: Webhook → Slack node → Response
- **Uso**: Automatizar notificaciones desde terceros

### 03-consumir-api-pública.json
- **Concepto**: Llamar APIs públicas con autenticación
- **Nodos**: HTTP Request → Parse → Transform
- **Uso**: Integración con servicios externos

### 04-webhook-con-validacion.json
- **Concepto**: Validar datos en webhook antes de procesar
- **Nodos**: Webhook → Validate → Process o Error
- **Uso**: Asegurar integridad de datos recibidos

### 05-rate-limiting.json
- **Concepto**: Implementar rate limiting en webhooks
- **Nodos**: Webhook → Delay → Execute
- **Uso**: Proteger contra spam y abuso

## Conceptos Clave

### Webhooks
- URL única por workflow
- Métodos HTTP soportados (GET, POST, PUT, DELETE)
- Parámetros y query strings
- Headers personalizados
- Respuestas HTTP configurables

### APIs REST
- Métodos CRUD (GET, POST, PUT, DELETE)
- Autenticación (API Key, Bearer, Basic, OAuth)
- Headers y body
- Manejo de errores HTTP
- Parsing de respuestas

### Rate Limiting
- Limitar llamadas por tiempo
- Esperar entre requests
- Manejar 429 Too Many Requests
- Implementar backoff exponencial
