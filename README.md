# PajaritoHack 🐦

Herramienta CLI para descargar audios de aves desde datasets exportados de Cornell/eBird Media.

## Descripción

PajaritoHack automatiza la descarga masiva de archivos MP3 utilizando los identificadores `ML Catalog Number` presentes en los CSV exportados desde el catálogo multimedia de Cornell.

La plataforma de Cornell/eBird permite exportar hasta miles de registros de audio en formato CSV, pero no ofrece una descarga masiva directa de los audios.
PajaritoHack aprovecha los `asset IDs` públicos para construir automáticamente las URLs de descarga y recuperar los archivos MP3 asociados.

## Fuente de datos

Los CSV pueden obtenerse desde el catálogo multimedia de eBird Media:

[eBird Media Catalog](https://media.ebird.org/catalog?utm_source=chatgpt.com)

Ejemplo de búsqueda:

[Compotón listado de audios](https://media.ebird.org/catalog?birdOnly=true&taxonCode=compot1&mediaType=audio&view=list&utm_source=chatgpt.com)

## Funcionamiento

1. Buscar una especie en eBird Media.
2. Filtrar resultados de audio.
3. Exportar el CSV desde Cornell.
4. Ejecutar `PajaritoHack`.
5. Seleccionar el CSV descargado.
6. Elegir:

   * cantidad de filas,
   * o rango de filas.
7. Descargar automáticamente los MP3.

## Características

* Descarga masiva de audios MP3
* Soporte para CSV exportados desde Cornell/eBird
* Selector gráfico de archivos CSV
* Descarga por cantidad o rango
* Prevención de redescargas duplicadas
* Manejo de interrupción mediante `Ctrl+C`
* ASCII UI adaptable al tamaño de terminal
* Compatible con CSV grandes (miles de registros)

## Requisitos

* Python 3.10+
* Windows / Linux
* Conexión a Internet

## Dependencias

* pandas
* requests

## Instalación

Clonar repositorio:

```bash
git clone https://github.com/HernanVirgilioFerreyra/PajaritoHack.git
cd PajaritoHack
```

Instalar dependencias:

```bash
pip install pandas requests
```

## Uso

Ejecutar:

```bash
python PajaritoHack.py
```

o:

```bash
py PajaritoHack.py
```

## Formatos de descarga soportados

Entrada válida:

```text
20
```

Descarga:

* filas 1 a 20

Entrada válida:

```text
1-20
```

Descarga:

* filas 1 a 20

Entrada válida:

```text
30-35
```

Descarga:

* filas 30 a 35

Entrada inválida:

```text
35-30
```

Resultado:

* rechazada automáticamente

## Estructura esperada del CSV

El CSV debe contener una columna con los `ML Catalog Number` exportados desde Cornell/eBird Media.

Actualmente el script utiliza la primera columna del CSV como fuente de IDs.

## Salida

Los audios descargados se almacenan automáticamente en:

```text
audios/
```

## Empaquetado EXE

Generar ejecutable standalone:

Instalar PyInstaller:

```bash
pip install pyinstaller
```

Compilar:

```bash
pyinstaller --onefile --hidden-import=tkinter PajaritoHack.py
```

El ejecutable generado aparecerá en:

```text
dist/PajaritoHack.exe
```

## Limitaciones

* Cornell/eBird no ofrece descarga masiva oficial de MP3.
* El sistema depende de endpoints públicos accesibles mediante `asset IDs`.
* Cambios futuros en la infraestructura de Cornell podrían romper compatibilidad.


## Autor

Hernán Virgilio Ferreyra
