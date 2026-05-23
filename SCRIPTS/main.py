from pathlib import Path

from io import BytesIO
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

from plots import build_graph_figures

# Colores
COLOR_FONDO = "F7F7F2"
COLOR_TEXTO = "1F2937"
COLOR_PRINCIPAL = "1D4E89"
COLOR_SECUNDARIO = "2A9D8F"
COLOR_ALERTA = "D95D39"
COLOR_NEUTRO = "8D99AE"

# Mejor forma de manejar direcciones de archivos

script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent

database_path = project_root / "INPUTS" / "database.sqlite"
output_path = project_root / "OUTPUTS" / "presentacion_final.pptx"

def rgb(hex_color):
    hex_color = hex_color.replace("#", "")
    return RGBColor(
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16)
    )


def crear_presentacion(output_path, analyses, integrantes):
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    def nueva_slide():
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = rgb(COLOR_FONDO)
        return slide

    def agregar_texto(slide, left, top, width, height, texto, tamano, color, negrita=False):
        box = slide.shapes.add_textbox(left, top, width, height)
        tf = box.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT

        run = p.add_run()
        run.text = texto
        run.font.name = "Aptos"
        run.font.size = Pt(tamano)
        run.font.bold = negrita
        run.font.color.rgb = rgb(color)

    def agregar_parrafos(slide, left, top, width, height, texto, tamano=18):
        box = slide.shapes.add_textbox(left, top, width, height)
        tf = box.text_frame
        tf.word_wrap = True
        tf.clear()

        parrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]

        for i, parrafo in enumerate(parrafos):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = parrafo
            p.space_after = Pt(10)

            for run in p.runs:
                run.font.name = "Aptos"
                run.font.size = Pt(tamano)
                run.font.color.rgb = rgb(COLOR_TEXTO)

    # Portada
    slide = nueva_slide()
    agregar_texto(
        slide,
        Inches(0.9), Inches(1.4),
        Inches(10.5), Inches(1.0),
        "Analisis de datos para decisiones futbolisticas",
        24,
        COLOR_PRINCIPAL,
        True
    )
    agregar_texto(
        slide,
        Inches(0.9), Inches(2.4),
        Inches(10.8), Inches(0.8),
        "Scouting, perfiles de jugador, valor competitivo y apoyo a decisiones tacticas",
        15,
        COLOR_NEUTRO
    )
    agregar_texto(
        slide,
        Inches(0.9), Inches(4.3),
        Inches(10.5), Inches(1.2),
        "Presentacion con graficas e interpretaciones del analisis.",
        18,
        COLOR_TEXTO
    )

    # Analisis
    for i, analysis in enumerate(analyses, start=1):
        # Slide de grafica
        slide = nueva_slide()
        agregar_texto(
            slide,
            Inches(0.7), Inches(0.5),
            Inches(11.0), Inches(0.5),
            f"Analisis {i:02d}: {analysis['title']}",
            20,
            COLOR_PRINCIPAL,
            True
        )

        figure = analysis["figure"]

        image_stream = BytesIO()
        figure.savefig(image_stream, format="png", dpi=200, bbox_inches="tight")
        image_stream.seek(0)

        max_width = 11.0
        max_height = 5.4

        fig_width, fig_height = figure.get_size_inches()
        scale = min(max_width / fig_width, max_height / fig_height)

        final_width = fig_width * scale
        final_height = fig_height * scale

        left = 1.0 + (max_width - final_width) / 2
        top = 1.3 + (max_height - final_height) / 2

        slide.shapes.add_picture(
            image_stream,
            Inches(left), Inches(top),
            width=Inches(final_width),
            height=Inches(final_height)
        )

        # Slide de texto
        slide = nueva_slide()
        agregar_texto(
            slide,
            Inches(0.7), Inches(0.5),
            Inches(11.0), Inches(0.5),
            f"Lectura del analisis {i:02d}: {analysis['title']}",
            20,
            COLOR_SECUNDARIO,
            True
        )
        agregar_parrafos(
            slide,
            Inches(0.9), Inches(1.4),
            Inches(11.2), Inches(5.6),
            analysis["analysis_text"],
            18
        )

    # Slide final
    slide = nueva_slide()
    agregar_texto(
        slide,
        Inches(0.9), Inches(1.5),
        Inches(5.0), Inches(0.6),
        "Integrantes",
        24,
        COLOR_PRINCIPAL,
        True
    )
    agregar_parrafos(
        slide,
        Inches(1.0), Inches(2.5),
        Inches(5.0), Inches(3.0),
        "\n\n".join(integrantes),
        20
    )

    prs.save(output_path)


if __name__ == "__main__":

    grafico_01, grafico_02, grafico_03, grafico_04, grafico_05, grafico_06, grafico_07, grafico_08, grafico_09, grafico_10 = build_graph_figures(database_path) 

    analyses = [
        {
            "title": "Que atributos mirar en jugadores de campo?",
            "figure": grafico_01,
            "analysis_text": """En el heatmap de jugadores de campo se observan bloques claros de atributos que se mueven casi juntos. Por ejemplo, ACCELERATION y SPRINT_SPEED tienen una correlación muy alta (0.89), lo que sugiere que ambas variables describen casi la misma dimensión de rapidez. Algo parecido ocurre con INTERCEPTIONS y STANDING_TACKLE (0.89), que representan un perfil defensivo muy similar.

También aparece un bloque técnico-ofensivo bastante marcado. DRIBBLING y BALL_CONTROL tienen una correlación alta (0.85), mientras que SHORT_PASSING y LONG_PASSING también se relacionan fuertemente (0.80). Además, FINISHING y POSITIONING muestran una correlación importante (0.80), lo que indica que los jugadores que suelen ubicarse mejor en zonas de ataque también tienden a definir mejor.

A nivel general, OVERALL_RATING se relaciona bastante con POTENTIAL (0.81) y con REACTIONS (0.78). Esto sugiere que la valoración global del jugador no depende de un solo atributo aislado, sino de combinaciones de técnica, lectura de juego y capacidad física. En otras palabras, para scouting de jugadores de campo no conviene tratar todas estas variables como independientes, porque varias son parcialmente redundantes y pueden resumirse por bloques."""
        },
        {
            "title": "Que atributos mirar en porteros?",
            "figure": grafico_02,
            "analysis_text": """En el heatmap de porteros se observa una estructura mucho más concentrada que en jugadores de campo. La variable OVERALL_RATING está fuertemente relacionada con casi todos los atributos específicos de arquero, en especial con GK_MEAN (0.98), GK_DIVING (0.91), GK_REFLEXES (0.90), GK_POSITIONING (0.89) y GK_HANDLING (0.88). Esto indica que el rendimiento general del portero está muy dominado por sus habilidades técnicas propias del puesto.

También se ven relaciones altas entre atributos internos del arco. Por ejemplo, GK_DIVING y GK_REFLEXES tienen una correlación de 0.89, mientras que GK_POSITIONING y GK_HANDLING alcanzan 0.83. Esto sugiere que varios indicadores del portero miden casi la misma calidad subyacente, por lo que existe bastante redundancia entre ellos.

En cambio, JUMPING muestra una relación bastante menor con el bloque principal de variables de arquero. Por ejemplo, su correlación con GK_MEAN es solo de 0.40. Esto sugiere que el salto aporta información complementaria, pero no explica tanto el nivel global del portero como las habilidades técnicas de atajada, colocación y reflejos.

En conjunto, este gráfico sugiere que para evaluar porteros se puede resumir gran parte del perfil usando pocas variables clave, porque muchas de las métricas del puesto se mueven casi juntas. A diferencia de los jugadores de campo, aquí la redundancia es más fuerte y el perfil parece estar más concentrado en un solo bloque de rendimiento especializado."""
        },
        {
            "title": "Cuanto margen tienen los campistas jovenes?",
            "figure": grafico_03,
            "analysis_text": """En el histograma de jugadores de campo se observa que la gran mayoría de los casos tiene un gap positivo entre POTENTIAL y OVERALL_RATING. Esto sugiere que, dentro de este grupo de jugadores jóvenes, lo normal es que todavía exista margen de desarrollo y que su nivel actual aún esté por debajo de su techo estimado.

La distribución se concentra sobre todo entre valores de gap de 7 a 11, con una mediana cercana a 8. Esto indica que, para muchos jugadores de campo jóvenes, el margen de crecimiento existe, pero no suele ser extremo. Los casos con gaps muy altos también aparecen, incluso llegando a valores cercanos a 22, pero claramente son menos frecuentes y pueden interpretarse como perfiles especialmente interesantes para scouting.

En conjunto, el gráfico sugiere que los jugadores de campo jóvenes suelen tener un margen de desarrollo moderado y relativamente estable. Por eso, al buscar prospectos, conviene prestar más atención a los casos que se alejan hacia la derecha de la distribución, ya que ahí es donde aparecen jugadores con un potencial mucho más alto que su rendimiento actual."""
        },
        {
            "title": "Cuanto margen tienen los porteros jovenes?",
            "figure": grafico_04,
            "analysis_text": """En el histograma de porteros también se observa una distribución claramente desplazada hacia valores positivos de gap. Esto sugiere que los arqueros jóvenes del dataset, al igual que los jugadores de campo, suelen conservar margen de desarrollo entre su POTENTIAL y su OVERALL_RATING.

En este caso, la distribución se concentra principalmente entre 7 y 12, con una mediana cercana a 9. Esto sugiere un margen de crecimiento ligeramente mayor que el observado en jugadores de campo. Sin embargo, aquí el número de observaciones es bastante menor, por lo que conviene interpretar el patrón con más cuidado y no sacar conclusiones demasiado fuertes a partir de pequeñas diferencias.

En conjunto, el gráfico indica que los porteros jóvenes también presentan espacio para mejorar, pero el análisis debe leerse con más prudencia por el tamaño de muestra. Aun así, los casos ubicados hacia la derecha de la distribución pueden verse como porteros especialmente prometedores, ya que combinan un nivel actual todavía contenido con un techo estimado más alto."""
        },
        {
            "title": "Que distingue a los jovenes con alto potencial?",
            "figure": grafico_05,
            "analysis_text": """En este gráfico se observa que los jugadores jóvenes de alto potencial no se diferencian tanto por atributos defensivos o físicos puros, sino sobre todo por rasgos técnicos y ofensivos. Los atributos que más sobresalen son DRIBBLING, CURVE, BALL_CONTROL, LONG_SHOTS, POSITIONING y VISION, lo que sugiere que el techo de desarrollo suele estar más asociado con calidad técnica y capacidad ofensiva que con fuerza o juego defensivo.

También destaca que SHORT_PASSING, CROSSING, SHOT_POWER y REACTIONS aparecen entre las diferencias más altas. Esto sugiere que los jugadores más prometedores no solo tienen habilidad individual, sino también mejores recursos para participar en la circulación del balón y resolver jugadas con más calidad.

En conjunto, el gráfico sugiere que, al buscar talento joven con margen de crecimiento, conviene priorizar perfiles con buena técnica ofensiva, control de balón y lectura de juego. De todos modos, este resultado debe interpretarse como una asociación y no como causalidad, ya que tener estos atributos no garantiza por sí solo que un jugador alcance su potencial."""
        },
        {
            "title": "Que tan cerrados son los partidos?",
            "figure": grafico_06,
            "analysis_text": """En el gráfico de anillo se observa que la categoría más frecuente es la de partidos Cerrados, es decir, aquellos definidos por 1 gol de diferencia, con 9,598 partidos, equivalentes a aproximadamente 37.0% del total. Además, si se suman los Empates y los partidos Cerrados, se obtiene alrededor de 62.3% de todos los encuentros. Esto indica que la mayor parte de los partidos del dataset se mueve en márgenes pequeños y competitivos.

Por otro lado, los partidos Moderados, definidos por 2 goles de diferencia, representan cerca de 22.1%, mientras que los partidos Amplios, con 3 o más goles de diferencia, son los menos frecuentes con aproximadamente 15.6%. Esto sugiere que los resultados abultados existen, pero son claramente menos comunes que los partidos ajustados.

En conjunto, el gráfico respalda la idea de que la mayoría de los partidos suelen ser cerrados. Desde una perspectiva de análisis deportivo, esto sugiere que pequeñas diferencias de rendimiento, decisiones tácticas o momentos puntuales del juego pueden tener un impacto grande en el resultado final, porque los márgenes amplios no son la norma sino la excepción."""
        },
        {
            "title": "En que destacan las altas promesas?",
            "figure": grafico_07,
            "analysis_text": """El boxplot muestra que el grupo de Alta Promesa (Top 10%) presenta distribuciones más altas que el grupo de Resto de Jóvenes en los seis atributos evaluados. Esto se nota porque, en todos los casos, la mediana de las altas promesas queda por encima de la mediana del resto, lo que indica una ventaja consistente y no aislada en un solo atributo.

Las diferencias más marcadas aparecen en atributos como Visión, Control de Balón, Reacciones y Pase Corto. Esto sugiere que los jugadores jóvenes con mayor potencial no solo destacan por condiciones físicas, sino también por atributos técnicos y de lectura del juego. En Velocidad Sprint y Resistencia también se observa una ventaja para las altas promesas, aunque la separación entre grupos parece algo menor.

En conjunto, la gráfica sugiere que el potencial alto en jugadores jóvenes está asociado a un perfil más completo y balanceado. Es decir, las altas promesas no sobresalen solo en un atributo puntual, sino que tienden a mantener niveles superiores en varias dimensiones importantes del rendimiento."""
        },
        {
            "title": "A que edad rinden mejor los jugadores?",
            "figure": grafico_08,
            "analysis_text": """Al observar la curva de tendencia en este gráfico de líneas, podemos identificar con claridad las tres etapas biológicas y deportivas que definen la carrera de un futbolista profesional:

- Fase de crecimiento: desde las edades más tempranas (16-18 años), la línea muestra una pendiente ascendente constante y pronunciada. Es en esta etapa donde los jugadores adquieren madurez táctica, experiencia y desarrollo físico.
- El "prime" o pico de rendimiento: la curva alcanza su punto más alto y forma una "meseta" típica entre los 27 y los 31 años. Es en esta franja donde el jugador encuentra el balance perfecto: combina su máxima experiencia futbolística con un físico aún en óptimas condiciones.
- Fase de declive: a partir de los 32 años, la línea comienza un descenso evidente, reflejando la pérdida natural de capacidades físicas, como velocidad, explosividad o resistencia, que termina por afectar la valoración general.

Este gráfico dicta la lógica financiera y deportiva para armar una plantilla equilibrada. Si el equipo busca éxito inmediato para competir por un campeonato, debe apostar por jugadores en su "prime" (27-30 años), sabiendo que su costo será el más elevado. En cambio, si la directiva busca construir un proyecto a mediano plazo y generar plusvalía, la inversión debe ir hacia la fase de crecimiento (20-23 años), adquiriendo talento cuyo rendimiento y valor de mercado estadísticamente irán al alza."""
        },
        {
            "title": "Que formaciones equilibran uso y rendimiento?",
            "figure": grafico_09,
            "analysis_text": """El bubble plot sugiere que no todas las formaciones combinan del mismo modo frecuencia de uso y rendimiento. En la zona superior derecha, donde coinciden más puntos por partido y una diferencia de gol promedio menos negativa o incluso positiva, aparecen esquemas como 4-3-3, 4-4-2 y 4-2-3-1. Entre ellas, 4-2-3-1 destaca especialmente porque combina un rendimiento competitivo con una burbuja grande, es decir, con una muestra amplia de partidos, lo que hace más confiable la señal.

También aparecen algunas formaciones con buen desempeño, pero con menor respaldo de muestra, como 3-5-2 y otras variantes cercanas al bloque superior. Esto sugiere que pueden ser opciones interesantes, pero conviene ser más prudente al interpretarlas, ya que una menor frecuencia de uso hace más difícil separar un patrón estable de un resultado puntual.

En el extremo opuesto, 5-3-2, 4-5-1 y 4-1-4-1 se ubican en la zona de peor balance, con menos puntos por partido y una diferencia de gol promedio más negativa. En conjunto, la gráfica sugiere que no basta con mirar qué formación se usa más: conviene priorizar esquemas que mantengan un equilibrio entre frecuencia y resultados, y en ese sentido 4-2-3-1 y 4-4-2 parecen alternativas más sólidas que otras formaciones menos consistentes."""
        },
        {
            "title": "Que formaciones son mas seguras o mas riesgosas?",
            "figure": grafico_10,
            "analysis_text": """Al ver los resultados, se nota que no todas las formaciones se comportan igual en la cancha. Hay algunas que son más confiables: no siempre ganan, pero pierden poco y te mantienen compitiendo partido a partido, lo cual es clave en torneos largos. Otras son más arriesgadas: te pueden dar muchas victorias, pero también más derrotas, como si el equipo jugara al límite; estas pueden ser útiles cuando necesitas ir por todo, por ejemplo en partidos decisivos.

También están las formaciones más conservadoras, que tienden a empatar mucho: no arriesgan demasiado, pero tampoco marcan tanta diferencia. Para un entrenador, esto se traduce en elegir la formación no solo por estilo, sino por el momento: usar esquemas más sólidos cuando buscas regularidad y control, y formaciones más agresivas cuando necesitas ganar sí o sí, aunque implique asumir más riesgo."""
        }
    ]

    integrantes = [
        "Ossian Ramirez",
        "Estefania Elizabeth",
        "Ian Pascual",
        "Karim Jacob"
    ]

    crear_presentacion(
        output_path=output_path,
        analyses=analyses,
        integrantes=integrantes
    )