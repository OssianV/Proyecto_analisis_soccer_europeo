# Analitica para scouting en futbol europeo

Proyecto de analisis de datos aplicado a scouting y toma de decisiones en futbol europeo. A partir de la [European Soccer Database](https://www.kaggle.com/datasets/hugomathien/soccer), utilize python, pandas y matplotlib para procesar datos historicos de jugadores y partidos, generar visualizaciones y producir una presentacion ejecutiva con hallazgos accionables.

El foco del proyecto esta en responder preguntas utiles para un cuerpo tecnico o area de scouting: que atributos conviene priorizar al evaluar talento, cuanto margen de desarrollo tienen los jugadores jovenes, a que edad suelen alcanzar su mejor nivel y que formaciones equilibran mejor uso y rendimiento.

## Resultado principal

- Presentacion final: [OUTPUTS/presentacion_final.pptx](OUTPUTS/presentacion_final.pptx)

Si quieres ver el proyecto rapidamente, ese archivo resume los analisis, graficos e interpretaciones principales.

## Hallazgos que resume el proyecto

- Existen bloques de atributos altamente correlacionados en jugadores de campo, lo que permite simplificar criterios de scouting sin perder demasiada informacion.
- En porteros tambien aparecen atributos redundantes, por lo que la evaluacion puede concentrarse en menos indicadores clave.
- Los jugadores jovenes presentan distribuciones de crecimiento potencial que ayudan a distinguir perfiles prometedores de mejoras mas normales dentro del mercado.
- El rendimiento promedio por edad sugiere una etapa de crecimiento, una meseta de prime y una fase de declive que puede orientar decisiones de fichaje.
- Algunas formaciones muestran un mejor equilibrio entre frecuencia de uso y diferencia de gol, lo que aporta contexto tactico para interpretar resultados.

## Stack y enfoque tecnico

- Python 3.13.1
- pandas y numpy para limpieza, transformacion y analisis
- matplotlib y seaborn para visualizacion
- python-pptx para generar la presentacion final
- SQLite como fuente original de datos

El flujo principal del proyecto esta dividido en tres modulos:

- [SCRIPTS/data_processing.py](SCRIPTS/data_processing.py): limpieza, estandarizacion e imputacion de datos, ademas de construccion de dataframes analiticos.
- [SCRIPTS/plots.py](SCRIPTS/plots.py): generación de graficos para cada analisis.
- [SCRIPTS/main.py](SCRIPTS/main.py): generación de la presentacion final a partir de los graficos, y analisis hechos manualmente.

## Estructura del repositorio

- [INPUTS](INPUTS): carpeta esperada para el archivo `database.sqlite` descargado manualmente.
- [SCRIPTS](SCRIPTS): codigo principal del pipeline.
- [NOTEBOOKS](NOTEBOOKS): libretas de apoyo usadas durante la exploracion, documentacion y desarrollo del analisis.
- [OUTPUTS](OUTPUTS): artefactos generados; el unico y principal es la presentacion final.
- [ATTACHMENTS](ATTACHMENTS): carpeta reservada para recursos auxiliares del proyecto (actualmente vacia).

## Como ejecutar el proyecto

1. Descarga la base de datos desde Kaggle: [European Soccer Database](https://www.kaggle.com/datasets/hugomathien/soccer).
2. Coloca el archivo `database.sqlite` dentro de [INPUTS](INPUTS).
3. Instala las dependencias necesarias.
4. Ejecuta el script principal.

```bash
pip install pandas numpy matplotlib seaborn python-pptx
python SCRIPTS/main.py
```

Al finalizar, el script genera o reemplaza [OUTPUTS/presentacion_final.pptx](OUTPUTS/presentacion_final.pptx).

## Material complementario

Las libretas en [NOTEBOOKS](NOTEBOOKS) quedan como respaldo del proceso exploratorio. La mas util para revisar el desarrollo analitico de los hallazgos es [NOTEBOOKS/Libreta_graficos_y_analisis.ipynb](NOTEBOOKS/Libreta_graficos_y_analisis.ipynb) y [NOTEBOOKS/Libreta_procesamiento_de_datos.ipynb](NOTEBOOKS/Libreta_procesamiento_de_datos.ipynb).

## Limitaciones del analisis

- La base cubre un periodo historico y no representa futbol actual.
- Parte importante de los atributos de jugadores proviene de valoraciones usadas en FIFA, por lo que sirven mejor como aproximación analitica que como verdad observacional absoluta.
- El objetivo del proyecto es exploratorio y de apoyo a decision, no construir un modelo predictivo definitivo de rendimiento.

## Pendientes a mejorar

- Limpiar scripts principales y mejorar pipeline.
- Realizar un analisis mas exhaustivo.
- Mejorar el control de excepciones.

## Autor

Ossian Ramirez

Proyecto desarrollado originalmente en un contexto academico y reorganizado como pieza de portafolio.
