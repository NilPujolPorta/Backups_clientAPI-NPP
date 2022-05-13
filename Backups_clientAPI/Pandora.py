import datetime
import utils
import requests
from LlocDeCopies import LlocDeCopies
from Copia import Copia

class Pandora(LlocDeCopies):
    def __init__(self, name:str, url:str, user:str, password:str, apipassw:str):
        """Constructor of the Pandora class 

        Parameters
        ----------
        name : String
            The object name

        url : String
            The url to the Pandora API.

        user : String
            The user to use for PandoraFMS server 

        password : String
            The password to use for the PandoraFMS user 

        apipassw : String
            The password to the api

        Returns
        -------
        Pandora
            The newly instantiated Pandora object

        """
        self._apipassw = apipassw
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
        try:
            parameters = {"op":"get", "op2":"all_agents", "return_type":"json", "apipass":self._apipassw, "user":super().get_user(), "pass":super().get_password()}
            agentsFull = requests.get(super().get_url(), params=parameters).json()
        except Exception as e:
            now = datetime.datetime.now()
            date_string = now.strftime('%Y-%m-%d--%H-%M-%S-Connexio')
            f = open(ruta+"/errorLogs/"+date_string+".txt",'w')
            f.write("Error de conexio"+str(e))
            f.close()
            return

        for agent in agentsFull['data']:
            super().add_copies(Copia(agent['alias'], utils.statusConvertorPandora(agent['status']), datetime.datetime.now(), self))