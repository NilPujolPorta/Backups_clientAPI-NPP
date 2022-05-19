# Recopilación de backups API-NPP

### **Lee en otros idiomas: [English](README.md), [Español](README.ES-es.md), [Català](README.CA-ca.md).**

## Información
- Para ejecutar el programa se tiene que tener instalado python version 3 o superior. Preferiblement v3.9
- Requisitos a requirements.txt
- Requiere una base de datos MySQL con la estructura del apartado [Estructura de la base de datos](#estructura-de-la-base-de-datos).
- 4GB de RAM
- 4rta gen intel cpu o lo equivalente de AMD.
- 500 MB libre de espacio sin contar la base de datos.
- Una connexión estable a internet.
- Configuración de la base de dayos en `config/config.yaml`
- Logs de errores a `errorLogs/*txt`
- Ejecutar con la opción -h o --help para ver mas opciones i funcionalidades de [Uso](#Uso).


## Estructura de la base de datos
En una Base de dayos de tu elección crear una tabla "credencials":
Los nombres de las columnas no son importantes, solo el orden.
```
"nombre" Nombre identificativo, clave primaria. Sin espacios!

"enlace" Enlace de la web de login del dispositivo

"user" Usuari con permisos de administrador o para ver las copias

"contraseña" Contrasseña del usuaria

"cookie/llave/apipasswd" Para conseguir la cookie ir a Chrome(o similar) entrar al enllace anterior i inspeccionar elemento; Una vez alli vamos al apartado de network hacemos CONTROL+R hacemos cliq al resultado i buscamos donde esta la cookie. La llave es el codigo TOTP para el servicio mspbackup. Apipasswd es la contraseña de  la API del Pandora
```

## Instalación

- Usando pip:

  ```pip install Backups_clientAPI-NPP```
  o
- Clonando github:
  ```gh repo clone NilPujolPorta/Backups_clientAPI-NPP```

Instalar [Google Chrome portable v101](GoogleChromePortable_101.0.4951.67_online.paf.exe) y [tesseract](tesseract-ocr-w64-setup-v5.0.0-rc1.20211030.exe) en la carpeta `Backups_clientAPI`.
Recuerda editar el fichero ``config/config.yaml`` con la info de tu base de datos


## Uso
### Maneras de ejecucion del programa
- En la linea de comandos `Backups-clientAPI-NPP [opcions]`
- ```python -m Backups-clientAPI [opcions]```
- Ejecutar el fitxero `__main__.py [opcions]`
- ```./backups-clientAPI-runner.py [opcions] ```
- Importar este paquete en tu proyecto.
- Crear una tarea en **Windows task manager** (el Windows task manager no puede ejecutar el fichero de python, usa un ejecutable como: ``algo.bat`` que ejecute el fichero de python, luego haz que el task manager ejecute `algo.bat`). Usa una **SIMPLE/BASIC TASK**.


### Opciones
```
usage: __main__.py [-h] [-q] [--portable-chrome-path RUTA] [-tr RUTA] [-g] [--json-file RUTA] [-d SEC] [-v]

Una API para recolectar información de copias de seguridad de varios dispositivos o webs.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Solo muestra errores por pantalla.
  --portable-chrome-path RUTA
                        La ruta del ejecutable de chrome portable
  -tr RUTA, --tesseractpath RUTA
                        La ruta hasta al fitxero tesseract.exe
  --json-file RUTA      La ruta(fitxero no incluido) donde se guardara el resultado en JSON.
  -d SEC, --date SEC    La cantidad de tiempo (en segundos) atras para buscar copias. Por defecto es 2592000(un mes)
  -v, --versio          Mostrar la version

Para configuracion adicional ir a config/config.yaml
```

### Proximamente:
1. Añadir soporte para otras bases de datos a parte de mysql
