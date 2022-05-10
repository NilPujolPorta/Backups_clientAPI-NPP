# Recopilacio de backups API-NPP
## Informació
- Per executar el programa s'ha de tenir instalat el python versio 3 o mes.
- Requeriments a requirements.txt
- Requereix una base de dades MySQL amb la estructura en el apartat [Estructura de la base de dades](#estructura-de-la-base-de-dades).
- Configuració de la base de dades a `config/config.yaml`
- Logs de errors a `errorLogs/*txt`
- El fitxer compilar.bat transforma el .py en .pyc que es mes eficient i rapid.
- Executar amb opcio -h per veure mes opcions i funcionalitats.


## Estructura de la base de dades
En una Base de dades que es digui "backups" un taula anomenada "credencials":
Els noms de les columnes de la base de dades no son rellevants només el seu ordre
```
"name" Nom identificatiu, no es pot repetir. SENSE ESPAIS!!!!

"url" Enllaç de la web de login del lloc en questio

"user" Usuari amb permisos d'administrador o de veure les copies

"password" Contrassenya del usuari

"cookie/clau" Per aconseguir la cookie anar al Chrome(o similar) entrar al enllaç anterior i fer inspeccionar elemento; Una vegada alla anem a l'apartat de network clickem CONTROL+R cliquem al resultat que ens sortira i busquem on esta cookie. Per la clau esta en el bitwarden.
```

## Instal·lació

- Utilitzant pip:

  ```pip install Backups_clientAPI-NPP```
  o
- Clonant el github:
  ```gh repo clone NilPujolPorta/Backups_clientAPI-NPP```

i a mes instal·lar el chrome portable versió 101 a la carpeta de


## Ús
### Maneres d'execució del programa (ordenades per recomenades)
- A la linea de commandes `Backups-clientAPI-NPP [opcions]`
- ```python -m Backups-clientAPI [opcions]```
- Executar el fitxer `__main__.py`amb les opcions adients.
- ```./backups-clientAPI-runner.py [opcions] ```

### Opcions
```
usage: __main__.py [-h] [-q] [--portable-chrome-path RUTA] [-tr RUTA] [-g] [--json-file RUTA] [-d SEC] [-v]

Una API per a recullir invormacio de varis NAS Synology que tinguin la versio 6 o mes.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Nomes mostra els errors i el missatge de acabada per pantalla.
  --portable-chrome-path RUTA
                        La ruta del executable de chrome
  -tr RUTA, --tesseractpath RUTA
                        La ruta fins al fitxer tesseract.exe
  -g, --graphicUI       Mostra el navegador graficament.
  --json-file RUTA      La ruta(fitxer no inclos) a on es guardara el fitxer de dades json. Per defecte es:C:\Users\npujol\eio.cat\Eio-sistemes -
                        Documentos\General\Drive\utilitats\APIs\Backups_clientAPI-NPP\Backups_clientAPI
  -d SEC, --date SEC    La cantitat de temps (en segons) enrere que agafara les dades de copies. Per defecte es 2592000(un mes)
  -v, --versio          Mostra la versio

Per configuracio adicional anar a config/config.yaml
```

### Proximament:
1. Afegir support per altres bases de dades a part de mysql
