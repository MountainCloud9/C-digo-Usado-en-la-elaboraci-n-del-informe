# AGENTS.md

## Propósito del repositorio
Este repositorio contiene scripts y documentos usados para la elaboración del informe, enfocados en:
- Curvas de calibración con método Folin-Ciocalteu (Python y R).
- Generación de figuras y tablas para reporte académico.

## Estructura principal
- `*.py`: calculadoras interactivas y scripts de análisis/figuras.
- `*.R` / `*.r`: scripts de visualización y análisis en R.
- `*.tex`: documentos en LaTeX para el informe.
- `README.md` y `TABLA_REFERENCIA_RAPIDA.md`: contexto general y referencia experimental.

## Flujo recomendado para agentes
1. Mantener cambios mínimos y enfocados en la tarea solicitada.
2. No renombrar archivos existentes (hay nombres con espacios y acentos usados por el proyecto).
3. Evitar editar datos experimentales sin instrucción explícita.
4. Si se agrega código Python nuevo, preferir estilo simple y compatible con ejecución por script (`python archivo.py`).
5. Si se agregan dependencias, documentarlas en el PR o en README.

## Ejecución local (referencia)
- Python: `python "<archivo>.py"`
- R: `Rscript "<archivo>.R"`

Dependencias observadas en scripts:
- Python: `pandas`, `numpy`, `matplotlib`, `scipy`, `tabulate`
- R: `ggplot2`, `dplyr`, `tidyr`, `ggpubr`, `gridExtra`, `grid`

## Validación
Actualmente no hay una suite formal de tests/lint en el repositorio.
Cuando se modifique código:
- Ejecutar el/los script(s) tocados y confirmar que no fallen.
- Verificar que las salidas esperadas (tablas/figuras/texto) se generen correctamente.

## Entregables y archivos generados
Varios scripts generan archivos `.txt` o `.png`.
- No sobrescribir resultados críticos sin solicitud del usuario.
- No incluir artefactos temporales o de pruebas en commits, salvo que se pidan explícitamente.
