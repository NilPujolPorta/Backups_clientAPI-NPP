
# Synology Active Backup for Business API-NPP
## Informació
- Per executar el programa s'ha de tenir instalat el python versio 3 o mes.
- Requeriments a requirements.txt
- Requereix una base de dades MySQL amb la estructura en el apartat [Estructura de la base de dades](#estructura-de-la-base-de-dades).
- Configuració de la base de dades a `config/config.yaml`
- Logs de errors a `errorLogs/*txt`
- El fitxer compilar.bat transforma el .py en .pyc que es mes eficient i rapid.
- Executar amb opcio -h per veure mes opcions i funcionalitats.


## Estructura de la base de dades
En una Base de dades que es digui "synology" un taula anomenada "dispositius":
```
"nom" Nom identificatiu, no es pot repetir. SENSE ESPAIS!!!!

"user" Usuari amb permisos d'administrador al active backup

"password" Contrassenya del NAS

"url" Enllaç quickconnect amb la barra final

"cookie" Per aconseguir la cookie anar al Chrome(o similar) entrar al enllaç anterior i fer inspeccionar elemento; Una vegada alla anem a l'apartat de network clickem CONTROL+R cliquem al resultat que ens sortira i busquem on esta cookie

"pandoraID" El numero identificador que te el grup de pandora.
```

## Instal·lació

- Utilitzant pip:

  ```pip install SynologyAPI-NPP```
  
- Clonant el github:
  ```gh repo clone NilPujolPorta/Synology_API-NPP```
  
- Manualment:

  ```wget https://files.pythonhosted.org/packages/3a/2b/8eb8454068f2004a927258f82509b0961c7c72d4b7d958a317819608d11d/SynologyAPI-NPP-1.7.1.tar.gz```

  ```tar -xvzf SynologyAPI-NPP-1.7.1.tar.gz```



## Ús
### Maneres d'execució del programa (ordenades per recomenades)
- A la linea de commandes `SynologyAPI-NPP [opcions]`
- ```python -m SynologyAPI [opcions]```
- Executar el fitxer `synology_API.py` o `synology_API.cpython-39.pyc` amb les opcions adients. Llavors les dades es guardaran a `dadesSynology.json` i si la opcio de excel esta activada tambe es guardara a `revisio_copies_seguretat_synology_vs1.xlsx`
- ```./synology_API-runner.py [opcions] ```

### Opcions
```
usage: SynologyAPI-NPP [-h] [-e] [-q] [-f RUTA] [--json-file RUTA] [-d SEC] [-v]

Una API per a recullir invormacio de varis NAS Synology que tinguin la versio 6 o mes.

optional arguments:
  -h, --help            show this help message and exit
  -e, --excel           Guardar la informacio a un excel, per defecte esta desactivat
  -q, --quiet           Nomes mostra els errors i el missatge de acabada per pantalla.
  -f RUTA, --file RUTA  Especificar la ruta absoluta a on guardar el fitxer d'excel. Per defecte es: la ruta on ho esta aquest fitxer
  --json-file RUTA      La ruta(fitxer inclos) a on es guardara el fitxer de dades json. Per defecte es: la ruta on ho esta aquest fitxer
  -d SEC, --date SEC    La cantitat de temps (en segons) enrere que agafara les dades de copies. Per defecte es
                        2592000(un mes)
  -v, --versio          Mostra la versio

Per configuracio adicional anar a config/config.yaml
```

### Errors coneguts
- Si dona error per algun motiu, en els logs et donara un codi, que llavors pots mirar a errorLogs/0codisErrors.txt per saber el seu significat.
- Si s'interumpeix a mitges el excel pot quedar corromput, pero al borrar-lo  i executar-ho una altre vegada s'arregla.

### Proximament:
1. Afegir support per altres bases de dades a part de mysql
