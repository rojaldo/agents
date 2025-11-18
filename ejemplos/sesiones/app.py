from langchain_ollama import OllamaLLM
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()
# Usar las variables de entorno para configurar el modelo
model_name = os.getenv("OLLAMA_MODEL", "mistral")
base_url = os.getenv("OLLAMA_BASE_URL", "http://google.com")

# set temperature to 0.7
llm = OllamaLLM(model=model_name, base_url=base_url, temperature=0.7)
respuesta = llm.invoke("¿Hola?")
print(respuesta)