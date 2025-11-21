# LoRA Training with Unsloth

Este proyecto entrena un modelo LoRA usando Unsloth sobre la librería Mistral 7B.

## Estructura

- `data/` - Carpeta con archivos de entrenamiento (archivos .md, .txt, .json)
- `train_lora.py` - Script principal de entrenamiento
- `unsloth_model/` - Directorio donde se guarda el modelo entrenado
- `specs.md` - Especificaciones del proyecto

## Características

- **Fragmentación inteligente**: Divide el texto en fragmentos de máximo 2048 tokens
- **Separación por oraciones**: Fragmenta por oraciones para mantener coherencia
- **LoRA de 8 bits**: Entrenamiento eficiente en memoria
- **Modelo base**: Mistral 7B v0.1

## Parámetros de entrenamiento

- Learning rate: 3e-4
- Batch size: 16
- Epochs: 3
- LoRA rank: 16
- LoRA alpha: 32
- LoRA dropout: 0.05

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python train_lora.py
```

El script automáticamente:
1. Carga todos los archivos .md de la carpeta `data/`
2. Divide el texto en fragmentos de máximo 2048 tokens
3. Carga el modelo Mistral 7B con optimizaciones de Unsloth
4. Entrena un adaptador LoRA
5. Guarda el modelo entrenado en la carpeta `unsloth_model/`

## Requisitos del sistema

- GPU NVIDIA con al menos 8GB de memoria
- CUDA 11.8+
- Python 3.10+
- 10+ GB de espacio en disco

## Notas

El entrenamiento puede tardar de 30 minutos a varias horas dependiendo del tamaño del dataset y hardware disponible.
