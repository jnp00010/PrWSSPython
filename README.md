# Población de Ontología Formula 1 con RDFlib

## Introducción y Objetivo

En esta práctica he implementado una solución para poblar una ontología RDF sobre la Fórmula 1.
El objetivo es con ficheros CSV crear individuos de la ontologia Prueba.rdf.

He utilizado Python 3 con la librería **RDFlib**, que proporciona herramientas para manipular grafos RDF.
## Metodología

### Diseño del proceso

El script `script.py` hace lo siguiente:

1. Se carga la ontología base desde `Prueba.rdf`, que ya contiene la estructura de clases, propiedades y restricciones.
2. Se iteran los ficheros CSV del directorio `data/`, leyendo cada fila como un nuevo individuo.
3. Para cada individuo, se crean los RDF correspondientes (tipo de clase, propiedades de datos) y se establecen las relaciones con otros individuos según los CSV referenciados.
4. Por ultimo, se crea `ontologia_poblada.rdf` en formato RDF/XML.

### Entidades pobladas

El script genera instancias de las siguientes diez clases concretas:

- **Temporada**: representan cada año de competición.
- **Equipo**: equipos constructores de monoplazas.
- **Motor**: motores fabricados por constructores.
- **Coche**: monoplazas concretos asociados a equipos.
- **Circuito**: pistas donde se celebran las carreras.
- **Piloto**: pilotos de carreras activos en una temporada.
- **DirectorDeEquipo**: directores técnicos o ejecutivos de los equipos.
- **Carrera**: eventos de carrera dentro de una temporada.
- **CampeonPilotos**: campeones de pilotos en un año determinado.
- **CampeonConstructores**: campeones de constructores en un año.

Las clases abstractas `Persona` y `Campeon` no se crean directamente, sino que quedan representadas mediante sus subclases concretas.


## Estructura de Datos y CSV

### Descripción de los ficheros CSV

Los ficheros CSV en el directorio `data/` contienen los datos que se transforman en indiviuos de la ontología.
Cada CSV corresponde a una clase y sus columnas definen tanto propiedades de datos como referencias a otras entidades:

- **temporadas.csv**: años de competición (`id`, `año`).
- **equipos.csv**: equipos pertenecientes a una temporada (`id`, `nombre`, `temporada_id`).
- **motores.csv**: motores disponibles (`id`, `nombre`, `fabricante`).
- **coches.csv**: monoplazas usando motor de un equipo (`id`, `nombre`, `equipo_id`, `motor_id`).
- **circuitos.csv**: pistas de carrera (`id`, `nombre`).
- **pilotos.csv**: pilotos adscritos a equipos (`id`, `nombre`, `nacionalidad`, `equipo_id`).
- **directores.csv**: directores técnicos de equipos (`id`, `nombre`, `nacionalidad`, `equipo_id`).
- **carreras.csv**: eventos de carrera con fecha en formato ISO 8601 (`id`, `nombre`, `fecha`, `nvueltas`, `temporada_id`, `circuito_id`).
- **campeones_pilotos.csv**: campeones de pilotos por año (`id`, `año`, `piloto_id`).
- **campeones_constructores.csv**: campeones de constructores por año (`id`, `año`, `equipo_id`).

### Relaciones entre entidades

El script establece automáticamente relaciones bidieccionales entre los individuos:

- Un piloto o director pertenece a un equipo (`esPilotoDe` / `tienePiloto`, `esDirectorDe` / `tieneDirector`).
- Un coche es construido por un equipo y usa un motor (`esConstruidoPor` / `construye`, `utilizaMotor` / `esUtilizadoPor`).
- Una carrera pertenece a una temporada y se celebra en un circuito (`perteneceATemporada` / `tieneCarrera`, `seCelebraEn` / `albergaCarrera`).
- Los campeones ganan campeonatos (`esGanadoPorPiloto` / `ganaCampeonatoPilotos`, `esGanadoPorEquipo` / `ganaCampeonatoConstructores`).
- Un equipo compite en una temporada (`compiteEn`).

## Resultado

El fichero `ontologia_poblada.rdf` es una ontología completa en RDF/XML que contiene:

- Todas las clases y propiedades definidas originalmente en `Prueba.rdf`.
- Individuos de todas las clases concretas, leídos de los CSV.
- Relaciones explícitas que vinculan esos individuos según los datos en los CSV.