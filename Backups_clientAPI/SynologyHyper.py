import datetime
import os
import time
from LlocDeCopies import LlocDeCopies
from Copia import Copia
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import wget
from utils import temps

class SynologyHyper(LlocDeCopies):
    def __init__(self, name:str, url:str, user:str, password:str):
        super().__init__(name, url, user, password)
    def retrieve_copies(self:LlocDeCopies, ruta:str, args)-> None:
        if not(os.path.exists(ruta+"/chromedriver.exe")):
            wget.download("https://github.com/NilPujolPorta/Backups_clientAPI-NPP/blob/master/Backups_clientAPI-NPP/chromedriver.exe?raw=true", ruta+"/chromedriver.exe")

            print()
        options = Options()
        options.binary_location = "C:\\Users\\npujol\\eio.cat\\Eio-sistemes - Documentos\\General\\Drive\\utilitats\\APIs\\Backups_clientAPI-NPP\\Backups_clientAPI\\GoogleChromePortable\\App\\Chrome-bin\\chrome.exe"
        if args.graphicUI:
            #options.headless = True
            #options.add_argument('--headless')
            #options.add_argument('--disable-gpu')
            options.add_argument('window-size=1720x980')
        options.add_argument('log-level=3')#INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3.
        browser = webdriver.Chrome(executable_path= ruta+"/chromedriver.exe", options = options)

        try:
            browser.get(super().get_url())
            time.sleep(15)
            usuari = browser.find_element(by="xpath", value='//*[@id="dsm-user-fieldset"]/div/div/div[1]/input')
            usuari.send_keys(super().get_user())
            browser.find_element(by="xpath", value='//*[@id="sds-login-vue-inst"]/div/span/div/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div[3]').click()
            time.sleep(5)
            passwd = browser.find_element(by="xpath", value='//*[@id="dsm-pass-fieldset"]/div[1]/div/div[1]/input')
            passwd.send_keys(super().get_password())
            browser.find_element(by="xpath", value='//*[@id="sds-login-vue-inst"]/div/span/div/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div[4]').click()
            time.sleep(20)
            hypericon=browser.find_element(by="xpath", value='//*[@id="sds-desktop-shortcut"]/div/li[7]')
            hypericon.click()
            time.sleep(10)
        except Exception as e:
            print("Error de connexio web")
            now = datetime.datetime.now()
            date_string = now.strftime('%Y-%m-%d--%H-%M-%S-errorWeb')
            f = open(ruta+"/errorLogs/"+date_string+".txt",'w')
            f.write("Error de connexio web\n"+str(e))
            f.close()
            super().add_copies(Copia(super().get_name(), "Error de connexio web", temps(), self))
        else:


            #aconsegueix els noms de cada copia i els guarda en un array
            nomsCopies = []
            nomTots = browser.find_elements(by="class name", value="x-tree-node-anchor")
            for nom in nomTots:
                nomsCopies.append(nom.text)


            #aconsegueix els elements del menu de l'esquerra i els posa en un array
            roottreenode = browser.find_elements(by="class name", value="x-tree-node")



            #per cada element del menu de l'esquerra el clica i extreu les dades d'aquella copia
            y=0
            for treenode in roottreenode:
                treenode.click()
                time.sleep(2)
                statusCopies=(browser.find_element(by="xpath", value='/html/body/div[11]/div[14]/div[3]/div[1]/div/div/div/div[2]/div['+str(y+1)+']/div/div/div[1]/div/div[2]/div/div/div[1]/div[1]/div').text)
                
                if ((statusCopies[(y)]) != "Eliminando versiones de copia de seguridad...") and ((statusCopies[(y)]) !='Deleting backup versions...') and ((statusCopies[(y)]) !='Waiting...') and ((statusCopies[(y)]) !='Backing up...') and ((statusCopies[(y)]) !='Canceling...'):
                    super().add_copies(Copia(nomsCopies[y], statusCopies, datetime.datetime.now(), self))
                else:
                    super().add_copies(Copia(nomsCopies[y],"Espera a que acabi el proces actual", datetime.datetime.now(), self))
                y+=1