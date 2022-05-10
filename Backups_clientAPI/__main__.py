import argparse
import json
import os
from importlib_metadata import List
import mysql.connector
import yaml
from os.path import exists

####Local imports###
from LlocDeCopies import LlocDeCopies

from SynologyActive import SynologyActive
from mspbackup import mspbackup
from SynologyHyper import SynologyHyper
from Pandora import Pandora



__version__ = "0.1.5"

def main(args=None):
	global ruta
	ruta = os.path.dirname(os.path.abspath(__file__))
	parser = argparse.ArgumentParser(description='Una API per a recullir invormacio de varis NAS Synology que tinguin la versio 6 o mes.', epilog="Per configuracio adicional anar a config/config.yaml")
	parser.add_argument('-q', '--quiet', help='Nomes mostra els errors i el missatge de acabada per pantalla.', action="store_false")
	parser.add_argument('--portable-chrome-path', help="La ruta del executable de chrome", default=None, metavar="RUTA")
	parser.add_argument('-tr','--tesseractpath', help='La ruta fins al fitxer tesseract.exe', default=ruta+'/tesseract/tesseract.exe', metavar='RUTA')
	parser.add_argument('-g', '--graphicUI', help='Mostra el navegador graficament.', action="store_false")
	parser.add_argument('--json-file', help='La ruta(fitxer no inclos) a on es guardara el fitxer de dades json. Per defecte es:'+ruta, default=ruta, metavar='RUTA')
	parser.add_argument('-d', '--date', type=int, help='La cantitat de temps (en segons) enrere que agafara les dades de copies. Per defecte es 2592000(un mes)', default=2592000, metavar='SEC')
	parser.add_argument('-v', '--versio', help='Mostra la versio', action='version', version='Backups_clientAPI-NPP v' + __version__)
	args = parser.parse_args(args)
	global conf
	conf = ruta+"/config/config.yaml"
	global current_transaction
	current_transaction = 2

	mydb = initialize()

	nasos = retrieveData(mydb, args)



	if not(saveDataDB(nasos)):
		saveJSON(nasos, ruta, args)


#Aquesta funció cre les carpetes i fitxers necesarris, segidament inicia la connexio a la DB i retorna aquesta
# si no consegueix conectar tanca el programa
def initialize():
	"""Create the folders necessary for the program and iniciates the database connection taking the credentials from the config file.
	If it doesn't manage to connect to the database it quits the program.

	Returns
	-------
	MySQLConnection
		Connection to hte the database.

	"""
	if not(os.path.exists(ruta+"/errorLogs")):
		os.mkdir(ruta+"/errorLogs")
	if not(os.path.exists(ruta+"/config")):
		os.mkdir(ruta+"/config")
	if not(exists(conf)):
		print("Emplena el fitxer de configuracio de Base de Dades a config/config.yaml")
		article_info = [
			{
				'BD': {
				'host' : 'localhost',
				'user': 'root',
				'passwd': 'patata',
				'database':'backups'
				}
			}
		]
		if not(os.path.exists(ruta+"/config")):
			os.mkdir(ruta+"/config")
		with open(conf, 'w') as yamlfile:
			data = yaml.dump(article_info, yamlfile)

	with open(conf, "r") as yamlfile:
		data = yaml.load(yamlfile, Loader=yaml.FullLoader)

	servidorBD = data[0]['BD']['host']
	usuariBD = data[0]['BD']['user']
	contrassenyaBD = data[0]['BD']['passwd']
	database = data[0]['BD']['database']
	try:
		mydb =mysql.connector.connect(
    	    host=servidorBD,
    	    user=usuariBD,
    	    password=contrassenyaBD,
    	    database=database
    	    )
		mycursor = mydb.cursor(buffered=True)
	except:
		try:        
			mydb =mysql.connector.connect(
	            host=servidorBD,
	            user=usuariBD,
	            password=contrassenyaBD
	            )
			print("Base de dades no existeix, creant-la ...")
			mycursor = mydb.cursor(buffered=True)
			mycursor.execute("CREATE DATABASE backups")
			mydb =mysql.connector.connect(
	            host=servidorBD,
	            user=usuariBD,
	            password=contrassenyaBD,
	            database=database
	            )
			mycursor = mydb.cursor(buffered=True)
			mycursor.execute("CREATE TABLE `credencials` (`name` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,`url` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'https://',`TipusCopies` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'TriaTipus',`user` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'usuari',`password` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '******',`cookie/clau` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,PRIMARY KEY (`name`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci")
		except:
			print("Login BDD incorrecte")
			quit()
	return mydb


#Aquesta funció recull les dades de la base de dades i les transforma en objectes de la classe pertinent 
#tambe executa la funcio retrieve_Copies de cada LlocDeCopies la cual afegeix totes les copies a l'array de copies de cada LlocDeCopies
#S'he l'hi ha de donar la connexio a la base de dades junt amb els arguments i retorna una llista de llocDeCopies
def retrieveData(mydb, args:argparse.Namespace)-> List[LlocDeCopies]:
	"""Retrieves all the LlocDeCopies from a given database.
	It also gets the copies from each LlocDeCopies and saves them in the corresponding LlocDeCopies object.
	
	Parameters
	----------
	mydb:MySQLConnection
		Connection to the MySQL database.
	args:Namespace
		arguments of argsparse.

	Returns
	-------
	List[LlocDeCopies]
		List of all the LlocDeCopies in the database.

	"""
	mycursor = mydb.cursor(buffered=True)
	nasos:List[LlocDeCopies] = []
	mycursor.execute("SELECT * FROM credencials")
	resultatbd = mycursor.fetchall()
	for x in resultatbd:
		if x[2] == "ActiveBackupBusiness":
			nasos.append(SynologyActive(x[0], x[1], x[3], x[4], x[5]))
		elif x[2] == "mspbackup":
			nasos.append(mspbackup(x[0], x[1], x[3], x[4], x[5]))
		elif x[2] == "HyperBackup":
			nasos.append(SynologyHyper(x[0], x[1], x[3], x[4]))
		elif x[2] == "Pandora":
			nasos.append(Pandora(x[0], x[1], x[3], x[4], x[5]))

	for nas in nasos:
		if(nas.checkConnection()):
			nas.retrieve_copies(ruta, args)
		else:
			print("Error de conexio")
	return nasos


#======In progress=========, guarda les dades en un JSON
#S'he li ha de passar la llista de copies retorna boolea depenet si ho ha conseguit o no
def saveJSON(nasos:List[LlocDeCopies], ruta:str, args)->bool:
	pass


def saveDataDB(nasos:List[LlocDeCopies])->bool:
	"""Saves copies to the array of this object
	
	Parameters
	----------
	nasos : List[LlocDeCopies]
		List of all the LlocDeCopies wanted to be saved in the DB

	Returns
	-------
	bool
		If it manages to save all the copies True otherwise False.

	"""
	try:
		mydb = initialize()
		mycursor = mydb.cursor(buffered=True)
		try:
			mycursor.execute("DROP TABLE copies;")
		except:
			pass
		mycursor.execute("CREATE TABLE copies (ID varchar(50), Status varchar(50), NomLlocDeCopies varchar(50));")
		for nas in nasos:
			for copia in nas.get_copies():
				
				mycursor.execute("INSERT INTO copies (ID, Status, NomLlocDeCopies) VALUES ('" + copia.get_id() + "', '"+ copia.get_status()+"', '"+ (copia.get_LlocDeCopies()).get_name()+"');")
		mydb.commit()
		return True
	except:
		return False

#El que fa aixo es que totes les execucions d'aquest fitxer iniciin la funcio main
if __name__ == "__main__":
    main()