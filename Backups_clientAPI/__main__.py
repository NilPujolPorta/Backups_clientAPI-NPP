import argparse
import datetime
import json
import os
from importlib_metadata import List
import mysql.connector
import yaml
from os.path import exists
import matplotlib.pyplot as plt

####Local imports###
from LlocDeCopies import LlocDeCopies

from SynologyActive import SynologyActive
from mspbackup import mspbackup
from SynologyHyper import SynologyHyper
from Pandora import Pandora



__version__ = "0.1"

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


	mycursor = mydb.cursor(buffered=True)
	nasos = []
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


	#prior retrieveData()
	for nas in nasos:
		if(nas.checkConnection):
			nas.retrieve_copies(ruta, args)
		else:
			print("Error de conexio")
	#END prior retrieveData()
	
	showData(nasos, args)
	saveJSON(nasos, ruta, args)
	saveDataDB(nasos, args)


def initialize():
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
			return
	return mydb

def showData(nasos:List[LlocDeCopies], args) -> None:
	StatusActive = []
	StatusMSP = []
	StatusHyper = []
	StatusPandora = []
	for nas in nasos:
		if not(nas.checkConnection):
			print("Error de conexio")
			return
		else:
			if (isinstance(nas, SynologyActive)):
				StatusActive = [*StatusActive, *nas.get_status_copies()]
			elif (isinstance(nas, mspbackup)):
				StatusMSP = [*StatusMSP, *nas.get_status_copies()]
			elif (isinstance(nas, SynologyHyper)):
				StatusHyper = [*StatusHyper, *nas.get_status_copies()]
			elif (isinstance(nas, Pandora)):
				StatusPandora = [*StatusPandora, *nas.get_status_copies()]
			else:
				pass
			#############
	plt.figure(1) #Graphics ActiveBackupBusiness
	ActivePie=[0,0,0,1]
	ActivePie[0]+=(StatusActive.count("Correcte"))
	ActivePie[1]+=(StatusActive.count("Warning"))
	ActivePie[2]+=(StatusActive.count("Error"))
	ActivePie[3]+=(StatusActive.count("CodiDesconegut"))
	names = ["Correcte", "Error", "Warning"]
	colors = ["Green", "Red", "Yellow"]
	plt.pie(ActivePie, wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' }, colors=colors, shadow=True)
	plt.legend(labels=names, title="Status Active Backup for Business")
	#############
	plt.figure(2)#Graphics mspbackup
	MSPPie=[0,0,0,1]
	MSPPie[0]+=(StatusMSP.count("Correcte"))
	MSPPie[1]+=(StatusMSP.count("Warning"))
	MSPPie[2]+=(StatusMSP.count("Error"))
	MSPPie[3]+=(StatusMSP.count("Atrasats"))
	names = ["Correcte", "Error", "Warning", "Atrasats"]
	colors = ["Green", "Red", "Yellow", "#fe7d09"]
	plt.pie(MSPPie, wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' }, colors=colors, shadow=True)
	plt.legend(labels=names, title="Status mspBackups")
	#############
	plt.figure(3)#Graphics HyperBackup
	HyperPie=[0,0,0,1]
	HyperPie[0]+=(StatusHyper.count("Correcte")+StatusHyper.count("Success"))
	HyperPie[1]+=(StatusHyper.count("Warning")+StatusHyper.count("Advertencia"))
	HyperPie[2]+=(StatusHyper.count("Error"))
	HyperPie[3]+=(StatusHyper.count("Espera a que acabi el proces actual"))
	names = ["Correcte", "Error", "Warning", "Espera a que acabi el proces actual"]
	colors = ["Green", "Red", "Yellow", "Blue"]
	plt.pie(HyperPie, wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' }, colors=colors, shadow=True)
	plt.legend(labels=names, title="Status HyperBackup")
	#############
	plt.figure(4)#Graphics Pandora
	PandoraPie=[0,0,0,1]
	PandoraPie[0]+=(StatusPandora.count("Correcte"))
	PandoraPie[1]+=(StatusPandora.count("Warning"))
	PandoraPie[2]+=(StatusPandora.count("Error"))
	PandoraPie[3]+=(StatusPandora.count("Desconegut/desconectat"))
	names = ["Correcte", "Error", "Warning", "Desconegut/desconectat"]
	colors = ["Green", "Red", "Yellow", "#fe7d09"]
	plt.pie(PandoraPie, wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' }, colors=colors, shadow=True)
	plt.legend(labels=names, title="Status Pandora")
	#plt.show()

def saveJSON(nasos:List[LlocDeCopies], ruta:str, args):
	pass

def saveDataDB(nasos:List[LlocDeCopies], args)->bool:
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
				
				hey = "INSERT INTO copies (ID, Status, NomLlocDeCopies) VALUES ('" + copia.get_id() + "', '"+ copia.get_status()+"', '"+ (copia.get_LlocDeCopies()).get_name()+"');"
				print(hey)
				mycursor.execute(hey)
		mydb.commit()
		return True
	except:
		return False

#El que fa aixo es que totes les execucions d'aquest fitxer iniciin la funcio main
if __name__ == "__main__":
    main()