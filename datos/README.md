# Datos

Esta carpeta contiene los conjuntos de datos utilizados en el análisis.

## Subcarpetas

- **brutos/**: Datos originales tal como fueron obtenidos, sin ninguna modificación.
- **procesados/**: Datos que han pasado por un proceso de limpieza y transformación, listos para el análisis.

## Notas

- Los datos brutos **no deben modificarse** directamente; cualquier transformación debe realizarse mediante scripts ubicados en `scripts/preprocesamiento/`.
- Si los datos contienen información sensible o son de gran tamaño, pueden no estar incluidos en el repositorio. En ese caso, se incluirá un archivo de instrucciones sobre cómo obtenerlos.
