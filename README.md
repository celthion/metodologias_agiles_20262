# Corpus auditable de cánticos del fútbol profesional colombiano

**Proyecto aplicado · Universidad Nacional de Colombia · 2026-2**

El proyecto estudia los referentes, sentimientos y emociones en letras públicas de cánticos de fútbol colombiano. La primera entrega reúne evidencia trazable para que, en fases posteriores, se puedan comparar los resultados de modelos preentrenados por club, región y otras variables de contexto.

> [!NOTE]
> **Fase 1 · Entendimiento del negocio y carga de datos.** Entrega el **26 de noviembre de 2026**. Los archivos de adquisición corresponden al corte del **1 de septiembre de 2026**.

| Cánticos adquiridos | Clubes con textos | Texto documentado | Tablas verificadas |
| :---: | :---: | :---: | :---: |
| **600** | **17 de 20** | **33.077 palabras** | **8** |

## Equipo del proyecto

| Integrante | Cargo |
| --- | --- |
| David Cardona Duque | Líder del proyecto y científico de datos |
| Manuela Zapata Jiménez | Ingeniera de datos |
| Federico Viviescas Ramirez | Ingeniero en ML |

## Entregables de la fase 1

| Entregable | Qué encontrará el lector |
| --- | --- |
| [Marco del proyecto](docs/business_understanding/project_charter.md) | Problema, objetivos, alcance, resultados esperados, interesados y plan de cinco semanas. |
| [Diccionarios de datos](docs/data/data_dictionary.md) | Campos, tipos, valores, procedencia y reglas de las tablas de adquisición y control. |
| [Notebook ejecutado](scripts/data_acquisition/carga_de_datos.ipynb) | Ejecución de la carga y lectura de los resultados de procedencia, cobertura y calidad. |
| [Código de carga](scripts/data_acquisition/main.py) | Validación de los CSV incluidos, sus huellas, esquema, llaves y cobertura. |
| [Definición y trazabilidad de los datos](docs/data/data_definition.md) | Origen, versión, formatos, rutas y evidencia de ejecución. |

## Reproducir la carga

Los ocho CSV de entrada están incluidos en [`data/source/`](data/source/). La carga usa la biblioteca estándar de Python y se puede ejecutar sin conexión. Desde la raíz del repositorio, con **Python 3.11 o superior**:

```bash
python3 scripts/data_acquisition/main.py
```

El cargador escribe las copias de trabajo en `data/raw/` y el resultado de la validación en `data/carga_fase1.json`. Ambas salidas se regeneran localmente.

Para instalar las dependencias desde PyPI y abrir el notebook con Poetry:

```bash
poetry install
poetry run jupyter lab scripts/data_acquisition/carga_de_datos.ipynb
```

<details>
<summary>Cargar desde una copia alternativa</summary>

Indique el directorio que contiene los ocho CSV de la versión documentada. El cargador aplica las mismas comprobaciones de integridad.

```bash
python3 scripts/data_acquisition/main.py --origen-local /ruta/al/directorio/datos
```

Puede cambiar la carpeta de salida con `--destino`. Las huellas y cabeceras esperadas están en el [manifiesto de adquisición](scripts/data_acquisition/manifest.json).

</details>

## Ruta del proyecto

| Entrega | Fase | Hito de revisión |
| :--- | :--- | :--- |
| **26 nov.** | **Entendimiento del negocio y carga de datos** | Marco, diccionarios y carga verificable. |
| **3 dic.** | Preprocesamiento y análisis exploratorio | Corpus preparado y análisis de su cobertura y estructura. |
| **10 dic.** | Modelamiento y extracción de características | Características, entidades y caracterización afectiva por cántico. |
| **17 dic.** | Despliegue | Flujo reproducible y guía de ejecución. |
| **24 dic.** | Evaluación y entrega final | Evidencia de funcionamiento, resultados y limitaciones. |

El alcance y los criterios de cierre de cada semana se detallan en el [marco del proyecto](docs/business_understanding/project_charter.md).
