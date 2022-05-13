import datetime
import requests
import utils
from LlocDeCopies import LlocDeCopies
from Copia import Copia


class SynologyActive(LlocDeCopies):
    def __init__(self, name:str, url:str, user:str, password:str, cookie: str):
        """Constructor of the SynologyActive class 

        Parameters
        ----------
        name : String
            The object name

        url : String
            The url to the Synology NAS.

        user : String
            The user to use for Synology NAS. 

        password : String
            The password to use for the NAS user 

        apipassw : cookie
            The cookie for the api. how to get it in readme.

        Returns
        -------
        SynologyActive
            The newly instantiated SynologyActive object

        """
        self._cookie = cookie
        super().__init__(name, url, user, password)
        
    def retrieve_copies(self, ruta:str, args) -> None:
        """Saves copies to the array of this object
        
        Parameters
        ----------
        ruta : String
            Route to the folder the program is in.
        args:Namespace
            arguments of argsparse.
        """
        query_parameters = {"api":"SYNO.API.Info", "version":"1", "method":"query", "query":"all"}
        queryUrl = super().get_url() + "webapi/query.cgi"
        try:
            query = requests.get(queryUrl, params=query_parameters, headers={"cookie": self._cookie})
            query = query.json()
            path= str(query['data']['SYNO.API.Auth']['path'])
        except Exception as e:
            now = datetime.datetime.now()
            date_string = now.strftime('%Y-%m-%d--%H-%M-%S-Query')
            a = open(ruta+"/errorLogs/"+date_string+".txt",'w')
            a.write(str(e))
            a.close()
        user = super().get_user()
        password = super().get_password()
        try:
            url = super().get_url()+"webapi/"+ path
        except:
            super().add_copies(Copia(super().get_name(), "Error en connectar amb la maquina", datetime.datetime.now(), self))
            super().set_tempsUltimCheck()
            return
        url2 = super().get_url()+"webapi/entry.cgi"
        nom = super().get_name()
        try:
            sid = self.login(user, password, url, args, ruta)
            self.InfoCopies(url2, sid, args, ruta)
            self.logout(url, args, ruta)
        except:
            now = datetime.datetime.now()
            date_string = now.strftime('%Y-%m-%d--%H-%M-%S-Conexio')
            f = open(ruta+"/errorLogs/"+date_string+".txt",'w')
            f.write("Error en connectar amb la maquina "+nom)
            f.close()
            super().add_copies(Copia(super().get_name(), "Error en connectar amb la maquina", datetime.datetime.now(), self))
        super().set_tempsUltimCheck()
        
    #Es logueja en la webapi de synology 
    #Els parametres son les credencials, la url per fer el logeig i la cookie identificacio enlloc de la sid.
    #Retorna la sid que servira per identificar-nos en les operacions seguents
    def login(self, user:str, password:str, url:str, args, ruta:str) -> str:
        """Logs in the api of any v7 synology NAS


        Parameters
        ----------
        user: String
            The user of the Synology nas

        passwort: String
            The password of the user mentioned avobe.

        url: String
            The url of the Synology NAS.

        args:Namespace
            arguments of argsparse.

        ruta : String
            Route to the folder the program is in.


        Returns
        -------
        String
            The SID of the newly created session.
        """
        login_parameters = {"api":"SYNO.API.Auth", "version":"3", "method":"login", "account": user, "passwd": password, "session":"ActiveBackup", "format":"cookie"}
        my_headers = {"cookie": self._cookie}
        
        try:
            sid = response['data']['sid']
            response = requests.get(url, params=login_parameters, headers=my_headers).json()
        except Exception as e:
            now = datetime.datetime.now()
            date_string = now.strftime('%Y-%m-%d--%H-%M-%S-login')
            f = open(ruta+"/errorLogs/"+date_string+".txt",'w')
            f.write(str(e))
            f.close()
        if	response['success'] != True:
            now = datetime.datetime.now()
            date_string = now.strftime('%Y-%m-%d--%H-%M-%S-login')
            f = open(ruta+"/errorLogs/"+date_string+".txt",'w')
            f.write(str(response))
            f.close()
        try:
            return(sid)
        except:
            return None

    #Tanca la sessió anteriorment oberta per la funcio login
    #Els paramatres es la url del lloc de logout i la sid i la cookie per idenficació
    #Retorna la resposta de la webapi tan si es error com si es correcte
    def logout(self, url:str, args, ruta:str)->bool:
        """Closes all the sessions previously opened with the login method of a given NAS.

        Parameters
        ----------
        url:String
            The url of the Synology NAS to close the sessions with.

        args:Namespace
            arguments of argsparse.

        ruta : String
            Route to the folder the program is in.
        
        Returns
        -------
        bool
            If it logged out successfully True, otherwise False.
        """
        logout_parameters = {"api":"SYNO.API.Auth", "version":"2", "method":"logout", "session":"ActiveBackup"}
        my_headers={"cookie": self._cookie}
        response = requests.get(url, params=logout_parameters, headers=my_headers).json()
        if	response['success'] == True:
            return True
        else:
            now = datetime.datetime.now()
            date_string = now.strftime('%Y-%m-%d--%H-%M-%S-Logout')
            f = open(ruta+"/errorLogs/"+date_string+".txt",'w')
            f.write(str(response))
            f.close()
            return False

    #Aconsegueix la informacio de les copies de seguretat de un NAS
    #Els parametres son la sid i la cookie per identificació i la url del NAS al cual recolectar les dades
    def InfoCopies(self, url:str, sid:str, args, ruta:str)->None:
        """Retrieve the copies from the given Synology NAS url.

        Parameters
        ----------
        url:String
            The url of the Synology NAS.

        sid: String
            The sid of the opened session.

        args:Namespace
            arguments of argsparse.

        ruta : String
            Route to the folder the program is in.
        
        
        """
        copies_parameters = {"api":"SYNO.ActiveBackup.Overview", "version":"1", "method":"list_device_transfer_size", "time_start": int(super().get_tempsUltimCheck())-args.date, "time_end": utils.temps(), "_sid": sid}
        response = requests.get(url, params=copies_parameters, headers={"cookie": self._cookie}).json()
        if	response['success'] == True:
            x = 0
            while x < int(response['data']['total']):
                numCopies = len(response['data']['device_list'][x]['transfer_list']) -1
                if not(numCopies < 0):
                    try:
                        nomCopia = response['data']['device_list'][x]['transfer_list'][numCopies]['device_name']
                        status = response['data']['device_list'][x]['transfer_list'][numCopies]['status']
                        try:
                            temps = utils.utcToTime(response['data']['device_list'][x]['transfer_list'][numCopies]['time_end'])
                        except Exception as e:
                            temps = utils.utcToTime(super().get_tempsUltimCheck())
                    except:
                        pass
                    else:
                        super().add_copies(Copia(nomCopia, utils.statusConvertor(status), temps, self))
                x+=1
            
        else:
            now = datetime.datetime.now()
            date_string = now.strftime('%Y-%m-%d--%H-%M-%S-Backups')
            f = open(ruta+"/errorLogs/"+date_string+".txt",'w')
            f.write(str(response))
            f.close()
            super().add_copies(Copia(id, "Fallo en extraccio de dades", datetime.datetime.now(), self))
