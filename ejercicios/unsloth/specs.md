# esto es para entrenar un lora de modelo de lenguaje con unsloth

## Usa los contenidos de la carpeta `data` para entrenar un modelo de lenguaje con la librería UnsLoTh.
## haz el proceso fragmentado de la informacion de los archivos en trozos de 2048 tokens como maximo.
## Por defecto framenta por frases
## genera un lora de 8 bits
## usa estos parametros:
- modelo base: "mistralai/Mistral-7B-v0.1"
- tasa de aprendizaje: 3e-4
- tamaño de batch: 16
- epochs: 3
- lora_rank: 16
- lora_alpha: 32
- lora_dropout: 0.05
- lora_target: all

## guarda el modelo entrenado en la carpeta `unsloth_model`