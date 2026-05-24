# Proyecto Analisis de Datos

---

Abstract: [PENDIENTE] - Poner un resumen del proyecto de un parrafo y pocas oraciones.

## Estructura del proyecto

El repositorio contiene dos archivos relevante importantes: (1) Scripts principales, y (2) Libretas de Jupyter secundarias.

La base de datos no esta en repositorio, para descargarla dirigase a en kaggle usando [este link.](https://www.kaggle.com/datasets/hugomathien/soccer). La base de datos tiene que estar en la carpeta `INPUTS`.

### Scripts principales

- [main.py](SCRIPTS/main.py)
- [plots.py](SCRIPTS/plots.py)
- [data_processing.py](SCRIPTS/data_processing.py)

Solo se tiene que ejectuar main.py. Este generara la presentacion final en la carpeta OUTPUTS.

Notese que se realizo con la version 3.13.1 de python. Tambien asegurese de tener las librerias utilizadas instaladas. Estas deben ser:

- pandas
- numpy
- matplotlib
- seaborn
- python-pptx

### Libretas de Jupyter secundarias

- [Libreta_sqlite_basics](SCRIPTS/Libreta_sqlite_basics.ipynb): Libreta con un tutorial basico de como leer las tablas del archivo .sqlite y pasarlas a un dataframe + un poco de teoria
- [Libreta_resumen_bd](SCRIPTS/Libreta_resumen_bd.ipynb): Libreta resumen de la base de datos, explicando que informacion contiene cada columna.
- [Libreta_graficos_y_analisis](SCRIPTS/Libreta_graficos_y_analisis.ipynb): Libreta donde se hicieron los 10 analisis y sus graficos.
- [Libreta_planteamiento_de_insights](SCRIPTS/Libreta_planteamiento_de_insights.ipynb): Libreta donde se plantearon los insights a realizar.
- [Libreta_procesamiento_de_datos](SCRIPTS/Libreta_procesamiento_de_datos.ipynb): Libreta donde se hizo todo el procesado de datos.


## Direccion del analisis

La direccion de analisis es la de obtener insights relevantes que podamos dar a un director tecnico o al personal que se encarga de hacer scouting de un equipo de futbol europeo.

Nos centraremos en analizar y generar sugerencias del tipo de jugador a scoutear, de las formacion a usar, de las mejores formas de identificar un jugador valioso, de los atributos de jugadores que mayor impacto tienen en ganar un partido, etc. El analisis entonces podra incluir observaciones hechas a travez de las diferentes ligas que se incluyen en el dataset.

## Tutoriales, articulos, documentacion relevante

- La base de datos en kaggle es [esta](https://www.kaggle.com/datasets/hugomathien/soccer)
- Si no saben usar github y git, yo aprendi lo superbasico usando [esta lista de reproduccion](https://www.youtube.com/watch?v=BCQHnlnPusY&list=PLRqwX-V7Uu6ZF9C0YMKuns9sLDzK6zoiV). Alternativamente, pueden usar los propios [tutoriales de github](https://docs.github.com/en/get-started/start-your-journey/hello-world). O solo preguntenle a un LLM.
- Para que aprendan a usar la funcion de "issues", solo vean [este video](https://www.youtube.com/watch?v=WMykv2ZMyEQ&list=PLRqwX-V7Uu6ZF9C0YMKuns9sLDzK6zoiV&index=4)
- Como la base de datos es un archivo .sqlite, para aprender lo basico de sqlite yo estoy usando [este recurso](https://www.sqlitetutorial.net/)


Extras:
- Lo basico de pandas lo pueden encontrar [aqui](https://pandas.pydata.org/docs/user_guide/index.html)
- Para que entiendan como funciona la programacion modular vean [este short](https://www.youtube.com/shorts/Ju6tP03GI7c). Para que vean como se veria un modulo creado por ustedes muy sencillo vean [este video](https://www.youtube.com/watch?v=cgxEqlGJcrY). Cuando yo he usado modulos siempre defino clases, y funciones dentro de clases; si puueden hagan lo mismo, aunque como se ve en el ultimo video esto no es necesario.
