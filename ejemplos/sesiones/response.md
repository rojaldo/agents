 # Cómo Crear una Función en Python

Crear una función en Python es un concepto fundamental en la programación y se utiliza para agrupar código común y reutilizarlo en diferentes partes de un programa. A continuación, te explicaré paso a paso cómo crear una función en Python.

## Definición de una función

Una función en Python se define utilizando la palabra clave `def` seguida del nombre de la función, los parámetros que recibirá y el código que realizará dentro de ella. Por ejemplo:

```python
def suma(num1, num2):
    return num1 + num2
```

En este ejemplo, estamos creando una función llamada `suma` que recibirá dos números como argumentos (`num1` y `num2`) y devolverá su suma.

## Parámetros

Los parámetros se definen entre los paréntesis de la función. Pueden ser valores simples (como números o cadenas) o incluso otras funciones. Por ejemplo:

```python
def saludo(nombre):
    return "Hola, " + nombre

print(saludo("Juan"))  # Salida: Hola, Juan
```

En este caso, estamos creando una función llamada `saludo` que recibirá un nombre como argumento y devolverá un mensaje personalizado.

## Return

El operador `return` se utiliza para especificar qué valor devolver la función. Puedes utilizar valores simples (como números o cadenas) o incluso funciones más complejas. Por ejemplo:

```python
def factorial(num):
    if num == 0:
        return 1
    else:
        return num * factorial(num-1)

print(factorial(5))  # Salida: 120
```

En este caso, estamos creando una función llamada `factorial` que calculará el factorial de un número ingresado.

## Ejemplos

Aquí te presento algunos ejemplos más para ilustrar la creación de funciones en Python:

```python
def mayor_de_tres(num1, num2, num3):
    return max(num1, num2, num3)

print(mayor_de_tres(5, 10, 15))  # Salida: 15

def concatenar(cadena1, cadena2):
    return cadena1 + cadena2

print(concatenar("Hola", " Mundo"))  # Salida: Hola Mundo
```

## Conclusión

En resumen, crear una función en Python implica definir un nombre para la función, especificar los parámetros que recibirá y devolver un valor o incluso otra función. Al seguir estos pasos, podrás crear funciones personalizadas para simplificar tus programas y aumentar tu productividad.  