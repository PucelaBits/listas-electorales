# Explorador de listas electorales España<!-- omit in toc -->

> [![license](https://img.shields.io/badge/license-AGPL-blue.svg)](./LICENSE)

Este proyecto **descarga, decodifica y normaliza** los datos oficiales de las candidaturas y candidatos de las elecciones democráticas de la historia reciente de España (1979 - 2023). Los datos se pueden explorar de forma interactiva en el [portal web](https://pucelabits.github.io/listas-electorales/).

- [Datos](#datos)
- [Uso](#uso)
  - [Portal web](#portal-web)
  - [Regenerar los datos](#regenerar-los-datos)
- [Aviso legal](#aviso-legal)
  - [Atribución y origen de los datos](#atribución-y-origen-de-los-datos)
  - [Protección de datos personales](#protección-de-datos-personales)
  - [Licencia del código](#licencia-del-código)

## Datos

El repositorio cubre las candidaturas y candidatos de:

- Elecciones **generales** (Congreso de los Diputados y Senado)
- Elecciones **municipales** y de **cabildos insulares** (Canarias)
- Elecciones al **Parlamento Europeo**
- Elecciones **autonómicas** (en desarrollo, ver más abajo)

> :warning: Las elecciones autonómicas no las publica el Ministerio del Interior (son competencia de cada Comunidad Autónoma). Estamos trabajando en incorporarlas, pero de momento no están disponibles.

Los datos de las elecciones se pueden encontrar en [`data/election_dates.csv`](data/election_dates.csv).

> :warning: Por falta de datos oficiales, no hemos podido incluir los datos de las elecciones europeas de 1985, las elecciones municipales de 1979 y 1983, las elecciones de cabildos insulares de 1979, 1983 y 1999.

Los últimos datos generados se encuentran en [`docs/data/electoral_data.csv.gz`](docs/data/electoral_data.csv.gz) (CSV comprimido con GZIP). El CSV contiene las siguientes columnas:

- `full_name`: Nombre completo del candidato
- `election_type`: Tipo de elección
- `year`: Año de la elección
- `month`: Mes de la elección
- `acronym`: Acrónimo del partido político / coalición
- `name`: Nombre del partido político / coalición
- `municipality`: Municipio (puede estar vacío)
- `province`: Provincia (puede estar vacío)
- `order`: Orden de lista
- `substitute`: Indicador de suplente (1 = sí, 0 = no)
- `elected`: Indicador de si el candidato fue electo (1 = sí, 0 = no), no disponible para elecciones autonómicas.

## Uso

### Portal web

La carpeta `docs` contiene un portal web estático (sin dependencias, solo archivos estáticos) que carga los datos de forma local en el navegador. Permite buscar y filtrar candidatos por cada uno de los campos del CSV.

Solamente abrir `docs/index.html` en un navegador o puedes visitar la versión [en línea](https://pucelabits.github.io/listas-electorales/).

### Regenerar los datos

Aunque los datos ya están generados y disponibles en `docs/data/electoral_data.csv.gz`, puedes regenerarlos ejecutando el script `src/main.py` desde la raíz del repositorio:

```console
$ python src/main.py
```

#### Requisitos<!-- omit in toc -->

Para ejecutar el script necesitas:

- **Python 3.10+**.
- Dependencias de terceros: `requests` y `pandas` — instálalas con:

```console
$ pip install -r requirements.txt
```

## Aviso legal

### Atribución y origen de los datos

- Parte del código (en particular los códigos de decodificación de provincias y municipios) procede del proyecto [`infoelectoral`](https://github.com/JaimeObregon/infoelectoral)
  de Jaime Gómez-Obregón, distribuido bajo la licencia [GNU AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html).
- Parte del código (en particular la descarga automática de los datos oficiales) se inspira en el código del proyecto [`rOpenSpain/infoelectoral`](https://github.com/rOpenSpain/infoelectoral), distribuido bajo la licencia [GPL-2](https://www.r-project.org/Licenses/GPL-2).
- El origen de los datos oficiales respecto a las elecciones generales, municipales, europeas y cabildos insulares proviene, sin alterarse, del [área de descarga del portal infoelectoral](https://infoelectoral.interior.gob.es/) del Ministerio del Interior.
- Las tablas de decodificación de municipios y provincias proceden del Instituto Nacional de Estadística (y algunos datos adicionales obtenidos de Agencia Estatal de Meteorología), con una ligera normalización de los nombres de los municipios.

El Ministerio del Interior, el Instituto Nacional de Estadística (INE) y la Agencia Estatal de Meteorología (AEMET) **no** participan, patrocinan ni necesariamente apoyan esta reutilización de datos ni los objetivos del proyecto.

### Protección de datos personales

Este software habilita la descarga de los datos oficiales que comprenden las listas electorales en las que han concurrido cientos de miles de candidatos desde la restauración democrática en España.

De esta descarga pueden deducirse listas que relacionen nombres de personas con los distintos partidos políticos en los que han concurrido a elecciones. Esto podría asemejarse a un fichero de datos personales de naturaleza ideológica y, por lo tanto, estar protegido por legislación específica que impediría el tratamiento que se podría llevar a cabo gracias a este repositorio.

No obstante, la Agencia Española de Protección de Datos, en su Resolución de 17 de julio de 2013, apartado séptimo, recuerda la jurisprudencia constitucional al respecto (el texto marcado en negrita procede proyecto [`infoelectoral`](https://github.com/JaimeObregon/infoelectoral) de Jaime Gómez-Obregón):

> En relación a los responsables de fichero respecto de los que se solicita el derecho de oposición debe tenerse en cuenta la STC 110/2007, de 10 de mayo, que recuerda la STC 85/2003 en la que se señaló que "las informaciones protegidas frente a una publicidad no querida por el art. 18.1 CE se corresponden con los aspectos más básicos de la autodeterminación personal y es obvio que entre aquellos aspectos básicos no se encuentran los datos referentes a la participación de los ciudadanos en la vida política, actividad que por su propia naturaleza se desarrolla en la esfera pública de una sociedad democrática, con excepción del derecho de sufragio activo dado el carácter secreto del voto. De esta manera, el ejercicio del derecho de participación política (art. 23.1 CE) implica en general la renuncia a mantener ese aspecto de la vida personal alejada del público conocimiento.

> A ello debe añadirse el carácter público que la legislación electoral atribuye a determinadas actuaciones de los ciudadanos en los procesos electorales, en concreto, la publicación de las candidaturas presentadas y proclamadas en las elecciones, que se efectúa, para las municipales, en el Boletín Oficial de la Provincia (arts. 47 y 187.4 LOREG); y la publicación de los electos, que se efectúa, para todo tipo de elecciones, en el Boletín Oficial del Estado (art. 108.6 LOREG). Estas normas que prescriben la publicidad de candidatos proclamados y electos son, por otra parte, básicas para la transparencia política que en un Estado democrático debe regir las relaciones entre electores y elegibles". (F. 21). En esta misma resolución rechazamos igualmente que pudiera "considerarse vulnerado el derecho fundamental a la protección de datos (art. 18.4 CE), que faculta a los ciudadanos para oponerse a que determinados datos personales sean utilizados para fines distintos de aquel legítimo que justificó su obtención (STC 94/1988, de 24 de mayo, F. 4). Tal derecho persigue garantizar a las personas un poder de control sobre sus datos personales, sobre su uso y su destino, con el propósito de impedir su tráfico ilícito y lesivo para la dignidad y derecho del afectado (STC 292/2000, de 30 de noviembre, F. 6). Pero ese poder de disposición no puede pretenderse con respecto al único dato relevante en este caso, a saber, la vinculación política de aquellos que concurren como candidatos a un proceso electoral pues, como hemos dicho, se trata de datos publicados a los que puede acceder cualquier ciudadano y que por tanto quedan fuera del control de las personas a las que se refieren. **La adscripción política de un candidato es y debe ser un dato público en una sociedad democrática, y por ello no puede reclamarse sobre él ningún poder de disposición**" (F. 12). En términos análogos, se han pronunciado las SSTC 99/2004, F. 13, y 68/2005, F. 15.

### Licencia del código

Este repositorio se distribuye bajo la **GNU Affero General Public License v3** o posterior.

Ver [`LICENSE`](./LICENSE) para más detalles.
