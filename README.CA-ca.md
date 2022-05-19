# Recopilació de backups API-NPP

### **Llegeix en altres idiomes: [English](README.md), [Español](README.ES-es.md), [Català](README.CA-ca.md).**

## Informació
- Per executar el programa s'ha de tenir instalat el python versio 3 o mes.
- Requeriments a requirements.txt
- Requereix una base de dades MySQL amb la estructura en el apartat [Estructura de la base de dades](#estructura-de-la-base-de-dades).
- 4GB de RAM
- 4rta gen intel cpu o l'equivalent d'AMD.
- 500 MB lliures de espai sense conta la base de dades.
- Una connexió estable a internet.
- Configuració de la base de dades a `config/config.yaml`
- Logs de errors a `errorLogs/*txt`
- Executar amb opció -h o --help per veure mes opcions i funcionalitats d'[Ús](#Ús).


## Estructura de la base de dades
En una Base de dades de la teva elecció crear un taula anomenada "credencials":
Els noms de les columnes de la base de dades no son rellevants només el seu ordre
```
"nom" Nom identificatiu, no es pot repetir. SENSE ESPAIS!!!!

"enllaç" Enllaç de la web de login del lloc en questio

"usuari" Usuari amb permisos d'administrador o de veure les copies

"contassenya" Contrassenya del usuari

"galeta/clau/apipasswd" Per aconseguir la galeta anar al Chrome(o similar) entrar al enllaç anterior i fer inspeccionar elemento; Una vegada alla anem a l'apartat de network clickem CONTROL+R cliquem al resultat que ens sortira i busquem on esta cookie. La clau es la clau TOTP del mspbackup. El apipasswd es la contrassenya de la api de Pandora.
```  

## Instal·lació

- Utilitzant pip:

  ```pip install Backups_clientAPI-NPP```
  o
- Clonant el github:
  ```gh repo clone NilPujolPorta/Backups_clientAPI-NPP```

Instal·lar [Google Chrome portable v101](GoogleChromePortable_101.0.4951.67_online.paf.exe) i [tesseract](tesseract-ocr-w64-setup-v5.0.0-rc1.20211030.exe) a la carpeta `Backups_clientAPI`.
Recorda editar el fitxer ``config/config.yaml`` amb la info de la teva base de dades


## Ús
### Maneres d'execució del programa (ordenades per recomenades)
- A la linea de commandes `Backups-clientAPI-NPP [opcions]`
- ```python -m Backups-clientAPI [opcions]```
- Executar el fitxer `__main__.py`amb les opcions adients.
- ```./backups-clientAPI-runner.py [opcions] ```
- Important el paquet i utilitzar-lo en el teu propi projecte.
- Creant una tasca en **Windows task manager** (el Windows task manager no pot executar el fitxer de python, utilitza un executable com: ``algo.bat`` que executi el fitxer de python, llavors fes que el task manager executi `algo.bat`). Utilitza una **SIMPLE/BASIC TASK**.

### Opcions
```
usage: __main__.py [-h] [-q] [--portable-chrome-path RUTA] [-tr RUTA] [-g] [--json-file RUTA] [-d SEC] [-v]

Una API per a recullir informació de copies de seguretat de varis tipus de dispositius o llocs web.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Nomes mostra els errors i el missatge de acabada per pantalla.
  --portable-chrome-path RUTA
                        La ruta del executable de chrome
  -tr RUTA, --tesseractpath RUTA
                        La ruta fins al fitxer tesseract.exe
  --json-file RUTA      La ruta(fitxer no inclos) a on es guardara el fitxer de dades json.
  -d SEC, --date SEC    La cantitat de temps (en segons) enrere que agafara les dades de copies. Per defecte es 2592000(un mes)
  -v, --versio          Mostra la versio

Per configuracio adicional anar a config/config.yaml
```

### Proximament:
1. Afegir support per altres bases de dades a part de mysql
