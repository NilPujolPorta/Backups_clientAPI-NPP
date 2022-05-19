# Recopilation of backups. API-NPP

### **Read this in other languages: [English](README.md), [Español](README.ES-es.md), [Català](README.CA-ca.md).**

Keep in mind part of the program is in catalan

## Information
- To execute this program you require python 3 o greater installed. Preferably v3.9
- Dependencies in requirements.txt
- Requires a MySQL database with this strucutre: [Database structure](#Database-structure).
- 4GB of RAM.
- 4th gen intel cpu or equivalent AMD.
- Windows 10, 11, Server 2016 or greater
- 500 MB of free space without conting database space usage.
- Stable internet connection. 
- Database config in `config/config.yaml`
- Error logs in `errorLogs/*txt`
- Use the -h or --help option for more information of [Usage](#Usage)


## Database structure
Inside the database of your choice it's nedded the table ``credencials`` whith the following structure:

The columns names are irrelevant only their positions are.
```
"name" Primary key, name of the device. Without spaces

"url" Login or API(in case of PandoraFMS) url of the device

"user" User with permission to see the backups

"password" The users password

"cookie/key/apipasswd" To get the cookie open Chrome, or similar, go to the url avobe and inspect element; Once there in the network tabwe do CONTROL+R cliquem al resultat que ens sortira i busquem on esta cookie. The key is the TOTP of the mspbackup. And the apipassword is the password of the Pandora API
```

If it's not created it will create it automatically.

## Installation

- Using pip:

  ```pip install Backups_clientAPI-NPP```

  or
- cloning:

  ```gh repo clone NilPujolPorta/Backups_clientAPI-NPP```

Install [portable chrome v101](GoogleChromePortable_101.0.4951.67_online.paf.exe) and [tesseract](tesseract-ocr-w64-setup-v5.0.0-rc1.20211030.exe) in the `Backups_clientAPI` folder.
Remember to edti the ``config/config.yaml`` file to your correct database info.


## Usage
### Ways of executing the program
- In the command line `Backups-clientAPI-NPP [opcions]`
- ```python -m Backups-clientAPI [opcions]```
- Execute the file: `__main__.py [opcions]`
- ```./backups-clientAPI-runner.py [opcions] ```
- Importing the package and using in your own project.
- Creating a task in **Windows task manager** (Windows task manager is UNABLE to execute the python file directly, use a executable like ``something.bat`` file that executes the python file and tell the task manager to execute the .bat file). Use a **SIMPLE/BASIC TASK**.

### Options
```
usage: __main__.py [-h] [-q] [--portable-chrome-path RUTA] [-tr RUTA] [-g] [--json-file RUTA] [-d SEC] [-v]

An API to recollect backups information from various sources.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Only shows error messages.
  --portable-chrome-path RUTA
                        Path to portable chrome executable.
  -tr RUTA, --tesseractpath RUTA
                        Route to tesseract.exe
  --json-file RUTA      The path(file not included) where you want to save the json file. 
  -d SEC, --date SEC    The ammount of time (in seconds) back wich the program will look for copies. By default is 2592000(a month)
  -v, --versio          Show the version

For additional configuration options: config/config.yaml
```

### In the near future:
1. Add suport for other database servers
