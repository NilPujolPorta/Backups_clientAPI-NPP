# Recopilation of backups. API-NPP

*Read this in other languages: [English](README.md), [Español](README.ES-es.md), [Català](README.CA-ca.md).*

## Information
- To execute this program you require python 3 o greater installed. Preferably v3.9
- Requeriments in requirements.txt
- Requires a MySQL database with this strucutre: [Database structure](#Database-structure).
- Database config in `config/config.yaml`
- Error logs in `errorLogs/*txt`
- Use the -h or --help option for more information of [Usage](#Usage)


## Database structure
Inside the database of your choice it's nedded the table ``credencials`` whith the following structure:

The columns names are irrelevant only their positions are.
```
"name" Nom identificatiu, no es pot repetir. SENSE ESPAIS!!!!

"url" Enllaç de la web de login del lloc en questio

"user" Usuari amb permisos d'administrador o de veure les copies

"password" Contrassenya del usuari

"cookie/clau" Per aconseguir la cookie anar al Chrome(o similar) entrar al enllaç anterior i fer inspeccionar elemento; Una vegada alla anem a l'apartat de network clickem CONTROL+R cliquem al resultat que ens sortira i busquem on esta cookie. Per la clau esta en el bitwarden.
```

If it's not created it will create it automatically.

## Installation

- Using pip:

  ```pip install Backups_clientAPI-NPP```

  or
- cloning:

  ```gh repo clone NilPujolPorta/Backups_clientAPI-NPP```

Also install portable chrome v101 in the `Backups_clientAPI`


## Usage
### Ways of executing the program
- In the command line `Backups-clientAPI-NPP [opcions]`
- ```python -m Backups-clientAPI [opcions]```
- Execute the file: `__main__.py [opcions]`
- ```./backups-clientAPI-runner.py [opcions] ```
- Importing the package and using in your project.

### Options
```
usage: __main__.py [-h] [-q] [--portable-chrome-path RUTA] [-tr RUTA] [-g] [--json-file RUTA] [-d SEC] [-v]

Una API per a recullir invormacio de varis NAS Synology que tinguin la versio 6 o mes.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Only shows error messages.
  --portable-chrome-path RUTA
                        Path to portable chrome executable.
  -tr RUTA, --tesseractpath RUTA
                        Route to tesseract.exe
  --json-file RUTA      The path(file not included) where you want to save the json file. By default: es:C:\Users\npujol\eio.cat\Eio-sistemes -
                        Documentos\General\Drive\utilitats\APIs\Backups_clientAPI-NPP\Backups_clientAPI
  -d SEC, --date SEC    The ammount of time (in seconds) back wich the program will look for copies. By default is 2592000(a month)
  -v, --versio          Show the version

For additional configuration options: config/config.yaml
```

### In the near future:
1. Add suport for other database servers
