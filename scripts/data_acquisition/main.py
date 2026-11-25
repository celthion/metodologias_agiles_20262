"""Carga la versión de adquisición del corpus y verifica su contrato de datos."""

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from datetime import date
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit


MANIFIESTO = Path(__file__).with_name("manifest.json")
RAIZ_REPOSITORIO = Path(__file__).resolve().parents[2]
DESTINO_PREDETERMINADO = RAIZ_REPOSITORIO / "data"


def sha256(contenido: bytes) -> str:
    return hashlib.sha256(contenido).hexdigest()


def cargar_archivo(ruta: Path, ficha: dict) -> bytes:
    """Lee un CSV local y verifica su integridad antes de interpretarlo."""
    if not ruta.is_file():
        raise ValueError(f"Falta el archivo de origen {ruta}.")
    with ruta.open("rb") as archivo:
        contenido = archivo.read(ficha["bytes"] + 1)
    if len(contenido) != ficha["bytes"]:
        raise ValueError(f"Tamaño incorrecto para {ruta.name}. Se esperaban {ficha['bytes']} bytes.")
    huella = sha256(contenido)
    if huella != ficha["sha256"]:
        raise ValueError(
            f"SHA-256 no coincide para {ruta.name}. "
            f"Esperado: {ficha['sha256']}. Obtenido: {huella}."
        )
    return contenido


def leer_tabla(contenido, nombre, ficha):
    """Lee campos multilínea y exige el esquema y las filas del corte publicado."""
    entrada = StringIO(contenido.decode("utf-8-sig"), newline="")
    lector = csv.DictReader(entrada, strict=True)
    if lector.fieldnames != ficha["columnas"]:
        raise ValueError(f"Cabecera inesperada en {nombre}: {lector.fieldnames}")
    filas = list(lector)
    if len(filas) != ficha["filas"]:
        raise ValueError(f"{nombre}: se esperaban {ficha['filas']} filas y se leyeron {len(filas)}.")
    if any(None in fila or None in fila.values() for fila in filas):
        raise ValueError(f"Hay filas con más o menos campos que la cabecera en {nombre}.")
    return filas


def clave_unica(filas, campo, nombre):
    valores = {fila[campo] for fila in filas}
    if len(valores) != len(filas) or any(not valor.strip() for valor in valores):
        raise ValueError(f"{nombre}.{campo} tiene claves vacías o repetidas.")
    return valores


def validar_corpus(tablas, fecha_corte):
    canticos = tablas["canticos.csv"]
    clubes = tablas["clubes.csv"]
    cobertura = tablas["control_cobertura.csv"]

    clave_unica(canticos, "cantico_id", "canticos")
    clave_unica(canticos, "url", "canticos")
    clave_unica(tablas["bibliografia_apa7.csv"], "ref_id", "bibliografia_apa7")
    clave_unica(tablas["decisiones_revision_fase2.csv"], "revision_id", "decisiones_revision_fase2")
    ids_clubes = clave_unica(clubes, "club_id", "clubes")
    ids_cobertura = clave_unica(cobertura, "club_id", "control_cobertura")
    conteo_por_club = Counter(fila["club_id"] for fila in canticos)
    if ids_cobertura != ids_clubes or set(conteo_por_club) - ids_clubes:
        raise ValueError("Las claves de club no concilian entre cánticos, clubes y cobertura.")
    if any(int(fila["registros_finales"]) != conteo_por_club[fila["club_id"]] for fila in cobertura):
        raise ValueError("Los conteos de control_cobertura.csv no coinciden con el corpus por club.")

    palabras = []
    for cantico in canticos:
        identificador = cantico["cantico_id"]
        for campo in ("letra_original", "fuente", "metodo_adquisicion"):
            if not cantico[campo].strip():
                raise ValueError(f"{campo} vacío en {identificador}.")
        url = urlsplit(cantico["url"])
        if url.scheme not in ("http", "https") or not url.hostname:
            raise ValueError(f"URL de procedencia inválida en {identificador}.")
        if date.fromisoformat(cantico["fecha_consulta"]).isoformat() != fecha_corte:
            raise ValueError(f"Fecha de consulta fuera del corte en {identificador}.")
        numero_palabras = int(cantico["numero_palabras"])
        if numero_palabras <= 0:
            raise ValueError(f"Conteo de palabras no positivo en {identificador}.")
        palabras.append(numero_palabras)

    return {
        "canticos": len(canticos),
        "clubes_referencia": len(clubes),
        "clubes_con_textos": len(conteo_por_club),
        "clubes_sin_textos_localizados": [
            fila["nombre_corto"] for fila in clubes if fila["club_id"] not in conteo_por_club
        ],
        "palabras": sum(palabras),
        "duplicados_exactos_documentados": len(tablas["duplicados_exactos.csv"]),
        "canticos_por_fuente": dict(Counter(fila["fuente"] for fila in canticos).most_common()),
        "estados_verificacion": dict(Counter(fila["estado_verificacion"] for fila in canticos).most_common()),
    }


def escritura_atomica(ruta, contenido):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=ruta.parent, prefix=".carga-") as temporal:
        archivo = Path(temporal) / ruta.name
        archivo.write_bytes(contenido)
        archivo.replace(ruta)


def cargar_corpus(destino: Path, origen_local: Path | None = None) -> dict:
    manifiesto = json.loads(MANIFIESTO.read_text(encoding="utf-8"))
    origen_repositorio = Path(manifiesto["origen"])
    directorio_origen = origen_local if origen_local is not None else RAIZ_REPOSITORIO / origen_repositorio
    recibo = {"version": manifiesto["version"], "fecha_corte": manifiesto["fecha_corte"], "archivos": {}}
    tablas = {}
    insumos = {}

    for nombre, ficha in manifiesto["archivos"].items():
        contenido = cargar_archivo(directorio_origen / nombre, ficha)
        tablas[nombre] = leer_tabla(contenido, nombre, ficha)
        insumos[nombre] = contenido
        recibo["archivos"][nombre] = {
            "origen": (origen_repositorio / nombre).as_posix() if origen_local is None else nombre,
            "sha256": ficha["sha256"],
            "filas": len(tablas[nombre]),
            "columnas": len(ficha["columnas"]),
            "modo": "incluido en el repositorio" if origen_local is None else "origen local",
        }

    recibo["controles"] = validar_corpus(tablas, manifiesto["fecha_corte"])
    for nombre, contenido in insumos.items():
        escritura_atomica(destino / "raw" / nombre, contenido)
    escritura_atomica(
        destino / "carga_fase1.json", (json.dumps(recibo, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )
    return recibo


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--origen-local", type=Path, metavar="DIRECTORIO",
        help="Usa una copia alternativa de los ocho CSV en lugar de data/source/.",
    )
    parser.add_argument(
        "--destino", type=Path, default=DESTINO_PREDETERMINADO, metavar="DIRECTORIO",
        help="Directorio de salida. Por defecto, data/ dentro del repositorio.",
    )
    args = parser.parse_args()
    try:
        recibo = cargar_corpus(args.destino, args.origen_local)
    except (OSError, ValueError, csv.Error) as error:
        print(f"Error de carga: {error}", file=sys.stderr)
        return 1

    for nombre, archivo in recibo["archivos"].items():
        print(f"{nombre}: {archivo['filas']} filas × {archivo['columnas']} columnas ({archivo['modo']})")
    controles = recibo["controles"]
    print(f"Corpus verificado: {controles['canticos']} cánticos de {controles['clubes_con_textos']} clubes.")
    fuentes = ", ".join(f"{fuente} ({cantidad})" for fuente, cantidad in controles["canticos_por_fuente"].items())
    print(f"Distribución por fuente: {fuentes}.")
    print(f"Recibo: {args.destino / 'carga_fase1.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
