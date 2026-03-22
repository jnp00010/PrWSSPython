"""
Script para poblar ontología RDF Formula 1 desde CSV con RDFlib.
Carga la ontología base, lee datos de CSV y genera individuos con relaciones.
"""

import csv
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD

ONT = Namespace("http://www.semanticweb.org/usuario/ontologies/2026/2/untitled-ontology-2#")
DATA_DIR = Path("data")


def leer_csv(nombre_archivo: str):
    """Lee un fichero CSV del directorio data/ y retorna lista de diccionarios."""
    ruta = DATA_DIR / nombre_archivo
    with open(ruta, newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def add_texto(grafo: Graph, sujeto, predicado, valor: str):
    """Añade un literal de texto al grafo RDF si el valor no está vacío."""
    if valor:
        grafo.add((sujeto, predicado, Literal(valor.strip())))


def add_entero(grafo: Graph, sujeto, predicado, valor: str):
    """Añade un literal entero al grafo RDF si el valor es válido."""
    if valor and valor.strip().isdigit():
        grafo.add((sujeto, predicado, Literal(int(valor), datatype=XSD.int)))


def add_datetime(grafo: Graph, sujeto, predicado, valor: str):
    """Añade un literal de fecha/hora al grafo RDF si el valor es válido."""
    if valor:
        valor = valor.strip()
        try:
            from datetime import datetime
            datetime.fromisoformat(valor)
            grafo.add((sujeto, predicado, Literal(valor, datatype=XSD.dateTime)))
        except ValueError:
            pass


def es_clase_o_propiedad(sujeto, grafo: Graph) -> bool:
    """Determina si un recurso RDF es clase u propiedad (no un individuo)."""
    tipos = set(grafo.objects(sujeto, RDF.type))
    clases_propiedades = {OWL.Class, OWL.DatatypeProperty, OWL.ObjectProperty}
    return any(t in clases_propiedades for t in tipos)


def poblar_temporadas(grafo: Graph):
    """Puebla individuos Temporada desde temporadas.csv con su año."""
    for row in leer_csv("temporadas.csv"):
        temporada = ONT[row["id"].strip()]
        grafo.add((temporada, RDF.type, ONT.Temporada))
        add_entero(grafo, temporada, ONT.AñoTemporada, row.get("año", ""))


def poblar_equipos(grafo: Graph):
    """Puebla individuos Equipo desde equipos.csv y vincula con temporadas."""
    for row in leer_csv("equipos.csv"):
        equipo = ONT[row["id"].strip()]
        grafo.add((equipo, RDF.type, ONT.Equipo))
        add_texto(grafo, equipo, ONT.NombreEquipo, row.get("nombre", ""))

        temporada_id = (row.get("temporada_id") or "").strip()
        if temporada_id:
            temporada = ONT[temporada_id]
            grafo.add((equipo, ONT.compiteEn, temporada))


def poblar_motores(grafo: Graph):
    """Puebla individuos Motor desde motores.csv con nombre y fabricante."""
    for row in leer_csv("motores.csv"):
        motor = ONT[row["id"].strip()]
        grafo.add((motor, RDF.type, ONT.Motor))
        add_texto(grafo, motor, ONT.NombreMotor, row.get("nombre", ""))
        add_texto(grafo, motor, ONT.Fabricante, row.get("fabricante", ""))


def poblar_coches(grafo: Graph):
    """Puebla individuos Coche desde coches.csv y vincula con equipos y motores."""
    for row in leer_csv("coches.csv"):
        coche = ONT[row["id"].strip()]
        grafo.add((coche, RDF.type, ONT.Coche))
        add_texto(grafo, coche, ONT.NombreCoche, row.get("nombre", ""))

        equipo_id = (row.get("equipo_id") or "").strip()
        if equipo_id:
            equipo = ONT[equipo_id]
            grafo.add((coche, ONT.esConstruidoPor, equipo))
            grafo.add((equipo, ONT.construye, coche))

        motor_id = (row.get("motor_id") or "").strip()
        if motor_id:
            motor = ONT[motor_id]
            grafo.add((coche, ONT.utilizaMotor, motor))
            grafo.add((motor, ONT.esUtilizadoPor, coche))


def poblar_circuitos(grafo: Graph):
    """Puebla individuos Circuito desde circuitos.csv con su nombre."""
    for row in leer_csv("circuitos.csv"):
        circuito = ONT[row["id"].strip()]
        grafo.add((circuito, RDF.type, ONT.Circuito))
        add_texto(grafo, circuito, ONT.NombreCircuito, row.get("nombre", ""))


def poblar_pilotos(grafo: Graph):
    """Puebla individuos Piloto desde pilotos.csv y vincula con equipos."""
    for row in leer_csv("pilotos.csv"):
        piloto = ONT[row["id"].strip()]
        grafo.add((piloto, RDF.type, ONT.Piloto))
        add_texto(grafo, piloto, ONT.NombrePersona, row.get("nombre", ""))
        add_texto(grafo, piloto, ONT.Nacionalidad, row.get("nacionalidad", ""))

        equipo_id = (row.get("equipo_id") or "").strip()
        if equipo_id:
            equipo = ONT[equipo_id]
            grafo.add((piloto, ONT.esPilotoDe, equipo))
            grafo.add((equipo, ONT.tienePiloto, piloto))


def poblar_directores(grafo: Graph):
    """Puebla individuos DirectorDeEquipo desde directores.csv y vincula con equipos."""
    for row in leer_csv("directores.csv"):
        director = ONT[row["id"].strip()]
        grafo.add((director, RDF.type, ONT.DirectorDeEquipo))
        add_texto(grafo, director, ONT.NombrePersona, row.get("nombre", ""))
        add_texto(grafo, director, ONT.Nacionalidad, row.get("nacionalidad", ""))

        equipo_id = (row.get("equipo_id") or "").strip()
        if equipo_id:
            equipo = ONT[equipo_id]
            grafo.add((director, ONT.esDirectorDe, equipo))
            grafo.add((equipo, ONT.tieneDirector, director))


def poblar_carreras(grafo: Graph):
    """Puebla individuos Carrera desde carreras.csv y vincula con temporadas y circuitos."""
    for row in leer_csv("carreras.csv"):
        carrera = ONT[row["id"].strip()]
        grafo.add((carrera, RDF.type, ONT.Carrera))
        add_texto(grafo, carrera, ONT.NombreCarrera, row.get("nombre", ""))
        add_datetime(grafo, carrera, ONT.Fecha, row.get("fecha", ""))
        add_entero(grafo, carrera, ONT.NVueltas, row.get("nvueltas", ""))

        temporada_id = (row.get("temporada_id") or "").strip()
        if temporada_id:
            temporada = ONT[temporada_id]
            grafo.add((carrera, ONT.perteneceATemporada, temporada))
            grafo.add((temporada, ONT.tieneCarrera, carrera))

        circuito_id = (row.get("circuito_id") or "").strip()
        if circuito_id:
            circuito = ONT[circuito_id]
            grafo.add((carrera, ONT.seCelebraEn, circuito))
            grafo.add((circuito, ONT.albergaCarrera, carrera))


def poblar_campeones_pilotos(grafo: Graph):
    """Puebla individuos CampeonPilotos desde campeones_pilotos.csv y vincula con pilotos."""
    for row in leer_csv("campeones_pilotos.csv"):
        campeonato = ONT[row["id"].strip()]
        piloto = ONT[row["piloto_id"].strip()]
        temporada = ONT[row["temporada_id"].strip()]
        grafo.add((campeonato, RDF.type, ONT.CampeonPilotos))
        add_entero(grafo, campeonato, ONT.AñoCampeonato, row.get("año", ""))
        grafo.add((campeonato, ONT.esGanadoPorPiloto, piloto))
        grafo.add((piloto, ONT.ganaCampeonatoPilotos, campeonato))
        grafo.add((temporada, ONT.tieneCampeonato, campeonato))


def poblar_campeones_constructores(grafo: Graph):
    """Puebla individuos CampeonConstructores desde campeones_constructores.csv y vincula con equipos."""
    for row in leer_csv("campeones_constructores.csv"):
        campeonato = ONT[row["id"].strip()]
        equipo = ONT[row["equipo_id"].strip()]
        temporada = ONT[row["temporada_id"].strip()]
        grafo.add((campeonato, RDF.type, ONT.CampeonConstructores))
        add_entero(grafo, campeonato, ONT.AñoCampeonato, row.get("año", ""))
        grafo.add((campeonato, ONT.esGanadoPorEquipo, equipo))
        grafo.add((equipo, ONT.ganaCampeonatoConstructores, campeonato))
        grafo.add((temporada, ONT.tieneCampeonato, campeonato))


def main():
    """Carga ontología base y puebla individuos desde CSV."""
    grafo = Graph()
    grafo.parse("Prueba.rdf")
    grafo.bind("ont", ONT)


    poblar_temporadas(grafo)
    poblar_equipos(grafo)
    poblar_motores(grafo)
    poblar_coches(grafo)
    poblar_circuitos(grafo)
    poblar_pilotos(grafo)
    poblar_directores(grafo)
    poblar_carreras(grafo)
    poblar_campeones_pilotos(grafo)
    poblar_campeones_constructores(grafo)

    grafo.serialize("nueva_ontologia.rdf", format="xml")
    print("OK: nueva_ontologia.rdf creada con estructura de Prueba.rdf y individuos de CSV.")


if __name__ == "__main__":
    main()
