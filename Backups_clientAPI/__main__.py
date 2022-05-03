import argparse
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

	initialize()

	nasos = LoadData()

	#old retrieveData()
	for nas in nasos:
		if(nas.checkConnection):
			nas.retrieve_copies(ruta, args)
		else:
			print("Error de conexio")
	#END old retrieveData()
	
	writeData(nasos, ruta, args)



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

def LoadData() -> List[LlocDeCopies]:
	with open(conf, "r") as yamlfile:
		data = yaml.load(yamlfile, Loader=yaml.FullLoader)

	servidorBD = data[0]['BD']['host']
	usuariBD = data[0]['BD']['user']
	contrassenyaBD = data[0]['BD']['passwd']
	databaseBD = data[0]['BD']['database']

	taulabd =bd(servidorBD, usuariBD, contrassenyaBD, databaseBD)
	nasos = []
	for x in taulabd:
		if x[2] == "ActiveBackupBusiness":
			nasos.append(SynologyActive(x[0], x[1], x[3], x[4], x[5]))
		elif x[2] == "mspbackup":
			nasos.append(mspbackup(x[0], x[1], x[3], x[4], x[5]))
		elif x[2] == "HyperBackup":
			nasos.append(SynologyHyper(x[0], x[1], x[3], x[4]))
		elif x[2] == "Pandora":
			nasos.append(Pandora(x[0], x[1], x[3], x[4], x[5]))
	return nasos



def bd(servidorBD:str, usuariBD:str, contrassenyaBD:str, database:str)->List[str]:
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
			mycursor.execute("CREATE TABLE credencials (nom name(25), url VARCHAR(100), TipusCopies VARCHAR(25), user VARCHAR(45), password VARCHAR(45));")
		except:
			print("Login BDD incorrecte")
			return
	taulabdi = []

	mycursor.execute("SELECT * FROM credencials")
	resultatbd = mycursor.fetchall()
	for fila in resultatbd:
		taulabdi.append(fila)
	return(taulabdi)

def writeData(nasos:List[LlocDeCopies], ruta:str, args) -> None:
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
				StatusActive.append(nas.get_status_copies())
			elif (isinstance(nas, mspbackup)):
				StatusMSP.append(nas.get_status_copies())
			elif (isinstance(nas, SynologyHyper)):
				StatusHyper.append(nas.get_status_copies())
			elif (isinstance(nas, Pandora)):
				StatusPandora.append(nas.get_status_copies())
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
			plt.pie(ActivePie, wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' }, colors=colors, shadow=True)
			plt.legend(labels=names, title="Status mspBackups")
			#############
			plt.figure(2)#Graphics HyperBackup
			MSPPie=[0,0,0,1]
			MSPPie[0]+=(StatusMSP.count("Correcte")+StatusMSP.count("Success"))
			MSPPie[1]+=(StatusMSP.count("Warning")+StatusMSP.count("Advertencia"))
			MSPPie[2]+=(StatusMSP.count("Error"))
			MSPPie[3]+=(StatusMSP.count("Espera a que acabi el proces actual"))
			names = ["Correcte", "Error", "Warning", "Espera a que acabi el proces actual"]
			colors = ["Green", "Red", "Yellow", "Blue"]
			plt.pie(ActivePie, wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' }, colors=colors, shadow=True)
			plt.legend(labels=names, title="Status HyperBackup")
			#############
			plt.figure(2)#Graphics Pandora
			MSPPie=[0,0,0,1]
			MSPPie[0]+=(StatusMSP.count("Correcte"))
			MSPPie[1]+=(StatusMSP.count("Warning"))
			MSPPie[2]+=(StatusMSP.count("Error"))
			MSPPie[3]+=(StatusMSP.count("Desconegut/desconectat"))
			names = ["Correcte", "Error", "Warning", "Desconegut/desconectat"]
			colors = ["Green", "Red", "Yellow", "#fe7d09"]
			plt.pie(ActivePie, wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' }, colors=colors, shadow=True)
			plt.legend(labels=names, title="Status Pandora")
			plt.show()




#El que fa aixo es que totes les execucions d'aquest fitxer iniciin la funcio main
if __name__ == "__main__":
    main()