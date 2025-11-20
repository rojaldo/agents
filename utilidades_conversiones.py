"""
Utilidades para convertir entre formatos JSON, YAML y TOML
"""

import json
import yaml
import toml
from pathlib import Path
from typing import Any, Union


class ConvertidorFormatos:
    """Clase para convertir entre formatos de configuración"""

    @staticmethod
    def json_a_yaml(datos_json: Union[str, dict]) -> str:
        """
        Convierte JSON a YAML

        Args:
            datos_json: String JSON o diccionario Python

        Returns:
            String en formato YAML
        """
        if isinstance(datos_json, str):
            datos = json.loads(datos_json)
        else:
            datos = datos_json

        return yaml.dump(datos, default_flow_style=False, allow_unicode=True)

    @staticmethod
    def yaml_a_json(datos_yaml: Union[str, dict]) -> str:
        """
        Convierte YAML a JSON

        Args:
            datos_yaml: String YAML o diccionario Python

        Returns:
            String en formato JSON formateado
        """
        if isinstance(datos_yaml, str):
            datos = yaml.safe_load(datos_yaml)
        else:
            datos = datos_yaml

        return json.dumps(datos, indent=2, ensure_ascii=False)

    @staticmethod
    def json_a_toml(datos_json: Union[str, dict]) -> str:
        """
        Convierte JSON a TOML

        Args:
            datos_json: String JSON o diccionario Python

        Returns:
            String en formato TOML
        """
        if isinstance(datos_json, str):
            datos = json.loads(datos_json)
        else:
            datos = datos_json

        return toml.dumps(datos)

    @staticmethod
    def toml_a_json(datos_toml: Union[str, dict]) -> str:
        """
        Convierte TOML a JSON

        Args:
            datos_toml: String TOML o diccionario Python

        Returns:
            String en formato JSON formateado
        """
        if isinstance(datos_toml, str):
            datos = toml.loads(datos_toml)
        else:
            datos = datos_toml

        return json.dumps(datos, indent=2, ensure_ascii=False)

    @staticmethod
    def yaml_a_toml(datos_yaml: Union[str, dict]) -> str:
        """
        Convierte YAML a TOML

        Args:
            datos_yaml: String YAML o diccionario Python

        Returns:
            String en formato TOML
        """
        if isinstance(datos_yaml, str):
            datos = yaml.safe_load(datos_yaml)
        else:
            datos = datos_yaml

        return toml.dumps(datos)

    @staticmethod
    def toml_a_yaml(datos_toml: Union[str, dict]) -> str:
        """
        Convierte TOML a YAML

        Args:
            datos_toml: String TOML o diccionario Python

        Returns:
            String en formato YAML
        """
        if isinstance(datos_toml, str):
            datos = toml.loads(datos_toml)
        else:
            datos = datos_toml

        return yaml.dump(datos, default_flow_style=False, allow_unicode=True)

    @staticmethod
    def archivo_a_json(ruta: str) -> str:
        """
        Lee un archivo (JSON, YAML o TOML) y lo convierte a JSON

        Args:
            ruta: Ruta del archivo

        Returns:
            String en formato JSON
        """
        ruta_path = Path(ruta)
        extension = ruta_path.suffix.lower()
        contenido = ruta_path.read_text(encoding='utf-8')

        if extension == '.json':
            datos = json.loads(contenido)
        elif extension in ['.yaml', '.yml']:
            datos = yaml.safe_load(contenido)
        elif extension == '.toml':
            datos = toml.loads(contenido)
        else:
            raise ValueError(f"Formato no soportado: {extension}")

        return json.dumps(datos, indent=2, ensure_ascii=False)

    @staticmethod
    def archivo_a_yaml(ruta: str) -> str:
        """
        Lee un archivo (JSON, YAML o TOML) y lo convierte a YAML

        Args:
            ruta: Ruta del archivo

        Returns:
            String en formato YAML
        """
        ruta_path = Path(ruta)
        extension = ruta_path.suffix.lower()
        contenido = ruta_path.read_text(encoding='utf-8')

        if extension == '.json':
            datos = json.loads(contenido)
        elif extension in ['.yaml', '.yml']:
            datos = yaml.safe_load(contenido)
        elif extension == '.toml':
            datos = toml.loads(contenido)
        else:
            raise ValueError(f"Formato no soportado: {extension}")

        return yaml.dump(datos, default_flow_style=False, allow_unicode=True)

    @staticmethod
    def archivo_a_toml(ruta: str) -> str:
        """
        Lee un archivo (JSON, YAML o TOML) y lo convierte a TOML

        Args:
            ruta: Ruta del archivo

        Returns:
            String en formato TOML
        """
        ruta_path = Path(ruta)
        extension = ruta_path.suffix.lower()
        contenido = ruta_path.read_text(encoding='utf-8')

        if extension == '.json':
            datos = json.loads(contenido)
        elif extension in ['.yaml', '.yml']:
            datos = yaml.safe_load(contenido)
        elif extension == '.toml':
            datos = toml.loads(contenido)
        else:
            raise ValueError(f"Formato no soportado: {extension}")

        return toml.dumps(datos)

    @staticmethod
    def guardar_conversion(contenido: str, ruta_salida: str) -> None:
        """
        Guarda el contenido en un archivo

        Args:
            contenido: Contenido a guardar
            ruta_salida: Ruta del archivo de salida
        """
        Path(ruta_salida).write_text(contenido, encoding='utf-8')


# Funciones de conveniencia directa
def json_a_yaml(datos: Union[str, dict]) -> str:
    """Convierte JSON a YAML"""
    return ConvertidorFormatos.json_a_yaml(datos)


def yaml_a_json(datos: Union[str, dict]) -> str:
    """Convierte YAML a JSON"""
    return ConvertidorFormatos.yaml_a_json(datos)


def json_a_toml(datos: Union[str, dict]) -> str:
    """Convierte JSON a TOML"""
    return ConvertidorFormatos.json_a_toml(datos)


def toml_a_json(datos: Union[str, dict]) -> str:
    """Convierte TOML a JSON"""
    return ConvertidorFormatos.toml_a_json(datos)


def yaml_a_toml(datos: Union[str, dict]) -> str:
    """Convierte YAML a TOML"""
    return ConvertidorFormatos.yaml_a_toml(datos)


def toml_a_yaml(datos: Union[str, dict]) -> str:
    """Convierte TOML a YAML"""
    return ConvertidorFormatos.toml_a_yaml(datos)


if __name__ == '__main__':
    # Ejemplo de uso
    datos_json = {
        "nombre": "Juan",
        "edad": 30,
        "ciudad": "Madrid",
        "hobbies": ["leer", "programar", "correr"]
    }

    print("=" * 50)
    print("DATOS ORIGINALES (DICT):")
    print(datos_json)

    print("\n" + "=" * 50)
    print("CONVERSIÓN A YAML:")
    yaml_resultado = json_a_yaml(datos_json)
    print(yaml_resultado)

    print("=" * 50)
    print("CONVERSIÓN A TOML:")
    toml_resultado = json_a_toml(datos_json)
    print(toml_resultado)

    print("=" * 50)
    print("VUELTA A JSON desde YAML:")
    json_resultado = yaml_a_json(yaml_resultado)
    print(json_resultado)
