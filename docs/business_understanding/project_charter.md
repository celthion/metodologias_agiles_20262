# Project Charter - Entendimiento del Negocio

[Objetivo](#objetivo-del-proyecto) · [Alcance](#alcance-del-proyecto) · [Metodología](#metodología) · [Cronograma](#cronograma) · [Equipo](#equipo-del-proyecto) · [Presupuesto](#presupuesto) · [Stakeholders](#stakeholders) · [Aprobaciones](#aprobaciones)

## Nombre del Proyecto

**Corpus auditable de cánticos del fútbol profesional colombiano**

> [!NOTE]
> La primera entrega delimita el problema y verifica la carga de **600 registros de 17 clubes**. La curaduría de fuentes y la revisión de similitud determinarán el tamaño del corpus analítico.

## Objetivo del Proyecto

Aplicar modelos preentrenados para caracterizar los referentes y el contenido afectivo de los cánticos recopilados, y relacionar descriptivamente esas salidas con el contexto de los clubes representados.

### Problema y decisión

Las letras públicas de los cánticos del fútbol colombiano están dispersas en sitios con formatos y coberturas desiguales. Los apodos, la jerga y las referencias territoriales también dificultan comparar repertorios a partir de ejemplos aislados. Para los textos recopilados hace falta una caracterización que permita seguir cada resultado hasta la letra, conocer los tipos de referentes mencionados y examinar los perfiles afectivos que asignan los modelos. El uso de cánticos en la construcción de pertenencia y memoria colectiva motiva esta lectura. [Knijnik (2018)](https://doi.org/10.1177/1012690216665356)

**Pregunta de trabajo.** ¿Qué entidades o referentes aparecen con mayor frecuencia, qué sentimientos y emociones asignan los modelos preentrenados y cómo se distribuyen ambos resultados por club, región y otras variables disponibles?

**Decisión que apoya el proyecto.** Al cerrar el análisis, el equipo seleccionará qué patrones comunicar y con qué nivel de detalle. La decisión se basará en el número de textos o menciones que respalda cada cruce, la concentración por fuente y la capacidad de rastrear las salidas hasta el texto original. El lector podrá valorar si el soporte alcanza para comparar grupos dentro del corpus.

### Objetivos específicos

1. Validar los 600 registros de adquisición y documentar cada decisión de curaduría y de auditoría de similitud. Conciliar los conteos de entrada, exclusiones y salida en cada paso.
2. Preparar `texto_modelo` para inferencia y conservar `letra_original` como evidencia.
3. Extraer entidades nombradas y organizar las menciones en categorías semánticas comparables.
4. Seleccionar y aplicar un recurso preentrenado que produzca etiquetas y puntuaciones afectivas más informativas que una polaridad básica.
5. Integrar las salidas con el contexto de los clubes mediante `club_id`. Calcular frecuencias o proporciones y comunicar los patrones que tengan soporte explícito.

## Alcance del Proyecto

### Incluye

- **Datos disponibles.** La unidad de análisis es una letra pública transcrita y asociada de forma verificable a un club. La búsqueda se cerró el **1 de septiembre de 2026**. El universo de referencia comprende los **20 clubes de la Liga BetPlay A 2026**. La cobertura observada fue de **17/20**. Para Águilas Doradas, Fortaleza CEIF y Llaneros FC no se localizaron letras que cumplieran los criterios de inclusión en ese corte. [Reglamento de DIMAYOR](https://dimayor.com.co/wp-content/uploads/2026/01/REGLAMENTO-LIGA-2026-V11-1.pdf) · [Definición de los datos](../data/data_definition.md)

- **Procedencia y contexto.** Barrabrava.net aporta 388 letras, FanChants 176, Attake Massivo Pasto & La Banda Tricolor 18 y Fortaleza Leoparda (4mg) 18. Las capturas registran el origen y la fecha de consulta. La tabla de adquisición marca los casos que requieren revisión. En las fases siguientes se usará `club_id` para vincular las salidas con región, ciudad, desempeño, asistencia, seguidores y otros campos disponibles. [Código de carga](../../scripts/data_acquisition/main.py) · [Diccionario de datos](../data/data_dictionary.md)

- **Resultados esperados.** Un corpus analítico con decisiones de calidad trazables, una salida por texto con entidades, categorías de referentes, etiquetas afectivas y puntuaciones, y un informe con tablas o gráficos por club, región y variables contextuales seleccionadas.

#### Criterios de éxito

| Criterio | Indicador | Evidencia o meta |
| --- | --- | --- |
| Carga utilizable | Registros válidos / registros de adquisición esperados | **600/600** en la carga inicial, con controles de integridad, identificadores únicos y texto de origen presente. |
| Cobertura comunicada | Clubes con textos / clubes del universo | **17/20** en el corte observado. El reporte identifica los tres clubes sin textos localizados. |
| Procesamiento de las dos tareas | Textos enviados a cada tarea / textos del corpus analítico resultante | **100 %** en cada tarea. Se reportarán por separado las ejecuciones válidas y fallidas. |
| Trazabilidad e integración | Salidas con IDs y versión del recurso / salidas generadas. Filas enlazadas con `clubes.csv` / filas a integrar | **100 %** en ambos controles. Se conservan `cantico_id`, `club_id` y el recurso preentrenado usado. |
| Salidas utilizables | Ejecuciones válidas con los campos de resultado / ejecuciones válidas de cada tarea | **100 %**. Se distingue entre una lista de menciones vacía y un error de procesamiento. |
| Lectura descriptiva | Cruces publicados con denominador, soporte y alcance / cruces publicados | **100 %**. Mostrar resultados por club y región cuando el soporte permita interpretarlos. |

> [!IMPORTANT]
> Las metas de procesamiento miden cobertura e integridad del flujo. La ausencia de etiquetas de referencia impide estimar la exactitud de los modelos en este corpus.

### Excluye

- Audio y video sin transcripción pública, comentarios privados y datos individuales.
- Entrenamiento propio, ajuste fino, anotación de referencia de entidades o afecto y evaluación humana de predicciones. La revisión de fuentes sí se realiza como control de calidad de los datos.
- Inferencia causal, atribución de estados psicológicos a quienes cantan y generalización a repertorios o hinchadas completas.

## Metodología

Se adopta **Team Data Science Process** para organizar las entregas, con un criterio de cierre verificable por semana. La estructura del marco, la documentación de los insumos y la comprobación inicial de la carga siguen los ejemplos del caso de estudio de MindLab. [Ciclo de vida de TDSP](https://learn.microsoft.com/en-us/azure/architecture/data-science-process/lifecycle) · [Caso de estudio MLDS6](https://github.com/mindlab-unal/mlds6-case-study/tree/09574fa2f892919cd2fe73080c7648f1dfd296e1)

La fase de carga verifica el corpus de letras públicas con su procedencia. La preparación conservará la letra de origen, aplicará decisiones de curaduría sobre una copia de trabajo y generará el texto de inferencia. La selección de recursos preentrenados considerará el español, la jerga, la granularidad de las salidas y la capacidad de cómputo. Los recursos y las categorías afectivas se definirán en la fase de modelamiento. El despliegue previsto es un flujo reproducible en el entorno del proyecto y la evaluación se centra en la cobertura, la trazabilidad y la lectura de resultados.

```mermaid
flowchart LR
    A["600 registros de adquisición"] -->|"Curaduría de fuentes"| B["Corpus con decisiones de revisión"]
    B -->|"Auditoría de similitud"| C["Corpus analítico con exclusiones trazables"]
    C --> D["Referentes y afecto por texto"]
    D --> E["Cruces con el contexto de los clubes"]
```

### Riesgos y controles

| Condición | Efecto y respuesta |
| --- | --- |
| Disponibilidad desigual de letras por club y fuente | Barrabrava.net aporta el 64,7 % de la adquisición. Mostrar soporte por grupo e interpretar las comparaciones en función de la composición observada. |
| Ambigüedad de apodos, metáforas y jerga barrista | Registrar etiqueta, puntuación y fragmento cuando corresponda. Tratar las salidas como estimaciones exploratorias del recurso seleccionado. |
| Cambios en las páginas y errores de integración | Usar la versión fijada de los insumos y verificar huellas e identificadores. Registrar cualquier corrección sobre una copia analítica. |
| Cómputo y compatibilidad de modelos | Verificar idioma, requisitos de ejecución y formato de salida antes de adoptar un recurso. Ajustar el ritmo de procesamiento a la capacidad disponible. |

## Cronograma

| Etapa | Duración estimada | Fechas de 2026 | Entregable y criterio de cierre |
| --- | --- | --- | --- |
| 1. Entendimiento del negocio y carga de datos | 1 semana | 20–26 de noviembre | Acta, definición y diccionario de datos. Carga reproducible del corte con procedencia, integridad y cobertura documentadas. |
| 2. Preprocesamiento y análisis exploratorio | 1 semana | 27 de noviembre–3 de diciembre | Corpus preparado y reporte exploratorio. Decisiones de curaduría aplicadas con conteos de entrada y salida, texto original preservado y perfiles por fuente y club. |
| 3. Modelamiento y extracción de características | 1 semana | 4–10 de diciembre | Selección documentada de recursos preentrenados, auditoría de similitudes y primeras salidas de referentes y afecto. Se registrarán las versiones, el tamaño analítico y los errores. |
| 4. Despliegue | 1 semana | 11–17 de diciembre | Flujo ejecutable en el entorno del proyecto e instrucciones de reproducción. Una ejecución de extremo a extremo generará resultados trazables por texto. |
| 5. Evaluación y entrega final | 1 semana | 18–24 de diciembre | Informe, tablas o gráficos y evidencia de evaluación técnica. Se revisarán la cobertura, los denominadores, los límites de interpretación y la documentación de cierre. |

Las fechas de inicio y cierre están incluidas. Las fases 2 a 5 corresponden al trabajo previsto para después de esta entrega.

## Equipo del Proyecto

| Integrante | Cargo | Responsabilidad |
| --- | --- | --- |
| David Cardona Duque | Líder del proyecto y científico de datos | Coordinar las entregas, definir los criterios de análisis e interpretar los resultados. |
| Manuela Zapata Jiménez | Ingeniera de datos | Mantener los insumos, la carga y los controles de calidad y trazabilidad. |
| Federico Viviescas Ramirez | Ingeniero en ML | Integrar los modelos preentrenados, preparar la ejecución reproducible y verificar las salidas. |

## Presupuesto

El presupuesto estimado de las **cinco semanas es de COP 8.987.000**. Valora 110 horas de dedicación académica del equipo e incluye capacidad de cómputo para inferencia, almacenamiento y una reserva del 10 %. Las tarifas unitarias son valores de planeación en pesos colombianos. [Estructura presupuestal del caso de estudio](https://github.com/mindlab-unal/mlds6-case-study/blob/09574fa2f892919cd2fe73080c7648f1dfd296e1/docs/business_understanding/project_charter.md#presupuesto)

| Categoría de gasto | Descripción | Base de cálculo | Costo estimado (COP) |
| --- | --- | --- | ---: |
| **I. Personal** | | | |
| Ciencia de datos | Diseño del análisis, comparación de recursos preentrenados e interpretación de resultados. | 32 h × 80.000 | 2.560.000 |
| Ingeniería de datos | Carga, curaduría, análisis exploratorio y control de calidad del corpus. | 32 h × 65.000 | 2.080.000 |
| Ingeniería en ML | Integración de modelos, ejecución de inferencias y despliegue reproducible. | 32 h × 75.000 | 2.400.000 |
| **Subtotal de personal** | | **96 h** | **7.040.000** |
| **II. Infraestructura y software** | | | |
| Cómputo para inferencia | Capacidad complementaria para probar y ejecutar los recursos preentrenados. | 12 h × 7.500 | 90.000 |
| Almacenamiento | Respaldo del corpus, resultados y artefactos de ejecución. | 5 GB × 2 meses × 1.000 por GB-mes | 10.000 |
| Licencias | Python, Jupyter y librerías de código abierto. | Herramientas de libre uso | 0 |
| **Subtotal de infraestructura y software** | | | **100.000** |
| **III. Coordinación y entrega** | | | |
| Gestión del proyecto | Revisión de los hitos, coordinación del equipo y seguimiento de las entregas. | 8 h × 80.000 | 640.000 |
| Documentación y verificación final | Revisión del repositorio, comprobación de la guía de reproducción y preparación de la entrega. | 6 h × 65.000 | 390.000 |
| **Subtotal de coordinación y entrega** | | **14 h** | **1.030.000** |
| **Subtotal del proyecto** | | **110 h de dedicación** | **8.170.000** |
| Contingencia | Reserva para reprocesamiento, ajustes de integración o mayor consumo de cómputo. | 10 % × 8.170.000 | 817.000 |
| **Total estimado del proyecto** | | | **8.987.000** |

<details>
<summary>Distribución de las 110 horas por fase</summary>

| Fase | David | Manuela | Federico | Total |
| --- | ---: | ---: | ---: | ---: |
| Entendimiento del negocio y carga de datos | 7 | 11 | 3 | 21 |
| Preprocesamiento y análisis exploratorio | 9 | 12 | 5 | 26 |
| Modelamiento y extracción de características | 12 | 5 | 12 | 29 |
| Despliegue | 5 | 4 | 9 | 18 |
| Evaluación y entrega final | 7 | 6 | 3 | 16 |
| **Total de horas** | **40** | **38** | **32** | **110** |

Las 40 horas de David incluyen 8 de coordinación. Las 38 horas de Manuela incluyen 6 de documentación y verificación final. El costo de cada actividad se registra una vez en el presupuesto.

</details>

## Stakeholders

| Grupo | Relación con el proyecto | Necesidad o expectativa |
| --- | --- | --- |
| Equipo de la materia | Consolida datos, ejecuta el flujo y documenta las decisiones. | Poder reproducir los resultados y rastrear las exclusiones, asociaciones y cambios. |
| Docencia y evaluación académica | Revisa el alcance y los entregables previstos. | Encontrar evidencias verificables y una interpretación coherente con los límites del estudio. |
| Investigadores y estudiantes de PLN, cultura y deporte | Lectores potenciales del corpus y del análisis. | Consultar resultados por referente y perfil afectivo con soporte y procedencia visibles. |
| Clubes, colectivos de hinchas, iniciativas de memoria y organizaciones deportivas, culturales o de convivencia | Beneficiarios potenciales de la lectura del material público. | Explorar expresiones recurrentes de pertenencia, territorio y rivalidad en los repertorios recopilados. |

## Aprobaciones

**Visto bueno interno para la entrega académica.** David Cardona Duque, líder del proyecto, aprobó el marco el **24 de noviembre de 2026**.

## Fuentes

- División Mayor del Fútbol Colombiano. (2026). *Reglamento Liga BetPlay DIMAYOR 2026*. [Documento oficial](https://dimayor.com.co/wp-content/uploads/2026/01/REGLAMENTO-LIGA-2026-V11-1.pdf)
- Knijnik, J. (2018). Imagining a multicultural community in an everyday football carnival: Chants, identity and social resistance on Western Sydney terraces. *International Review for the Sociology of Sport, 53*(4), 471–489. [https://doi.org/10.1177/1012690216665356](https://doi.org/10.1177/1012690216665356)
- Microsoft. (s. f.). *Team Data Science Process lifecycle*. [Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/data-science-process/lifecycle)
- MindLab UNAL. (2025). *MLDS6 case study* [Repositorio de GitHub]. [Versión consultada](https://github.com/mindlab-unal/mlds6-case-study/tree/09574fa2f892919cd2fe73080c7648f1dfd296e1)
